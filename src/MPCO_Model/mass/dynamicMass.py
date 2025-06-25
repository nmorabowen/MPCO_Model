import os
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Optional


class Masses:
    """
    In order to use this class, you need to have the OpenSees output files in a specific format.
    Add the getMass custom command to the STKO model to generate the nodeMassCoord.out file.
    """
    def __init__(self, folder_path, stories=None):
        """
        :param folder_path: Path to the directory containing OpenSees output files.
        """
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"The folder path '{folder_path}' is not a valid directory.")
        self.folder_path = folder_path
        self.stories=stories

    def _get_masses(self, filename='nodeMassCoord.out', results_path='results'):
        """
        Reads the nodeMassCoord.out file (or any similarly formatted file) and returns a pandas DataFrame.
        
        Expected format in the file (one header line starting with '#'):
        # nodeID  xCrd  yCrd  zCrd  Mx  My  Mz  Mrx  Mry  Mrz
        1  0.0  0.0  0.0  12.0  0.0  0.0  0.0  0.0  0.0
        2  10.0  0.0  0.0  12.0  0.0  0.0  0.0  0.0  0.0
        ...
        
        :param filename: The name of the file to read (default = 'nodeMassCoord.out').
        :return: A pandas DataFrame with columns:
                 ['nodeID','xCrd','yCrd','zCrd','Mx','My','Mz','Mrx','Mry','Mrz'].
        :raises FileNotFoundError: If the file does not exist.
        :raises ValueError: If the file is empty or improperly formatted.
        """
        # Build full path to the file
        filepath = os.path.join(self.folder_path, results_path, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"The file '{filepath}' does not exist.")
        
        # Log the file reading
        logging.info(f"Reading file: {filepath}")
        
        # Define column names
        col_names = ['nodeID', 'xCrd', 'yCrd', 'zCrd', 'Mx', 'My', 'Mz', 'Mrx', 'Mry', 'Mrz']
        
        # Read the file using pandas
        try:
            df = pd.read_csv(
                filepath,
                comment='#',
                sep=r'\s+',
                header=None,
                names=col_names,
                encoding='utf-8'
            )
            if df.empty:
                raise ValueError(f"The file '{filename}' is empty or improperly formatted.")
        except Exception as e:
            raise ValueError(f"Error reading '{filename}': {str(e)}")
        
        # Ensure correct data types
        df = df.astype({
            'nodeID': int,
            'xCrd': float, 'yCrd': float, 'zCrd': float,
            'Mx': float, 'My': float, 'Mz': float,
            'Mrx': float, 'Mry': float, 'Mrz': float
        })
        
        return df
           
    def _aggregated_mass(self, filename='nodeMassCoord.out', results_path='results', plot=False, scalingFactorPlot=0.00005):
        """
        Aggregates all masses (Mx, My, Mz, Mrx, Mry, Mrz) by a specified axis coordinate (x, y, or z).

        :param filename: The name of the file to read (default = 'nodeMassCoord.out').
        :param results_path: Path to the results directory (default = 'results').
        :param plot: If True, generates a 2D plot of aggregated masses.
        :return: A pandas DataFrame with the specified axis coordinate and aggregated masses.
        """

        # Get the DataFrame with mass data
        df = self._get_masses(filename, results_path)

        # Rename the chosen axis for grouping
        coord_column = 'zCrd'

        # Aggregate masses by the specified coordinate
        aggregated = df.groupby(coord_column)[['Mx', 'My', 'Mz', 'Mrx', 'Mry', 'Mrz']].sum().reset_index()

        if plot:
            fig, ax = plt.subplots(ncols=3, nrows=1, figsize=(10, 8))

            if self.stories is not None and len(self.stories) > 1:
                # Calculate the story heights (difference between consecutive z-coordinates)
                story_heights = np.diff(self.stories)
                min_floor_height = np.min(story_heights)
                max_radius = min_floor_height / 3  # Maximum radius for markers
                max_area = np.pi * max_radius**2*scalingFactorPlot  # Corresponding maximum area for markers
            else:
                max_area = 100  # Reduced default max area if story heights are not available

            max_size = aggregated[['Mx', 'My', 'Mz']].max().max()

            for i, mass in enumerate(['Mx', 'My', 'Mz']):
                # Calculate sizes ensuring they don't exceed max_radius
                sizes = (aggregated[mass] / max_size) * max_area
                
                ax[i].scatter(
                    [0] * len(aggregated['zCrd']), 
                    aggregated['zCrd'],
                    s=sizes,  # This will now be properly scaled
                    alpha=0.6, 
                    label=mass
                )
                ax[i].set_title(f'{mass} vs zCrd')
                ax[i].set_xlabel('X (fixed at 0)')
                ax[i].set_ylabel('zCrd')
                if self.stories is not None:
                    ax[i].set_yticks(self.stories)
                ax[i].grid(True)
                ax[i].legend()

            plt.tight_layout()
            plt.show()
            
    def _aggregated_mass_lumped(self, filename='nodeMassCoord.out', results_path='results', plot=False, scalingFactorPlot=0.00005):
        """
        Aggregates all masses (Mx, My, Mz, Mrx, Mry, Mrz) to each story level.
        If `stories` is defined, the mass is aggregated specifically for each story level,
        summing the masses from nodes with `zCrd` values > floor below and <= current floor.

        :param filename: The name of the file to read (default = 'nodeMassCoord.out').
        :param results_path: Path to the results directory (default = 'results').
        :param plot: If True, generates a 2D plot of aggregated masses for each story.
        :param scalingFactorPlot: Scaling factor for marker sizes in the plot.
        :return: A pandas DataFrame with aggregated masses for each story.
        """
        if self.stories is None:
            raise ValueError("Stories are not defined. Please define `stories` before using this method.")
        
        # Get the DataFrame with mass data
        df = self._get_masses(filename, results_path)

        # Rename the chosen axis for grouping
        coord_column = 'zCrd'

        # Initialize a list to store the aggregated results
        lumped_masses_list = []

        # Iterate through each story level
        for i, story in enumerate(self.stories):
            if i == 0:
                # First floor, include all masses <= current floor
                filtered_nodes = df[df[coord_column] <= story]
            else:
                # Floors above the first, include masses > previous floor and <= current floor
                floor_below = self.stories[i - 1]
                filtered_nodes = df[(df[coord_column] > floor_below) & (df[coord_column] <= story)]

            # Aggregate masses for the filtered nodes
            aggregated_masses = filtered_nodes[['Mx', 'My', 'Mz', 'Mrx', 'Mry', 'Mrz']].sum()

            # Append the results as a dictionary to the list
            lumped_masses_list.append({'story': story, **aggregated_masses})

        # Convert the list of dictionaries to a DataFrame
        lumped_masses = pd.DataFrame(lumped_masses_list)

        # Ensure the story column matches the type of self.stories (usually float or int)
        lumped_masses['story'] = lumped_masses['story'].astype(type(self.stories[0]))

        if plot:
            # Plot similar to the _aggregated_mass method
            fig, ax = plt.subplots(ncols=3, nrows=1, figsize=(10, 8))

            # Determine max radius based on story heights
            if len(self.stories) > 1:
                story_heights = np.diff(self.stories)
                min_floor_height = np.min(story_heights)
                max_radius = min_floor_height / 3  # Maximum radius for markers
                max_area = np.pi * max_radius**2 * scalingFactorPlot  # Corresponding maximum area for markers
            else:
                max_area = 100  # Reduced default max area if story heights are not available

            max_size = lumped_masses[['Mx', 'My', 'Mz']].max().max()

            for i, mass in enumerate(['Mx', 'My', 'Mz']):
                # Calculate sizes ensuring they don't exceed max_radius
                sizes = (lumped_masses[mass] / max_size) * max_area
                
                ax[i].scatter(
                    [0] * len(lumped_masses['story']), 
                    lumped_masses['story'],
                    s=sizes,  # This will now be properly scaled
                    alpha=0.6, 
                    label=mass
                )
                ax[i].set_title(f'{mass} vs Story')
                ax[i].set_xlabel('X (fixed at 0)')
                ax[i].set_ylabel('Story')
                ax[i].set_yticks(self.stories)
                ax[i].grid(True)
                ax[i].legend()

            plt.tight_layout()
            plt.show()

        return lumped_masses

    def get_first_periods(self, n: int = 5, modal_filename: str = 'modal.txt') -> list[float]:
        """
        Reads the first `n` modal periods from the modal analysis report file.

        Parameters
        ----------
        n : int
            Number of modal periods to return (default = 5).
        modal_filename : str
            Name of the modal report file (default is 'modal.txt').

        Returns
        -------
        List[float]
            List of the first `n` modal periods.

        Raises
        ------
        FileNotFoundError
            If the modal report file is not found.
        ValueError
            If the periods could not be parsed.
        """
        filepath = os.path.join(self.folder_path, modal_filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Modal file '{filepath}' not found.")

        periods = []

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and line[0].isdigit():
                    parts = line.split()
                    if len(parts) >= 5:
                        try:
                            periods.append(float(parts[4]))  # 5th column = Period
                            if len(periods) == n:
                                break
                        except ValueError:
                            raise ValueError(f"Could not parse period from line: {line}")

        if len(periods) < n:
            raise ValueError(f"Only found {len(periods)} modal periods (expected {n}).")

        return periods