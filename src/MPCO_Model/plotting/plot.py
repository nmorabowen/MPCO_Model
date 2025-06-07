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

        # Initialize color cycle for automatic coloring
        color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        self.color_iter = itertools.cycle(color_cycle)

    def pushover_plot(
        self,
        selection_set_id_verticalAxis: int,
        direction_verticalAxis: int,
        selection_set_id_horizontallAxis: int,
        direction_horizontalAxis: int,
        color: str = None,
        ax=None,
        figsize=(10, 6),
        title: str = None,
        save_path: str = None,
    ):
        """
        Plots a pushover curve (e.g., base shear vs top displacement) from the given model dataset.

        This function aggregates nodal results from two selection sets: one for the vertical axis 
        (e.g., base reaction force) and one for the horizontal axis (e.g., control node displacement).

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

        # Choose color (override > from parameters > from cycle)
        if color is None:
            color = parameters.color or next(self.color_iter)

        # Plot using STKO_to_python base plotter
        self.dataset.plot.plot_nodal_results(
            model_stage=parameters.model_stage,
            results_name_verticalAxis=parameters.results_name_verticalAxis,
            selection_set_id_verticalAxis=selection_set_id_verticalAxis,
            direction_verticalAxis=direction_verticalAxis,
            values_operation_verticalAxis=parameters.values_operation_verticalAxis,
            scaling_factor_verticalAxis=parameters.scaling_factor_verticalAxis,
            results_name_horizontalAxis=parameters.results_name_horizontalAxis,
            selection_set_id_horizontallAxis=selection_set_id_horizontallAxis,
            direction_horizontalAxis=direction_horizontalAxis,
            values_operation_horizontalAxis=parameters.values_operation_horizontalAxis,
            scaling_factor_horizontalAxis=parameters.scaling_factor_horizontalAxis,
            ax=ax,
            label=label,
            color=color,
            linetype=parameters.linestyle,
            linewidth=parameters.linewidth,
        )

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            fig.savefig(save_path+'svg', format='svg')

        return ax
