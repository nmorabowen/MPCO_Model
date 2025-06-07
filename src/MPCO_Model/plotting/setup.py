import matplotlib.pyplot as plt
from cycler import cycler

class PlotStyle:
    def __init__(self):
        self.main_colors = [
            'blue', 'black', 'red', 'gray', '#000077', '#5E7470'
        ]
        self.extended_colors = [
            # Cool Blues and Teals
            '#2E3B4E', '#4A5E7E', '#6A8BA3', '#8AACBF', '#A8C9DC', '#C6E5F7',
            '#2F4F4F', '#4E6F6F', '#6E8F8F', '#8EB0B0', '#AED1D1',
            # Muted Purples and Violets
            '#3C2F51', '#5A4A7A', '#7C6799', '#9D87B7', '#BFA7D5',
            # Muted Reds and Oranges
            '#502F2A', '#744E49', '#976E69', '#BA8E88', '#DCCDBF',
            '#5D3C33', '#855E52', '#B0876F', '#CCA695', '#E8CCB9',
            # Soft Greens
            '#2F4632', '#546E58', '#7B977F', '#A3BFA7', '#CADFD1',
            # Neutrals and Low-Yellows
            '#4D463D', '#7A756C', '#A19E98', '#C6C4BF', '#E6E5E2', '#F7F6F4'
        ]
        self.full_palette = self.main_colors + self.extended_colors

    def __call__(self):
        self.apply()

    def apply(self):
        full_palette = self.full_palette
        plt.rcParams['axes.prop_cycle'] = cycler('color', full_palette)

        # Font settings
        plt.rcParams['font.family'] = 'Archivo Narrow'
        plt.rcParams['font.size'] = 10
        plt.rcParams['font.stretch'] = 'condensed'

        # Grid appearance
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.color'] = (200/255, 200/255, 200/255)
        plt.rcParams['grid.linestyle'] = '--'
        plt.rcParams['grid.linewidth'] = 0.5
        plt.rcParams['grid.alpha'] = 0.6

        # Minor ticks
        plt.rcParams['xtick.minor.visible'] = True
        plt.rcParams['ytick.minor.visible'] = True
        plt.rcParams['xtick.direction'] = 'out'
        plt.rcParams['ytick.direction'] = 'out'

        # Axis spines
        plt.rcParams['axes.spines.top'] = False
        plt.rcParams['axes.spines.right'] = False
        plt.rcParams['axes.spines.left'] = True
        plt.rcParams['axes.spines.bottom'] = True

        # Legend
        plt.rcParams['legend.frameon'] = True
        plt.rcParams['legend.facecolor'] = (0.97, 0.97, 0.97)
        plt.rcParams['legend.edgecolor'] = 'none'
        plt.rcParams['legend.framealpha'] = 1.0
        plt.rcParams['legend.fancybox'] = False
        plt.rcParams['legend.borderpad'] = 1.10

        # Figure appearance
        plt.rcParams['figure.dpi'] = 100

