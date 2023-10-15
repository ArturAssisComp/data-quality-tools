import logging
import os
from tools.null_value_inspector.snapshot.row_null_distribution.model.model import RowNullDistributionSnapshotModel

from tools.null_value_inspector.model.documentation import Documentation
from utils.file_operations import FileOperations
from logger.utils import get_custom_logger_name
from utils.statistics import std_dev_weighted

from matplotlib import pyplot as plt
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 2, 'last'))

class StatisticalSummaryOverviewGenerator:
    _logger:logging.Logger
    _fileOperations:FileOperations
    _row_null_distribution_snapshot:RowNullDistributionSnapshotModel
    _row_null_distribution_snapshot_filepath:str
    _base_result_filepath:str
    _documentation:Documentation
    def __init__(self, logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations()):
        self._logger = logger
        self._fileOperations = fileOperations
    
    def generate_overview(self, row_null_distribution_snapshot_filepath:str, base_result_filepath:str, documentation:Documentation):
        self._logger.info('Creating overview')
        self._row_null_distribution_snapshot = RowNullDistributionSnapshotModel(** self._fileOperations.read_Json(row_null_distribution_snapshot_filepath))
        self._row_null_distribution_snapshot_filepath = row_null_distribution_snapshot_filepath
        self._base_result_filepath = base_result_filepath
        self._documentation = documentation
        try:
            self._generate_statistical_summary()
        except Exception as e:
            self._logger.error(f'Result not generated: {e}')
    


    def _generate_statistical_summary(self):
        distribution_by_row = self._row_null_distribution_snapshot.content

        general_summary = self._create_general_summary(distribution_by_row)

        if general_summary.get('total_columns'):
            completeness_metric = self._create_completeness_metric(general_summary)
        else: 
            completeness_metric = None

        # average nulls per row
        average_nulls_per_row = self._create_average_nulls_per_row(general_summary)

        # standard deviation nulls per row
        std_deviation_nulls_per_row = self._create_std_deviation_nulls_per_row(distribution_by_row)

        # TODO average nulls per column
        # TODO std deviation nulls per columns

        statistical_summary = {
            'general_summary':general_summary,
            'completeness_metric':completeness_metric,
            'average_nulls_per_row':average_nulls_per_row,
            'std_deviation_nulls_per_row':std_deviation_nulls_per_row,
        }

        # save the result
        self._fileOperations.to_json(os.path.join(self._base_result_filepath, 'statistical_summary.json'), statistical_summary)

        # save to a pdf
        try:
            self._generate_pdf_report(statistical_summary, os.path.join(self._base_result_filepath, 'report.pdf'))
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
        c.drawString(1 * inch, 7.5 * inch, "General Summary")
        c.drawString(1 * inch, 7 * inch, f"Total Rows: {data['general_summary']['total_rows']}")
        c.drawString(1 * inch, 6.8 * inch, f"Total Nulls: {data['general_summary']['total_nulls']}")
        c.drawString(1 * inch, 6.6 * inch, f"Max Nulls Per Row: {data['general_summary']['max_nulls_per_row']}")
        c.drawString(1 * inch, 6.4 * inch, f"Min Nulls Per Row: {data['general_summary']['min_nulls_per_row']}")
        c.drawString(1 * inch, 6.2 * inch, f"Average Nulls Per Row: {data['average_nulls_per_row']}")
        c.drawString(1 * inch, 6 * inch, f"Std Deviation Nulls Per Row: {data['std_deviation_nulls_per_row']}")

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

    def _create_general_summary(self, distribution_by_row:dict[int, int]):
        total_rows = sum(distribution_by_row.values())
        total_nulls = sum(k*v for k, v in distribution_by_row.items())
        max_nulls_per_row = max(distribution_by_row)
        min_nulls_per_row = min(distribution_by_row)
        if self._documentation.column:
            column_list = self._documentation.column
            total_columns = len(self._documentation.column)
            total_cells = total_rows * total_columns
            total_nulls_percentage = round(100 * total_nulls / (total_cells), 2)
        else:
            column_list = None
            total_columns = None
            total_cells = None
            total_nulls_percentage = None

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
        
    def _create_std_deviation_nulls_per_row(self, distribution:dict[int, int]):
        return round(std_dev_weighted(distribution), 4)