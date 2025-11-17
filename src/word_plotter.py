from abc import ABC, abstractmethod
from typing import Dict, List
import matplotlib
import matplotlib.pyplot as plt


class WordPlotter(ABC):
    """Handles plotting functionality for word frequency data."""

    LABELS = ["Low Reviews", "Medium Reviews", "High Reviews"]

    def __init__(self) -> None:
        self.x_vals = [0, 1, 2]  # x axis positions for the three categories

    @abstractmethod
    def plot(
        self,
        word: str,
        word_data: Dict[str, Dict[str, List[int]]],
        max_frequency: int,
        subplot: matplotlib.axes._axes.Axes,
    ) -> None:
        """
        This function takes the word_data dictionary, the word, and the max_frequency, and
        plots the frequencies for this word's use in low, medium, and high reviews when
        rating professors.

        Args:
            word_data (dict): Dictionary containing word frequency data for all words
            word (str): The word to plot
            max_frequency (int): Maximum frequency for y-axis scaling
            subplot (matplotlib.axes._axes.Axes): The subplot to plot on
        """
        pass


class WomenWordPlotter(WordPlotter):
    """Plotting functionality for word frequency data associated with women"""

    def plot(
        self,
        word: str,
        word_data: Dict[str, Dict[str, List[int]]],
        max_frequency: int,
        subplot: matplotlib.axes._axes.Axes,
    ) -> None:
        """Plot word frequency data for women professors."""
        # Get the counts for women across all three review buckets
        y_vals = word_data[word]['W']
        
        # Create bar chart
        subplot.bar(self.x_vals, y_vals, color="tab:pink")
        subplot.set_title(f'"{word}" used in reviews of women professors')
        subplot.set_xlabel("Review Rating")
        subplot.set_ylabel("Frequency")
        subplot.set_xticks(self.x_vals)
        subplot.set_xticklabels(self.LABELS)
        subplot.set_ylim(0, max_frequency)


class MenWordPlotter(WordPlotter):
    """Plotting functionality for word frequency data associated with men"""

    def plot(
        self,
        word: str,
        word_data: Dict[str, Dict[str, List[int]]],
        max_frequency: int,
        subplot: matplotlib.axes._axes.Axes,
    ) -> None:
        """Plot word frequency data for men professors."""
        # Get the counts for men across all three review buckets
        y_vals = word_data[word]['M']
        
        # Create bar chart
        subplot.bar(self.x_vals, y_vals, color="tab:blue")
        subplot.set_title(f'"{word}" used in reviews of men professors')
        subplot.set_xlabel("Review Rating")
        subplot.set_ylabel("Frequency")
        subplot.set_xticks(self.x_vals)
        subplot.set_xticklabels(self.LABELS)
        subplot.set_ylim(0, max_frequency)