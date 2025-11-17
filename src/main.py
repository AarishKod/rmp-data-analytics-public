import sys
import matplotlib.pyplot as plt

sys.path.append(".")

from src.data_loader import DataLoader
from src.word_plotter import WomenWordPlotter, MenWordPlotter


def main() -> None:
    """Main function to run the word analysis program."""

    if len(sys.argv) < 2:
        print("Usage: python main.py <word>")
        sys.exit(1)

    word = sys.argv[1]

    if len(sys.argv) > 2:
        data_filename = sys.argv[2]
    else:
        data_filename = "data/full-data.txt"

    data = DataLoader.load_dictionary(data_filename)

    max_frequency = 0
    for gender, frequencies in data.get(word, {}).items():
        max_frequency = max(max_frequency, *frequencies)

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    WomenWordPlotter().plot(word, data, max_frequency, ax1)
    MenWordPlotter().plot(word, data, max_frequency, ax2)

    plt.show()


if __name__ == "__main__":
    main()
