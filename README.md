# Weather Forecasting App

## Overview
The Weather Forecasting App is a simple graphical user interface (GUI) application built using Python's Tkinter library. It allows users to input a city and receive random weather forecasts for that location. The app provides options for daily, weekly, and custom duration forecasts, with features for viewing, saving, loading, and clearing historical weather data.

## Features
- **City Input**: Enter the name of a city to get a weather forecast.
- **Forecast Types**: Choose from daily, weekly, or custom duration forecasts.
- **Temperature Unit Conversion**: Display temperatures in Celsius or Fahrenheit.
- **Random Weather Conditions**: Simulate various weather conditions including clear, cloudy, rainy, stormy, heatwave, and snowy.
- **Historical Data Management**: 
  - View historical forecast data in a separate window.
  - Save historical data to a JSON file.
  - Load historical data from a JSON file.
  - Clear historical data.
- **Graphical Representation**: Visualize forecast temperatures using Matplotlib.

## Requirements
- Python 3.x
- Tkinter (usually comes pre-installed with Python)
- Matplotlib
- JSON (part of the Python standard library)

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/WeatherForecastingApp.git
Change to the project directory:

bash
Copy code
cd WeatherForecastingApp
Install required packages (if necessary):

bash
Copy code
pip install matplotlib
Usage
Run the application:

bash
Copy code
python weather_forecasting_app.py
In the application:

Enter the name of the city in the input field.
Select the forecast type (Daily, Weekly, or Custom).
If Custom is selected, specify the duration in days.
Choose the temperature unit (Celsius or Fahrenheit).
Click the "Get Forecast" button to see the forecast.
Use the historical data management buttons to view, save, load, or clear historical data.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Tkinter documentation for GUI components.
Matplotlib documentation for plotting functionality.
