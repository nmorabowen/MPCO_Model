import itertools
import os

from STKO_to_python import MPCODataSet
import matplotlib.pyplot as plt


from ..dataclass.plotProperties import Pushover_plot_parameters, TH_parameters_plot_parameters

if TYPE_CHECKING:
    from STKO_to_python import MPCODataSet

class Plot:
    def __init__(self, dataset: "MPCODataSet"):
        self.dataset = dataset
        # Initialize color cycle for automatic coloring
        color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        self.color_iter = itertools.cycle(color_cycle)

    def pushover_plot(
        self,
        selection_set_id_verticalAxis: int,
        direction_verticalAxis: int,
        parameters: Pushover_plot_parameters,
        color: str = None,
        ax=None,
        figsize=(10, 6),
        title: str = None,
        save_path: str = None,
    ):
        """
        Plots pushover curve: base shear vs top displacement.

        Arguments:
        - selection_set_id_verticalAxis: for base shear or reaction force
        - direction_verticalAxis: typically 1 or 2 (global Y)
        - parameters: configuration object (model_stage, scaling, etc.)
        - color: optional override; falls back to parameter or default cycle
        """
        
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
            selection_set_id_horizontallAxis=parameters.selection_set_id_horizontalAxis,
            direction_horizontalAxis=parameters.direction_horizontalAxis,
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
