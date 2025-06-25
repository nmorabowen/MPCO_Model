import os
from numpy import ndarray

from STKO_to_python import MPCODataSet
from MPCO_Model.plotting.plot import Plot
from MPCO_Model.mass.dynamicMass import Masses


class Model:
    def __init__(self, dataset: MPCODataSet, stories = None):
        self.dataset = dataset
        self.stories = stories

        # Define composite classes for added functionality
        self.plot:Plot = Plot(dataset)
        
        # Create info related to the masses
        masses_folder = self.dataset.hdf5_directory
        masses_file = os.path.join(masses_folder, 'results','nodeMassCoord.out')
        
        if os.path.exists(masses_file) and stories is not None:
            self.mass:Masses = Masses(folder_path=masses_folder,
                                    stories=stories)
        else:
            self.mass=None

        # Validation
        print("Model initialized with dataset:", dataset.info.name)

    @property
    def name(self) -> str:
        return self.dataset.info.name

    @property
    def root_folder(self) -> str:
        return self.dataset.hdf5_directory

    @property
    def directory(self) -> str:
        return self.dataset.hdf5_directory
    
    def __repr__(self):
        return f"<Model {self.name} at {self.directory}>"

