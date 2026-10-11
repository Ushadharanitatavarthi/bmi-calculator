
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


DB_NAME = "bmi_records.db"


# ---------- Database ----------

def initialize_database():
    with sqlite3.connect(DB_NAME) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                recorded_at TEXT NOT NULL
            )
        """)


def save_record(name, weight, height, bmi, category):
    with sqlite3.connect(DB_NAME) as connection:
        connection.execute("""
            INSERT INTO bmi_records
            (name, weight, height, bmi, category, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name, weight, height, bmi, category,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))


# ---------- BMI calculation ----------

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", "#D97706"
    elif bmi < 25:
        return "Normal", "#15803D"
    elif bmi < 30:
        return "Overweight", "#EA580C"
    else:
        return "Obese", "#DC2626"


def calculate_bmi():
    name = name_entry.get().strip()

    if not name:
        messagebox.showerror("Input Error", "Please enter your name.")
        return

    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Input Error",
                "Weight and height must be greater than zero."
            )
            return

        if weight > 1000 or height > 3:
            messagebox.showerror(
                "Input Error",
                "Please check your weight in kg and height in metres."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numbers for weight and height."
        )
        return

    bmi = weight / (height ** 2)
    category, color = classify_bmi(bmi)

    result_label.config(
        text=f"BMI: {bmi:.2f}\nCategory: {category}",
        foreground=color
    )

    try:
        save_record(name, weight, height, bmi, category)
        messagebox.showinfo(
            "Success",
            f"BMI record saved for {name}."
        )
    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not save the BMI record.\n{error}"
        )


# ---------- BMI history chart ----------

def show_history():
    name = name_entry.get().strip()

    if not name:
        messagebox.showerror(
            "Input Error",
            "Enter a user's name to view their BMI history."
        )
        return

    try:
        with sqlite3.connect(DB_NAME) as connection:
            records = connection.execute("""
                SELECT recorded_at, bmi
                FROM bmi_records
                WHERE name = ? COLLATE NOCASE
                ORDER BY recorded_at ASC, id ASC
            """, (name,)).fetchall()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not read BMI history.\n{error}"
        )
        return

    if not records:
        messagebox.showinfo(
            "No History",
            f"No BMI records found for {name}."
        )
        return

    dates = [
        datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S")
        for record in records
    ]
    bmis = [record[1] for record in records]

    chart_window = tk.Toplevel(root)
    chart_window.title(f"BMI History - {name}")
    chart_window.geometry("750x480")

    figure, axis = plt.subplots(figsize=(8, 4.5))

    axis.plot(dates, bmis, marker="o", linewidth=2)
    axis.set_title(f"BMI Trend for {name}")
    axis.set_xlabel("Recorded Date and Time")
    axis.set_ylabel("BMI")
    axis.grid(True, linestyle="--", alpha=0.5)

    figure.autofmt_xdate()
    figure.tight_layout()

    canvas = FigureCanvasTkAgg(figure, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def close_chart():
        plt.close(figure)
        chart_window.destroy()

    chart_window.protocol("WM_DELETE_WINDOW", close_chart)


# ---------- GUI ----------

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("460x490")
root.resizable(False, False)

try:
    initialize_database()
except sqlite3.Error as error:
    messagebox.showerror(
        "Database Error",
        f"Could not initialize the database.\n{error}"
    )
    root.destroy()
    raise SystemExit(1)

main_frame = ttk.Frame(root, padding=25)
main_frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(
    main_frame,
    text="BMI CALCULATOR",
    font=("Arial", 20, "bold")
).pack(pady=(0, 8))

ttk.Label(
    main_frame,
    text="Calculate your Body Mass Index",
    font=("Arial", 10)
).pack(pady=(0, 20))

ttk.Label(main_frame, text="User Name").pack(anchor="w")
name_entry = ttk.Entry(main_frame, width=35)
name_entry.pack(fill="x", pady=(4, 12))

ttk.Label(main_frame, text="Weight (kg)").pack(anchor="w")
weight_entry = ttk.Entry(main_frame, width=35)
weight_entry.pack(fill="x", pady=(4, 12))

ttk.Label(main_frame, text="Height (metres)").pack(anchor="w")
height_entry = ttk.Entry(main_frame, width=35)
height_entry.pack(fill="x", pady=(4, 18))

ttk.Button(
    main_frame,
    text="Calculate BMI & Save Record",
    command=calculate_bmi
).pack(fill="x", ipady=5)

result_label = ttk.Label(
    main_frame,
    text="Your BMI result will appear here",
    font=("Arial", 13, "bold"),
    justify="center"
)
result_label.pack(pady=20)

ttk.Button(
    main_frame,
    text="View BMI History Chart",
    command=show_history
).pack(fill="x", ipady=5)

ttk.Label(
    main_frame,
    text="BMI is a general screening measure, not a diagnosis.",
    font=("Arial", 8)
).pack(pady=(15, 0))

root.mainloop()
