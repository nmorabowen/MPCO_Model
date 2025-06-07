from dataclasses import dataclass

@dataclass
class Pushover_plot_parameters:
    """
    Parameters for the pushover data extraction and plotting.
    The pushover curve will be plotted with the base reaction force at some selection set versus the displecement at another selection set.

    We are leaving the selection set and the direction as user values to be pass on the plot method.

    # LARGA VIDA AL LADRUÑO
    """
    # GLOBAL PARAMETERS
    model_stage: str = 'MODEL_STAGE[5]'

    # FOR THE REACTION FORCE
    results_name_verticalAxis: str = 'REACTION_FORCE'
    values_operation_verticalAxis='Sum' 
    scaling_factor_verticalAxis=-1

    # FOR THE DISPLACEMENT
    results_name_horizontalAxis='DISPLACEMENT'
    values_operation_horizontalAxis='Sum'
    scaling_factor_horizontalAxis=1

    linestyle: str = '-'
    linewidth: float = 1.0

@dataclass
class TH_parameters_plot_parameters:
    """
    Parameters for the time history data extraction and plotting.
    The time history plot will be plotted with the ('DISPLACEMENT', 'ACCELERATION', 'VELOCITY') component at some selection set versus the 'TIME'.

    We are leaving the selection set, the direction, and the result name as user values to be pass on the plot method.

    # LARGA VIDA AL LADRUÑO
    """
    # GLOBAL PARAMETERS
    model_stage: str = 'MODEL_STAGE[5]'

    # VALUES FOR THE VERTICAL AXIS
    values_operation_verticalAxis='Mean'
    results_name_horizontalAxis='TIME'
    scaling_factor_verticalAxis=1

    linestyle: str = '-'
    linewidth: float = 1.0





