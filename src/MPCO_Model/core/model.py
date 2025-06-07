import numpy as np
from STKO_to_python import MPCODataSet
import matplotlib.pyplot as plt
import os
from matplotlib.gridspec import GridSpec

from MPCO_Model.plotting.setup import PlotStyle
PlotStyle()

class Model:
    def __init__(self, dataset: MPCODataSet):
        self.dataset = dataset




