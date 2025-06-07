import itertools
import os
from typing import TYPE_CHECKING

from STKO_to_python import MPCODataSet
import matplotlib.pyplot as plt

from MPCO_Model.dataclass.plotProperties import Pushover_plot_parameters, TH_parameters_plot_parameters

if TYPE_CHECKING:
    from STKO_to_python import MPCODataSet

class Plot:
    def __init__(self, dataset: "MPCODataSet"):
        self.dataset = dataset

        # Call the default plot parameters
        self.default_parameters_PO = Pushover_plot_parameters()
        self.default_parameters_TH = TH_parameters_plot_parameters()


    def pushover_plot(
        self,
        selection_set_id_verticalAxis: int = 2,
        selection_set_id_horizontalAxis: int = 1,
        direction: int= 1,
        color: str = 'black',
        ax=None,
        figsize=(10, 6),
        title: str = None,
        save_svg:bool = False,
    ):
        """
        Plots a pushover curve (e.g., base shear vs top displacement) from the given model dataset.

        This function aggregates nodal results from two selection sets: one for the vertical axis 
        (e.g., base reaction force) and one for the horizontal axis (e.g., control node displacement).

        - We assume the direction is the same for both axes, as it is common in pushover analysis.
        - If multiple nodes are set on the selection sets, the results are aggregated using the specified operation (in this case they are set to sum).

        Args:
            selection_set_id_verticalAxis (int): 
                The ID of the selection set for the vertical axis (e.g., base reactions).
            direction_verticalAxis (int): 
                The component direction (0=x, 1=y, 2=z) for vertical axis aggregation.
            selection_set_id_horizontallAxis (int): 
                The ID of the selection set for the horizontal axis (e.g., control displacement).
            direction_horizontalAxis (int): 
                The component direction (0=x, 1=y, 2=z) for horizontal axis aggregation.
            color (str, optional): 
                Line color for the curve. If None, uses the parameter-defined or automatic cycling color.
            ax (matplotlib.axes.Axes, optional): 
                An existing matplotlib Axes object to plot on. If None, a new figure and axes are created.
            figsize (tuple, optional): 
                Size of the figure if `ax` is not provided. Defaults to (10, 6).
            title (str, optional): 
                Title or label for the curve (also used in the legend). Defaults to the model name.
            save_path (str, optional): 
                Path to save the figure. If provided, the figure is saved as SVG.

        Returns:
            matplotlib.axes.Axes: 
                The matplotlib Axes object containing the plot.
        """
        
        parameters=self.default_parameters_PO

        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)

        label = title or self.dataset.info.name

        # Plot using STKO_to_python base plotter
        ax, results = self.dataset.plot.plot_nodal_results(
            model_stage=parameters.model_stage,
            results_name_verticalAxis=parameters.results_name_verticalAxis,
            selection_set_id_verticalAxis=selection_set_id_verticalAxis,
            direction_verticalAxis=direction,
            values_operation_verticalAxis=parameters.values_operation_verticalAxis,
            scaling_factor_verticalAxis=parameters.scaling_factor_verticalAxis,
            results_name_horizontalAxis=parameters.results_name_horizontalAxis,
            selection_set_id_horizontalAxis=selection_set_id_horizontalAxis,
            direction_horizontalAxis=direction,
            values_operation_horizontalAxis=parameters.values_operation_horizontalAxis,
            scaling_factor_horizontalAxis=parameters.scaling_factor_horizontalAxis,
            ax=ax,
            label=label,
            color=color,
            linetype=parameters.linestyle,
            linewidth=parameters.linewidth,
        )

        if save_svg:
            save_path = self.dataset.hdf5_directory
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            fig=ax.get_figure()
            filename = 'PO_'+str(direction)+'.svg'
            fig.savefig(save_path + filename, format='svg')

        return ax, results

    def time_history_plot(self,
                          results_name_verticalAxis='DISPLACEMENT',
                          selection_set_id_verticalAxis=1,
                          direction=1,
                          color: str = 'black',
                          ax=None,
                          figsize=(10, 6),
                          title: str = None,
                          save_svg: bool = False):
            """
            Plots a time history response (e.g., displacement, acceleration) at a given selection set.

            This method uses the vertical axis to represent time-varying results (such as 
            displacement, acceleration, or force) for a selection set, and the horizontal 
            axis as time (taken from the dataset's time step records).

            Args:
                results_name_verticalAxis (str, optional): 
                    The name of the result to plot over time (e.g., 'DISPLACEMENT', 'ACCELERATION').
                selection_set_id_verticalAxis (int, optional): 
                    The ID of the selection set containing the nodes of interest.
                direction (int, optional): 
                    The index of the direction (0=x, 1=y, 2=z) to extract from the result.
                color (str, optional): 
                    Line color for the plot. Defaults to 'black'.
                ax (matplotlib.axes.Axes, optional): 
                    Optional Axes object to plot on. If None, a new figure and axes will be created.
                figsize (tuple, optional): 
                    Size of the figure if `ax` is not provided. Defaults to (10, 6).
                title (str, optional): 
                    Custom title or legend label. Defaults to the dataset name.
                save_path (str, optional): 
                    Directory path to save the figure. If provided, the figure is saved as SVG with
                    filename `TH_<direction>.svg`.

            Returns:
                tuple:
                    - ax (matplotlib.axes.Axes): The matplotlib Axes object containing the plot.
                    - results (dict): Dictionary containing `x_array` (time) and `y_array` (response).
            """


            parameters=self.default_parameters_TH

            if ax is None:
                fig, ax = plt.subplots(figsize=figsize)

            label = title or self.dataset.info.name

            # Plot using STKO_to_python base plotter
            ax, results = self.dataset.plot.plot_nodal_results(
                model_stage=parameters.model_stage,
                results_name_verticalAxis=results_name_verticalAxis,
                selection_set_id_verticalAxis=selection_set_id_verticalAxis,
                direction_verticalAxis=direction,
                values_operation_verticalAxis=parameters.values_operation_verticalAxis,
                scaling_factor_verticalAxis=parameters.scaling_factor_verticalAxis,
                results_name_horizontalAxis=parameters.results_name_horizontalAxis,
                ax=ax,
                label=label,
                color=color,
                linetype=parameters.linestyle,
                linewidth=parameters.linewidth
            )

            if save_svg:
                save_path = self.dataset.hdf5_directory
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                fig=ax.get_figure()
                filename = 'TH_'+str(direction)+'.svg'
                fig.savefig(save_path + filename, format='svg')

            return ax, results






