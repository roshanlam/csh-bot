import unittest
import json
from lib import calcGrade
class TestCalcGrade(unittest.TestCase):
    def test_calcGrade(self):
        gradeData = {"class": "cs220", "hw": 90, "midterm1": 37, "midterm2": 47, "final": 100, "lecture": 70, "lab": 100}
        expected_grade = 71.48
        self.assertAlmostEqual(calcGrade(gradeData), expected_grade, places=2)

if __name__ == '__main__':
    unittest.main()
