# bmi-calculator

## Project Description
The BMI Calculator is a Python application that calculates a user's Body Mass Index (BMI) using their weight and height. It classifies the result into standard BMI categories and stores BMI records for users.

This project was developed as part of my Python Internship.

## Objective
To develop a BMI Calculator that calculates BMI, displays the corresponding category, validates user input, and maintains BMI history.

## Technologies Used
- Python
- Tkinter
- SQLite3
- Matplotlib

## Features
- Graphical user interface built with Tkinter.
- Accepts the user's name, weight in kilograms, and height in metres.
- Calculates BMI using the formula:

  **BMI = Weight (kg) / Height (m)²**

- Displays the BMI value rounded to two decimal places.
- Classifies BMI into the following categories:
  - Underweight: BMI below 18.5
  - Normal: BMI from 18.5 to below 25
  - Overweight: BMI from 25 to below 30
  - Obese: BMI of 30 or above
- Validates weight and height inputs.
- Displays colour-coded BMI category results.
- Saves records for multiple named users in an SQLite database.
- Displays a user's BMI history as a line chart using Matplotlib.
- Handles database errors with error messages.

## Project Structure

```text
bmi-calculator/
├── bmi_calculator.py
├── README.md
└── screenshots/
    └── bmi_calculator_output.png
```

The `bmi_records.db` database is created automatically when the application runs.

## Installation and Execution

### Prerequisites
- Python 3 installed on your computer.
- Tkinter available with your Python installation.

### Install Matplotlib

Open the terminal and run:

```bash
python -m pip install matplotlib
```

### Run the Application

1. Download or clone this repository.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Run the following command:

```bash
python bmi_calculator.py
```

5. Enter the user's name, weight, and height.
6. Click **Calculate BMI & Save Record** to calculate BMI and save the record.
7. Enter a user's name and click **View BMI History Chart** to view their saved BMI history.

## BMI Categories

| BMI Range | Category |
|---|---|
| Below 18.5 | Underweight |
| 18.5 to below 25 | Normal |
| 25 to below 30 | Overweight |
| 30 or above | Obese |

## Screenshots

The `screenshots/` folder contains a screenshot of the BMI Calculator application.

## Conclusion

The BMI Calculator demonstrates Python GUI development, BMI calculation, input validation, SQLite database operations, and BMI history visualisation using Matplotlib.

**Internship Task:** Task 2 — BMI Calculator
