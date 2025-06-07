import numpy as np
from STKO_to_python import MPCODataSet
import matplotlib.pyplot as plt
import os
from matplotlib.gridspec import GridSpec

from MPCO_Model.plotting.setup import PlotStyle
PlotStyle()

from MPCO_Model.plotting.plot import Plot

class Model:
    def __init__(self, dataset: MPCODataSet):
        self.dataset = dataset

        # Define composite classes for added functionality
        self.plot:Plot = Plot(dataset)

        # Validation
        print("Model initialized with dataset:", dataset.info.name)

    @property
    def name(self) -> str:
        return self.dataset.info.name

    @property
    def directory(self) -> str:
        return self.dataset.hdf5_directory
    
    def __repr__(self):
        return f"<Model {self.name} at {self.directory}>"

