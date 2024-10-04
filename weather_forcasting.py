import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

class WeatherForecastingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecasting App")
        self.root.geometry("500x600")  # Adjust window size

        # City input label and entry box
        self.city_label = tk.Label(root, text="City:")
        self.city_label.pack()

        self.city_entry = tk.Entry(root)
        self.city_entry.pack()

        # Button to get the forecast
        self.forecast_button = tk.Button(root, text="Get Forecast", command=self.get_forecast)
        self.forecast_button.pack()

        # Dropdown to select forecast type (Daily/Weekly/Custom)
        self.forecast_type_label = tk.Label(root, text="Select Forecast Type:")
        self.forecast_type_label.pack()

        self.forecast_type_var = tk.StringVar()
        self.forecast_type_var.set("Daily")  # Default forecast type
        self.forecast_type_menu = ttk.Combobox(root, values=["Daily", "Weekly", "Custom"], textvariable=self.forecast_type_var)
        self.forecast_type_menu.pack()

        # Custom duration selection for forecasting (for Custom type)
        self.custom_duration_label = tk.Label(root, text="Custom Duration (days):")
        self.custom_duration_label.pack()

        self.custom_duration_spinbox = tk.Spinbox(root, from_=1, to=14, width=5)
        self.custom_duration_spinbox.pack()

        # Temperature Unit Conversion (Celsius or Fahrenheit)
        self.temp_unit_label = tk.Label(root, text="Select Temperature Unit:")
        self.temp_unit_label.pack()

        self.temp_unit_var = tk.StringVar()
        self.temp_unit_var.set("Celsius")  # Default unit
        self.temp_unit_menu = ttk.Combobox(root, values=["Celsius", "Fahrenheit"], textvariable=self.temp_unit_var)
        self.temp_unit_menu.pack()

        # Buttons for historical data management
        self.historical_button = tk.Button(root, text="View Historical Data", command=self.view_historical_data)
        self.historical_button.pack()

        self.save_button = tk.Button(root, text="Save Historical Data", command=self.save_historical_data)
        self.save_button.pack()

        self.load_button = tk.Button(root, text="Load Historical Data", command=self.load_historical_data)
        self.load_button.pack()

        self.clear_button = tk.Button(root, text="Clear Historical Data", command=self.clear_historical_data)
        self.clear_button.pack()

        # Matplotlib figure and canvas for plotting data
        self.figure, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()

        # Initialize history log for tracking forecasts
        self.history_log = []

    def get_real_weather(self, city):
        """
        Generates random weather data based on the forecast type (Daily/Weekly/Custom).
        Includes extreme weather events like heatwaves and storms.
        """
        forecast_type = self.forecast_type_var.get()

        if forecast_type == "Daily":
            # Daily forecast (single-day weather)
            return {
                "city": city,
                "temperature": round(random.uniform(-10, 35), 2),  # Random temperature in Celsius
                "condition": random.choice(["Clear", "Cloudy", "Rainy", "Stormy", "Heatwave", "Snowy"])
            }

        elif forecast_type == "Weekly":
            # Weekly forecast (7 days)
            return {
                "city": city,
                "temperature": [round(random.uniform(-10, 35), 2) for _ in range(7)],
                "condition": [random.choice(["Clear", "Cloudy", "Rainy", "Stormy", "Heatwave", "Snowy"]) for _ in range(7)]
            }

        elif forecast_type == "Custom":
            # Custom forecast (user-defined duration)
            duration = int(self.custom_duration_spinbox.get())
            return {
                "city": city,
                "temperature": [round(random.uniform(-10, 35), 2) for _ in range(duration)],
                "condition": [random.choice(["Clear", "Cloudy", "Rainy", "Stormy", "Heatwave", "Snowy"]) for _ in range(duration)]
            }

    def convert_temperature(self, temperature):
        """
        Converts temperature between Celsius and Fahrenheit.
        """
        if self.temp_unit_var.get() == "Fahrenheit":
            if isinstance(temperature, list):
                return [round(temp * 9 / 5 + 32, 2) for temp in temperature]
            else:
                return round(temperature * 9 / 5 + 32, 2)
        return temperature  # Return unchanged if in Celsius

    def display_forecast(self):
        """
        Displays the forecast and plots the data using Matplotlib.
        """
        forecast_type = self.forecast_type_var.get()
        self.weather_data['temperature'] = self.convert_temperature(self.weather_data['temperature'])

        if forecast_type == "Daily":
            messagebox.showinfo(
                "Weather Forecast",
                f"Weather in {self.weather_data['city']}:\n"
                f"Temperature: {self.weather_data['temperature']}°{self.temp_unit_var.get()[0]}\n"
                f"Condition: {self.weather_data['condition']}"
            )
        elif forecast_type in ["Weekly", "Custom"]:
            duration = 7 if forecast_type == "Weekly" else len(self.weather_data['temperature'])
            messagebox.showinfo(
                "Weather Forecast",
                f"{forecast_type} Weather Forecast for {self.weather_data['city']}:\n"
                f"Temperature: {', '.join(map(str, self.weather_data['temperature']))}°{self.temp_unit_var.get()[0]}\n"
                f"Conditions: {', '.join(self.weather_data['condition'])}"
            )

        # Clear previous plot and plot the new data
        self.ax.clear()
        if forecast_type == "Daily":
            self.ax.bar(["Temperature"], [self.weather_data['temperature']], color='blue')
        else:
            days = range(1, len(self.weather_data['temperature']) + 1)
            self.ax.plot(days, self.weather_data['temperature'], marker='o', linestyle='-', color='blue')
            self.ax.set_xticks(days)

        self.ax.set_title(f"{forecast_type} Temperature Forecast")
        self.ax.set_xlabel("Days")
        self.ax.set_ylabel(f"Temperature (°{self.temp_unit_var.get()[0]})")
        self.canvas.draw()

        # Add current forecast to the history log
        self.history_log.append(self.weather_data.copy())

    def view_historical_data(self):
        """
        Displays a detailed window showing the forecast history log for all cities.
        """
        if not self.history_log:
            messagebox.showinfo("Historical Data", "No historical data available.")
            return

        # Create a new window to show historical data
        history_window = tk.Toplevel(self.root)
        history_window.title("Historical Data")
        history_window.geometry("400x300")

        # Listbox to display historical forecasts
        history_listbox = tk.Listbox(history_window, width=50, height=15)
        history_listbox.pack()

        # Add history logs to the listbox
        for entry in self.history_log:
            history_listbox.insert(tk.END, f"{entry['city']}: {entry['temperature']}°{self.temp_unit_var.get()[0]} - {entry['condition']}")

    def save_historical_data(self):
        """
        Saves the historical data log to a JSON file.
        """
        if not self.history_log:
            messagebox.showinfo("Save Data", "No historical data to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    json.dump(self.history_log, file)
                messagebox.showinfo("Save Data", f"Historical data saved to {file_path}.")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def load_historical_data(self):
        """
        Loads historical data from a JSON file.
        """
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.history_log = json.load(file)
                messagebox.showinfo("Load Data", f"Historical data loaded from {file_path}.")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading file: {str(e)}")

    def clear_historical_data(self):
        """
        Clears the historical data log.
        """
        self.history_log = []
        messagebox.showinfo("Clear Data", "Historical data cleared.")

    def get_forecast(self):
        """
        Retrieves and displays the weather forecast for the entered city.
        """
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city.")
            return

        # Retrieve fake weather data based on the city and forecast type
        self.weather_data = self.get_real_weather(city)

        # Display the forecast and plot the graph
        self.display_forecast()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherForecastingApp(root)
    root.mainloop()
