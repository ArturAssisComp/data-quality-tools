import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
import seaborn as sns
import pandas as pd
from matplotlib.colors import LogNorm

class PlotOperations:
    _DPI=300
    
    def plot_heatmap(self, df:pd.DataFrame, title:str, base_result_filepath:str, fig_name:str, log_scale=False):
        # Define your order
        order = list(df.columns)

        # Reorder your DataFrame
        df = df.loc[list(reversed(order)), order]

        # Increase the figure size
        plt.figure(figsize=(20, 14))
    
        # calculate vmin and vmax
        df_copy = df.copy()
        for col in df_copy.columns:
            df_copy.loc[col, col] = np.nan
        vmin = df_copy.min().min()
        vmax = df_copy.max().max()

        delta = 1e-3
        min_log_scale = 1
        norm = LogNorm(vmin=vmin + delta + min_log_scale, vmax=vmax + delta)  if log_scale else None

        int_annot = np.vectorize(lambda x: f"{int(x)}")(df + delta)
        sns.heatmap(df + delta, vmax=vmax, vmin=vmin, annot=int_annot, cmap='coolwarm', annot_kws={"color": 'white', "size": 7, "fontweight": 800}, fmt='', linewidths=1, norm=norm)

        # Add a title to the heatmap
        plt.title(title, fontsize=20, pad=20)  # Added padding for better visualization

        # Improve axis labels readability
        plt.xticks(fontsize=10, rotation=45)  # Rotation for better visibility
        plt.yticks(fontsize=10, rotation=0)

        # Use a tight layout to make sure everything fits
        plt.tight_layout()

        # Save the plot to a PNG file with high resolution
        plt.savefig(os.path.join(base_result_filepath, fig_name), dpi=self._DPI)
        plt.close()


    # TODO remove `suffix` arg because it is not necessary. The arg `relative` is enough
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


