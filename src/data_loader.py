from typing import Dict, List
from collections.abc import Hashable
import pandas as pd

class DataLoader:
    """Handles loading and processing of data files."""

    @staticmethod
    def load_dictionary(filename: str) -> Dict[str, Dict[str, List[int]]]:
        """
        Loads the given file's contents as a dictionary and returns it.
        """
        try:
            df = pd.read_csv(filename, sep=',')
        except FileExistsError as e:
            print(f"Error: {e}")

        return DataLoader.create_data_structure(df.to_dict())

    @staticmethod
    def create_data_structure(data: Dict[Hashable, Dict[Hashable, str]]) -> Dict[str, Dict[str, List[int]]]:
        """Creates the data structure containing word counts"""
        structure: Dict[str, Dict[str, List[int]]] = {}

        dict_of_comments = data["Comment Text"]

        for key in dict_of_comments:
            list_of_words = dict_of_comments[key].split()
            for word in list_of_words:
                if word not in structure:
                    structure[word] = {
                        'W': [0, 0, 0],
                        'M': [0, 0, 0]
                    }
                gender: str = data["Professor Gender"][key]
                structure[word][gender][0 if float(data["Rating"][key]) < 2.5 else 1 if 2.5 <= float(data["Rating"][key]) <= 3.5 else 2] += 1

        return structure