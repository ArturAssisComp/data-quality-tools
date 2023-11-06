import logging
import os
from typing import Any

import numpy as np
from globals.types import SnapshotType
from tools.data_consistency_inspector.snapshot.column_inconsistency_count_by_type.model.model import ColumnInconsistencyCountByTypeSnapshotContent
from tools.data_consistency_inspector.snapshot.row_inconsistency_distribution.model.model import RowInconsistencyDistributionSnapshotContent
from tools.base_result_generator.base_generator import BaseOverviewGenerator

from utils.file_operations import FileOperations
from logger.utils import get_custom_logger_name
from utils.statistics import std_dev_weighted

from matplotlib import pyplot as plt
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 2, 'last'))


class StatisticalSummaryOverviewGenerator(BaseOverviewGenerator):
    _needed_snapshots:list[SnapshotType] = [SnapshotType.COLUMN_INCONSISTENCY_COUNT_BY_TYPE_SNAPSHOT, SnapshotType.ROW_INCONSISTENCY_DISTRIBUTION_SNAPSHOT]
    def __init__(self,snapshot_filepath:dict[SnapshotType, str], logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations()):
        super().__init__(snapshot_filepath, logger=logger, fileOperations=fileOperations)
    
    
    
    def _handle_content(self, parsed_content_dict:dict[SnapshotType, Any], basedir_path:str, name_preffix:str=''):
        columnInconsistencyCountByTypeSnapshotContentModel = parsed_content_dict[SnapshotType.COLUMN_INCONSISTENCY_COUNT_BY_TYPE_SNAPSHOT]
        columnInconsistencyCountSnapshotContent = self._count_by_type_to_count_by_column(columnInconsistencyCountByTypeSnapshotContentModel)
        rowInconsistencyDistributionSnapshotContentModel = parsed_content_dict[SnapshotType.ROW_INCONSISTENCY_DISTRIBUTION_SNAPSHOT]
        try:
            self._generate_statistical_summary(rowInconsistencyDistributionSnapshotContentModel, columnInconsistencyCountByTypeSnapshotContentModel, columnInconsistencyCountSnapshotContent, basedir_path, name_preffix=name_preffix)
        except Exception as e:
            self._logger.error(f'Result not generated: {e}')

    
                
    # TODO refactor: used in multiple classes
    def _count_by_type_to_count_by_column(self, column_inconsistency_count_by_type_snapshot_content:ColumnInconsistencyCountByTypeSnapshotContent):
        result:dict[str, int] = dict()
        for key, value in column_inconsistency_count_by_type_snapshot_content.content.items():
            result[key] = sum(value.values())
        return result
    

    def _generate_statistical_summary(self, row_inconsistency_distribution_snapshot_content_model:RowInconsistencyDistributionSnapshotContent, column_inconsistency_count_by_type_snapshot_content_model:ColumnInconsistencyCountByTypeSnapshotContent, column_inconsistency_count_snapshot_content:dict[str, int], base_dir_path:str, name_preffix:str=''):
        distribution_by_row = row_inconsistency_distribution_snapshot_content_model.content
        inconsistencies_per_column = column_inconsistency_count_snapshot_content
        inconsistencies_per_column_per_type = column_inconsistency_count_by_type_snapshot_content_model.content

        general_summary = self._create_general_summary(distribution_by_row, inconsistencies_per_column)

        consistency_metric = self._create_consistency_metric(general_summary)

        # average inconsistencies per row
        average_inconsistencies_per_row = self._create_average_inconsistencies_per_row(general_summary)

        # average inconsistencies per column
        average_inconsistencies_per_column = self._create_average_inconsistencies_per_column(general_summary)


        # standard deviation inconsistencies per row
        std_deviation_inconsistencies_per_row = self._create_std_deviation_inconsistencies_per_row(distribution_by_row)

        # standard deviation inconsistencies per column
        std_deviation_inconsistencies_per_column = self._create_std_deviation_inconsistencies_per_column(list(inconsistencies_per_column.values()))

        inconsistencies_by_column_by_type = self._get_inconsistencies_by_column_by_type(inconsistencies_per_column_per_type, inconsistencies_per_column)


        statistical_summary = {
            'general_summary':general_summary,
            'consistency_metric':consistency_metric,
            'average_inconsistencies_per_row':average_inconsistencies_per_row,
            'average_inconsistencies_per_column':average_inconsistencies_per_column,
            'std_deviation_inconsistencies_per_row':std_deviation_inconsistencies_per_row,
            'std_deviation_inconsistencies_per_column':std_deviation_inconsistencies_per_column,
            'inconsistencies_by_column_by_type':inconsistencies_by_column_by_type,
        }

        # save the result
        self._fileOperations.to_json(os.path.join(base_dir_path, name_preffix + 'statistical_summary.json'), statistical_summary)

        # save to a pdf
        try:
            self._generate_pdf_report(statistical_summary, os.path.join(base_dir_path, name_preffix + 'report.pdf'))
        finally:
            plt.close()

        self._logger.info('statistical_summary.json generated!')

    def _get_inconsistencies_by_column_by_type(self, inconsistencies_per_column_per_type:dict[str, dict[str, int]], inconsistencies_per_column:dict[str, int]):
        max_columns = 10
        result = []
        for n, (col, num_of_inconsistencies) in enumerate(sorted(inconsistencies_per_column.items(), key=lambda x:x[1], reverse=True)):
            if n == max_columns:
                break
            col_status = {
                'col':col,
                'total':num_of_inconsistencies,
                'inconsistencies':list()
            }
            for item in sorted(inconsistencies_per_column_per_type[col].items(), key=lambda x:x[1], reverse=True):
                col_status['inconsistencies'].append(item)
            result.append(col_status)
        return result


        
    def _generate_pdf_report(self, data:dict, output_filename="report.pdf"):
        c = canvas.Canvas(output_filename, pagesize=landscape(letter))
        self._write_summary(c, data)
        c.showPage()
        self._generate_pie_chart(c, data['general_summary']['total_inconsistencies'], data['general_summary']['total_cells'])
        c.save()
        self._logger.info('report.pdf generated!')
    
    def _write_summary(self, c: canvas.Canvas, data: dict):
            height = landscape(letter)[1]
            initial_y = height - inch
            margin = inch
            bottom_margin = inch
            space_between_sections = 0.25 * inch

            self._add_section_title(c, "Data Quality Report - Data Consistency Inspector", initial_y, 18)
            initial_y -= space_between_sections

            initial_y = self._add_section(c, "General Summary", initial_y, data['general_summary'], margin, bottom_margin)
            initial_y -= space_between_sections
            
            initial_y = self._add_section(c, "Statistical Summary", initial_y, {
                'Average Inconsistencies Per Row': data['average_inconsistencies_per_row'],
                'Std Deviation Inconsistencies Per Row': data['std_deviation_inconsistencies_per_row'],
                'Average Inconsistencies Per Column': data['average_inconsistencies_per_column'],
                'Std Deviation Inconsistencies Per Column': data['std_deviation_inconsistencies_per_column'],
                'Consistency Metric': f"{data['consistency_metric']}%"
            }, margin, bottom_margin)
            initial_y -= space_between_sections

            self._add_inconsistencies_details(c, data['inconsistencies_by_column_by_type'], initial_y, margin, bottom_margin)

    def _add_section_title(self, c:canvas.Canvas, title:str, y:float, font_size:float):
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(inch, y, title)
        return y - 0.3 * inch

    def _add_section(self, c:canvas.Canvas, section_title:str, initial_y:float, section_data:dict, margin:float, bottom_margin:float):
        initial_y = self._add_section_title(c, section_title, initial_y, 14)
        c.setFont("Helvetica", 12)
        for key, value in section_data.items():
            text = f"{key}: {value}"
            c.drawString(margin, initial_y, text)
            initial_y -= 0.2 * inch
            if initial_y <= bottom_margin:
                c.showPage()
                initial_y = landscape(letter)[1] - inch
                c.setFont("Helvetica", 12)
        return initial_y

    def _add_inconsistencies_details(self, c: canvas.Canvas, inconsistencies_data: dict, initial_y: float, margin: float, bottom_margin: float):
        initial_y = self._add_section_title(c, "Inconsistencies per Column per Type", initial_y, 14)
        c.setFont("Helvetica", 12)
        line_height = 0.25 * inch  # Increase the line height for better readability

        if inconsistencies_data:
            initial_y += line_height
            for col_status in inconsistencies_data:
                initial_y -= line_height  # Increase spacing before starting a new column section
                c.drawString(margin, initial_y, f"Column '{col_status['col']}' - Total Inconsistencies: {col_status['total']}")

                for constraint, count in col_status['inconsistencies']:
                    initial_y -= line_height  # Consistent spacing between constraints
                    
                    # Set font to bold for constraint name
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(margin + 0.5 * inch, initial_y, f"• \"{constraint}\": ")
                    
                    # Calculate the width of the constraint name and bullet point to place the count correctly
                    constraint_name_width = c.stringWidth(f"• \"{constraint}\": ", "Helvetica-Bold", 12)
                    
                    # Reset font to regular for the count and draw it
                    c.setFont("Helvetica", 12)
                    c.drawString(margin + 0.5 * inch + constraint_name_width, initial_y, f"{count}")

                    # Check if we need to start a new page
                    if initial_y <= bottom_margin:
                        c.showPage()
                        initial_y = landscape(letter)[1] - inch  # Reset initial_y for the new page
                        c.setFont("Helvetica", 12)  # Reset font settings for the new page

        return initial_y  # Return the updated Y position in case more content needs to be added after this



    def _generate_pie_chart(self, c:canvas.Canvas, total_inconsistencies:int, total_cells:int):
        labels = ['Total Inconsistencies', 'Not Inconsistent']
        sizes = [total_inconsistencies, total_cells - total_inconsistencies]
        colors = ['red', 'green']

        # Create the pie chart using matplotlib
        fig, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title("Inconsistencies Distribution")

        # Save the pie chart to a file
        pie_chart_filename = "pie_chart.png"
        plt.savefig(pie_chart_filename, bbox_inches='tight')  # bbox_inches='tight' to remove extra white spaces

        # Get the page width and height in points
        page_width, page_height = landscape(letter)

        # Calculate the image width, assuming 1 inch margin on each side
        image_width = page_width / 2 
        image_height = image_width  # Keep the aspect ratio of the pie chart

        # Calculate the position where the top of the image will be at the top margin
        top_margin = 2 * inch  # You can adjust this value as needed
        x_position = page_width / 2 - image_width / 2
        y_position = page_height - top_margin - image_height  # Subtract the image height and top margin from page height

        # Draw the pie chart on the canvas
        c.drawImage(pie_chart_filename, x_position, y_position, width=image_width, height=image_height)

        # Close the figure to free memory and remove the pie chart file
        plt.close(fig)
        os.remove(pie_chart_filename)

    def _create_general_summary(self, distribution_by_row:dict[int, int], column_inconsistencies_count:dict[str, int]):
        total_rows = sum(distribution_by_row.values())
        total_inconsistencies = sum(k*v for k, v in distribution_by_row.items())
        max_inconsistencies_per_row = max(distribution_by_row)
        min_inconsistencies_per_row = min(distribution_by_row)
        column_list = list(column_inconsistencies_count.keys())
        total_columns = len(column_list)
        total_cells = total_rows * total_columns
        total_inconsistencies_percentage = round(100 * total_inconsistencies / (total_cells), 2)
        return {
            'total_rows': total_rows,
            'total_inconsistencies':total_inconsistencies,
            'total_cells':total_cells,
            'max_inconsistencies_per_row':max_inconsistencies_per_row,
            'min_inconsistencies_per_row':min_inconsistencies_per_row,
            'total_columns':total_columns,
            'columns_list':column_list,
            'total_inconsistencies_percentage':total_inconsistencies_percentage,
        }

    def _create_consistency_metric(self, general_summary:dict):
        return round(100 - general_summary['total_inconsistencies_percentage'], 2)

    def _create_average_inconsistencies_per_row(self, general_summary:dict):
        return round(general_summary['total_inconsistencies'] / general_summary['total_rows'], 2)

    def _create_average_inconsistencies_per_column(self, general_summary:dict):
        return round(general_summary['total_inconsistencies'] / general_summary['total_columns'], 2)
        
    def _create_std_deviation_inconsistencies_per_row(self, distribution:dict[int, int]):
        return round(std_dev_weighted(distribution), 4)

    def _create_std_deviation_inconsistencies_per_column(self, values:list[int]):
        return round(np.std(values), 4)





