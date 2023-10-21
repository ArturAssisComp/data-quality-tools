import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os

class PlotOperations:
    _DPI=300

    def plot_figure(self, x:list[int], y:list[float]|list[int], y_label:str, x_label:str, title:str, average_value:float, has_label_on_top:bool, fig_name:str, relative:bool, suffix:str, base_result_filepath:str, x_labels:list[str]|None=None):
        """
        This method generates a bar chart with the given parameters and saves it as a PNG file.

        Parameters:
        - `x` (list[int]): The x-coordinates of the bars.
        - `y` (list[float] or list[int]): The heights of the bars.
        - `y_label` (str): The label for the y-axis.
        - `x_label` (str): The label for the x-axis.
        - `title` (str): The title of the plot.
        - `average_value` (float): The value at which to draw a vertical line representing the average.
        - `has_label_on_top` (bool): Whether to add data labels on top of the bars.
        - `fig_name` (str): The name of the output PNG file.
        - `relative` (bool): Whether to format the y-tick labels to display percentages.
        - `suffix` (str): The suffix to add to the data labels on top of the bars.
        - `base_result_filepath` (str): The directory in which to save the output PNG file.
        - `x_labels` (list[str], optional): The labels for the x-ticks. Defaults to None.
        """
        # Use a style for the plot
        plt.style.use('ggplot')

        # Create a color map
        cmap = plt.get_cmap('viridis')

        # Create a bar chart with color map
        bars = plt.bar(x, y, color=cmap(np.linspace(0, 1, len(y))))

        # Label the axes
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        # Add a title
        plt.title(title)

        # Add data labels on top of the bars
        if has_label_on_top:
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}{suffix}', va='bottom', ha='center') # Add percentage sign to the label


        if x_labels:
            # Add a vertical line at the average value
            plt.xticks(range(len(x)), x_labels, rotation=45, ha='right', fontsize=6, fontweight='bold')
            plt.axhline(average_value, color='r', linestyle='--', label=f'Average: {average_value:.2f}')
        else:
            # Add a vertical line at the average value
            plt.axvline(average_value, color='r', linestyle='--', label=f'Average: {average_value:.2f}')
            # Ensure x-axis only displays integer values
            plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        plt.legend()  # Display the legend to show what the vertical line represents
        
        if relative:
            # Format the y-tick labels to display percentages
            plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter())

        # Ensure everything fits
        plt.tight_layout()

        # Save the plot to a PNG file with high resolution
        plt.savefig(os.path.join(base_result_filepath, fig_name), dpi=self._DPI)
        plt.close()


