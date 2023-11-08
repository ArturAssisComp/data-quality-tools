import logging
import os
from typing import Any

import numpy as np
from globals.types import SnapshotType
from tools.null_value_inspector.snapshot.row_null_distribution.model.model import RowNullDistributionSnapshotContent
from tools.null_value_inspector.snapshot.column_null_count.model.model import ColumnNullCountSnapshotContent
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
    _needed_snapshots:list[SnapshotType] = [SnapshotType.COLUMN_NULL_COUNT_SNAPSHOT, SnapshotType.ROW_NULL_DISTRIBUTION_SNAPSHOT]
    def __init__(self,snapshot_filepath:dict[SnapshotType, str], logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations()):
        super().__init__(snapshot_filepath, logger=logger, fileOperations=fileOperations)
    
    
    
    def _handle_content(self, parsed_content_dict:dict[SnapshotType, Any], basedir_path:str, name_preffix:str=''):
        columnNullCountSnapshotContentModel = parsed_content_dict[SnapshotType.COLUMN_NULL_COUNT_SNAPSHOT]
        rowNullDistributionSnapshotContentModel = parsed_content_dict[SnapshotType.ROW_NULL_DISTRIBUTION_SNAPSHOT]
        try:
            self._generate_statistical_summary(rowNullDistributionSnapshotContentModel, columnNullCountSnapshotContentModel, basedir_path, name_preffix=name_preffix)
        except Exception as e:
            self._logger.error(f'Result not generated: {e}')

    
                
    

    def _generate_statistical_summary(self, row_null_distribution_snapshot_content_model:RowNullDistributionSnapshotContent, column_null_count_snapshot_model:ColumnNullCountSnapshotContent, base_dir_path:str, name_preffix:str=''):
        distribution_by_row = row_null_distribution_snapshot_content_model.content
        nulls_per_column = column_null_count_snapshot_model.content

        general_summary = self._create_general_summary(distribution_by_row, nulls_per_column)

        completeness_metric = self._create_completeness_metric(general_summary)

        # average nulls per row
        average_nulls_per_row = self._create_average_nulls_per_row(general_summary)

        # average nulls per column
        average_nulls_per_column = self._create_average_nulls_per_column(general_summary)


        # standard deviation nulls per row
        std_deviation_nulls_per_row = self._create_std_deviation_nulls_per_row(distribution_by_row)

        # standard deviation nulls per column
        std_deviation_nulls_per_column = self._create_std_deviation_nulls_per_column(list(nulls_per_column.values()))


        statistical_summary = {
            'general_summary':general_summary,
            'completeness_metric':completeness_metric,
            'average_nulls_per_row':average_nulls_per_row,
            'average_nulls_per_column':average_nulls_per_column,
            'std_deviation_nulls_per_row':std_deviation_nulls_per_row,
            'std_deviation_nulls_per_column':std_deviation_nulls_per_column,
        }

        # save the result
        self._fileOperations.to_json(os.path.join(base_dir_path, name_preffix + 'statistical_summary.json'), statistical_summary)

        # save to a pdf
        try:
            self._generate_pdf_report(statistical_summary, os.path.join(base_dir_path, name_preffix + 'report.pdf'))
        finally:
            plt.close()

        self._logger.info('statistical_summary.json generated!')


    def _generate_pdf_report(self, data:dict, output_filename="report.pdf"):
        # Create PDF using reportlab
        c = canvas.Canvas(output_filename, pagesize=landscape(letter))
        self._write_summary(c, data)
        if data['general_summary']['total_cells']:
            self._generate_pie_chart(c, data['general_summary']['total_nulls'], data['general_summary']['total_cells'])
        c.showPage()
        c.save()
        self._logger.info('report.pdf generated!')
    
    def _write_summary(self, c:canvas.Canvas, data:dict):
        initial_y = 8
        # Main Title
        c.setFont("Helvetica-Bold", 18)
        c.drawString(1 * inch, initial_y * inch, "Data Quality Report - Null Value Inspector")

        # General Summary Title
        c.setFont("Helvetica-Bold", 14)
        initial_y -= 0.5
        c.drawString(1 * inch, initial_y * inch, "General Summary")
        
        # General Summary Details
        c.setFont("Helvetica", 12)
        initial_y -= 0.2
        c.drawString(1 * inch, initial_y * inch, f"Total Rows: {data['general_summary']['total_rows']}")
        initial_y -= 0.2
        c.drawString(1 * inch,  initial_y * inch, f"Total Nulls: {data['general_summary']['total_nulls']}")
        initial_y -= 0.2
        c.drawString(1 * inch,  initial_y * inch, f"Max Nulls Per Row: {data['general_summary']['max_nulls_per_row']}")
        initial_y -= 0.2
        c.drawString(1 * inch,  initial_y * inch, f"Min Nulls Per Row: {data['general_summary']['min_nulls_per_row']}")
        initial_y -= 0.2
        c.drawString(1 * inch,  initial_y * inch, f"Total Columns: {data['general_summary']['total_columns']}")
        initial_y -= 0.2
        c.drawString(1 * inch,  initial_y * inch, f"Total Nulls Percentage: {data['general_summary']['total_nulls_percentage']}%")
        initial_y -= 0.2

        # Statistical Summary Title
        c.setFont("Helvetica-Bold", 14)
        initial_y -= 0.3
        c.drawString(1 * inch, initial_y * inch, "Statistical Summary")
        
        # Statistical Summary Details
        c.setFont("Helvetica", 12)
        initial_y -= 0.3
        c.drawString(1 * inch, initial_y * inch, f"Average Nulls Per Row: {data['average_nulls_per_row']}")
        initial_y -= 0.2
        c.drawString(1 * inch,  initial_y * inch, f"Std Deviation Nulls Per Row: {data['std_deviation_nulls_per_row']}")
        initial_y -= 0.2
        c.drawString(1 * inch,  initial_y * inch, f"Average Nulls Per Column: {data['average_nulls_per_column']}")
        initial_y -= 0.2
        c.drawString(1 * inch,  initial_y * inch, f"Std Deviation Nulls Per Column: {data['std_deviation_nulls_per_column']}")
        initial_y -= 0.2
        c.drawString(1 * inch,  initial_y * inch, f"Completeness Metric: {data['completeness_metric']}%")


    def _generate_pie_chart(self, c:canvas.Canvas, total_nulls:int, total_cells:int):
        # Plotting data
        labels = 'Total Nulls', 'Not Null'
        sizes = [total_nulls, total_cells - total_nulls]
        colors = ['red', 'green']

        _, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title("Nulls Distribution")
        plt.savefig("pie_chart.png")
        c.drawInlineImage("pie_chart.png", 5*inch, 5*inch, width=3*inch, height=3*inch)
        os.remove('pie_chart.png')

    def _create_general_summary(self, distribution_by_row:dict[int, int], column_null_count:dict[str, int]):
        total_rows = sum(distribution_by_row.values())
        total_nulls = sum(k*v for k, v in distribution_by_row.items())
        max_nulls_per_row = max(distribution_by_row)
        min_nulls_per_row = min(distribution_by_row)
        snapshot =  self._snapshots[SnapshotType.COLUMN_NULL_COUNT_SNAPSHOT]
        assert snapshot
        column_list = snapshot.columns.copy()
        total_columns = len(column_list)
        total_cells = total_rows * total_columns
        total_nulls_percentage = round(100 * total_nulls / (total_cells), 2)
        return {
            'total_rows': total_rows,
            'total_nulls':total_nulls,
            'total_cells':total_cells,
            'max_nulls_per_row':max_nulls_per_row,
            'min_nulls_per_row':min_nulls_per_row,
            'total_columns':total_columns,
            'columns_list':column_list,
            'total_nulls_percentage':total_nulls_percentage,
        }

    def _create_completeness_metric(self, general_summary:dict):
        return round(100 - general_summary['total_nulls_percentage'], 2)

    def _create_average_nulls_per_row(self, general_summary:dict):
        return round(general_summary['total_nulls'] / general_summary['total_rows'], 2)

    def _create_average_nulls_per_column(self, general_summary:dict):
        return round(general_summary['total_nulls'] / general_summary['total_columns'], 2)
        
    def _create_std_deviation_nulls_per_row(self, distribution:dict[int, int]):
        return round(std_dev_weighted(distribution), 4)

    def _create_std_deviation_nulls_per_column(self, values:list[int]):
        return round(np.std(values), 4)





