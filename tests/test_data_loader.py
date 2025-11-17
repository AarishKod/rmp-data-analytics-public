import unittest
import sys
import pandas as pd
import os

sys.path.append(".")
from src.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    """Unit tests for DataLoader class."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        # Create a temporary directory for test files
        self.test_dir = "data/test-data.txt"

    def tearDown(self) -> None:
        """Clean up after each test method."""
        # Remove temporary test files
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

    def test_create_data_structure_single_word_single_gender(self) -> None:
        """Test creating structure with one word and one gender."""
        data = {
            "Comment Text": {0: "great"},
            "Professor Gender": {0: "W"},
            "Rating": {0: "4.0"}
        }
        
        result = DataLoader.create_data_structure(data)
        
        self.assertIn("great", result)
        self.assertEqual(result["great"]["W"], [0, 0, 1])
        self.assertEqual(result["great"]["M"], [0, 0, 0])

    def test_create_data_structure_multiple_words(self) -> None:
        """Test creating structure with multiple words."""
        data = {
            "Comment Text": {0: "great teacher"},
            "Professor Gender": {0: "M"},
            "Rating": {0: "3.0"}
        }
        
        result = DataLoader.create_data_structure(data)
        
        self.assertIn("great", result)
        self.assertIn("teacher", result)
        self.assertEqual(result["great"]["M"], [0, 1, 0])
        self.assertEqual(result["teacher"]["M"], [0, 1, 0])

    def test_create_data_structure_low_rating_bucket(self) -> None:
        """Test that ratings < 2.5 go to bucket 0."""
        data = {
            "Comment Text": {0: "bad"},
            "Professor Gender": {0: "W"},
            "Rating": {0: "2.0"}
        }
        
        result = DataLoader.create_data_structure(data)
        
        self.assertEqual(result["bad"]["W"], [1, 0, 0])

    def test_create_data_structure_medium_rating_bucket(self) -> None:
        """Test that ratings 2.5-3.5 go to bucket 1."""
        data = {
            "Comment Text": {0: "okay"},
            "Professor Gender": {0: "M"},
            "Rating": {0: "3.0"}
        }
        
        result = DataLoader.create_data_structure(data)
        
        self.assertEqual(result["okay"]["M"], [0, 1, 0])

    def test_create_data_structure_high_rating_bucket(self) -> None:
        """Test that ratings > 3.5 go to bucket 2."""
        data = {
            "Comment Text": {0: "excellent"},
            "Professor Gender": {0: "W"},
            "Rating": {0: "4.5"}
        }
        
        result = DataLoader.create_data_structure(data)
        
        self.assertEqual(result["excellent"]["W"], [0, 0, 1])

    def test_create_data_structure_boundary_ratings(self) -> None:
        """Test boundary values for rating buckets."""
        data = {
            "Comment Text": {
                0: "word1",  # 2.5 exactly
                1: "word2",  # 3.5 exactly
                2: "word3"   # Just above 3.5
            },
            "Professor Gender": {0: "W", 1: "M", 2: "W"},
            "Rating": {0: "2.5", 1: "3.5", 2: "3.6"}
        }
        
        result = DataLoader.create_data_structure(data)
        
        self.assertEqual(result["word1"]["W"], [0, 1, 0])  # 2.5 goes to bucket 1
        self.assertEqual(result["word2"]["M"], [0, 1, 0])  # 3.5 goes to bucket 1
        self.assertEqual(result["word3"]["W"], [0, 0, 1])  # 3.6 goes to bucket 2

    def test_create_data_structure_multiple_reviews(self) -> None:
        """Test with multiple reviews across different buckets."""
        data = {
            "Comment Text": {
                0: "great class",
                1: "great professor",
                2: "bad class"
            },
            "Professor Gender": {0: "W", 1: "M", 2: "W"},
            "Rating": {0: "4.0", 1: "4.5", 2: "2.0"}
        }
        
        result = DataLoader.create_data_structure(data)
        
        # "great" appears twice in high bucket (once W, once M)
        self.assertEqual(result["great"]["W"], [0, 0, 1])
        self.assertEqual(result["great"]["M"], [0, 0, 1])
        
        # "class" appears once in high bucket (W) and once in low bucket (W)
        self.assertEqual(result["class"]["W"], [1, 0, 1])
        
        # "bad" appears once in low bucket (W)
        self.assertEqual(result["bad"]["W"], [1, 0, 0])

    def test_create_data_structure_repeated_words_same_review(self) -> None:
        """Test that repeated words in same review count multiple times."""
        data = {
            "Comment Text": {0: "great great great"},
            "Professor Gender": {0: "M"},
            "Rating": {0: "4.0"}
        }
        
        result = DataLoader.create_data_structure(data)
        
        self.assertEqual(result["great"]["M"], [0, 0, 3])

    def test_create_data_structure_both_genders(self) -> None:
        """Test that both genders are tracked correctly."""
        data = {
            "Comment Text": {
                0: "excellent",
                1: "excellent"
            },
            "Professor Gender": {0: "W", 1: "M"},
            "Rating": {0: "4.0", 1: "4.0"}
        }
        
        result = DataLoader.create_data_structure(data)
        
        self.assertEqual(result["excellent"]["W"], [0, 0, 1])
        self.assertEqual(result["excellent"]["M"], [0, 0, 1])

    def test_load_dictionary_valid_file(self) -> None:
        """Test loading a valid CSV file."""
        # Create a test CSV file
        test_file = os.path.join(self.test_dir, "test_data.csv")
        with open(test_file, 'w') as f:
            f.write("Comment Text,Professor Gender,Rating\n")
            f.write("great teacher,W,4.0\n")
            f.write("okay class,M,3.0\n")
        
        result = DataLoader.load_dictionary(test_file)
        
        self.assertIn("great", result)
        self.assertIn("teacher", result)
        self.assertEqual(result["great"]["W"], [0, 0, 1])
        self.assertEqual(result["okay"]["M"], [0, 1, 0])

    def test_load_dictionary_complex_file(self) -> None:
        """Test loading a CSV with multiple rows and various ratings."""
        test_file = os.path.join(self.test_dir, "complex_data.csv")
        with open(test_file, 'w') as f:
            f.write("Comment Text,Professor Gender,Rating\n")
            f.write("amazing professor,W,5.0\n")
            f.write("terrible class,M,1.5\n")
            f.write("average teacher,W,3.0\n")
            f.write("amazing class,M,4.8\n")
        
        result = DataLoader.load_dictionary(test_file)
        
        # "amazing" appears in high bucket for both genders
        self.assertEqual(result["amazing"]["W"], [0, 0, 1])
        self.assertEqual(result["amazing"]["M"], [0, 0, 1])
        
        # "terrible" appears in low bucket
        self.assertEqual(result["terrible"]["M"], [1, 0, 0])

    def test_create_data_structure_empty_comment(self) -> None:
        """Test handling of empty comment text."""
        data = {
            "Comment Text": {0: ""},
            "Professor Gender": {0: "W"},
            "Rating": {0: "4.0"}
        }
        
        result = DataLoader.create_data_structure(data)
        
        # Should return empty structure since no words
        self.assertEqual(result, {})

    def test_create_data_structure_whitespace_handling(self) -> None:
        """Test that multiple spaces are handled correctly."""
        data = {
            "Comment Text": {0: "great  teacher   excellent"},  # Multiple spaces
            "Professor Gender": {0: "M"},
            "Rating": {0: "4.0"}
        }
        
        result = DataLoader.create_data_structure(data)
        
        self.assertIn("great", result)
        self.assertIn("teacher", result)
        self.assertIn("excellent", result)
        # Empty strings from split should not create entries
        self.assertNotIn("", result)


if __name__ == '__main__':
    unittest.main()