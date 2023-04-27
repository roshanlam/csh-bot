import unittest
import json

def calcGrade(grades: dict):
    with open('gradeCalc.json') as f:
        data = json.load(f)
    grade = 0
    for key in data:
        if key == grades['class']:
            data = data[key]
            break
    for key in grades:
        if key == 'class':
            continue
        grade += grades[key] * (data[key]/100)
    return grade

class TestCalcGrade(unittest.TestCase):
    def test_calcGrade(self):
        gradeData = {"class": "cs220", "hw": 90, "midterm1": 37, "midterm2": 47, "final": 100, "lecture": 70, "lab": 100}
        expected_grade = 71.48
        self.assertAlmostEqual(calcGrade(gradeData), expected_grade, places=2)

if __name__ == '__main__':
    unittest.main()
