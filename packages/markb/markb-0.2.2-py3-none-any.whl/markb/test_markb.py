import unittest

from markb import detect_readme_filename, ReadmeFilenameNotDetected


class MarkbTests(unittest.TestCase):

    def test_detect_various_readme_filenames(self):
        filenames = ["README.md", "README", "README.txt", "README.markdown",
                     "readme.md", "readme", "readme.txt", "readme.markdown"]

        for filename in filenames:
            detected = detect_readme_filename([filename])
            self.assertEqual(detected, filename)

    def test_detection_raises_when_not_found(self):
        filenames = ["index.html", "index.js", "cat.png"]
        with self.assertRaises(ReadmeFilenameNotDetected):
            detect_readme_filename(filenames)
    
    def test_detection_among_files(self):
        filenames = ["index.html", "index.js", "README", "cat.png"]
        detected = detect_readme_filename(filenames)
        self.assertEqual(detected, "README")
    


if __name__ == "__main__":
    unittest.main()
