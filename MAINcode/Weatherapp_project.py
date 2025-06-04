import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

# Weather icons (emoji-based)
weather_icons = {
    0: "\u2600\ufe0f Sunny",
    1: "\U0001F324\ufe0f Mostly Sunny",
    2: "\u26C5 Partly Cloudy",
    3: "\u2601\ufe0f Cloudy",
    45: "\U0001F32B\ufe0f Fog",
    48: "\U0001F32B\ufe0f Fog",
    51: "\U0001F326\ufe0f Drizzle",
    61: "\U0001F327\ufe0f Rain",
    71: "\u2744\ufe0f Snow",
    95: "\U0001F329\ufe0f Thunderstorm",
    96: "\U0001F329\ufe0f Thunderstorm"
}

# Indian states and capital cities
states = {
    "Andhra Pradesh": "Vijayawada",
    "Bihar": "Patna",
    "Delhi": "New Delhi",
    "Gujarat": "Gandhinagar",
    "Karnataka": "Bengaluru",
    "Kerala": "Thiruvananthapuram",
    "Maharashtra": "Mumbai",
    "Punjab": "Chandigarh",
    "Rajasthan": "Jaipur",
    "Tamil Nadu": "Chennai",
    "Telangana": "Hyderabad",
    "Uttar Pradesh": "Lucknow",
    "West Bengal": "Kolkata"
}

def get_weather(city):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_data = requests.get(geo_url).json()
        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_data = requests.get(weather_url).json()
        current = weather_data['current_weather']
        code = current['weathercode']
        icon = weather_icons.get(code, "\U0001F308 Weather Info")

        return f"{icon}\n\nTemperature: {current['temperature']} °C\nWind Speed: {current['windspeed']} km/h"
    except Exception as e:
        return f"Error fetching data: {e}"

# Create GUI app
app = tk.Tk()
app.title("Weather Vista - Indian States")
app.geometry("700x600")
app.configure(bg="#1e1e2e")  # Deep bluish background

# Title
title = tk.Label(app, text="\u26C5 Weather Vista \u26C5", font=("Verdana", 32, "bold"), bg="#1e1e2e", fg="#f5c542")
title.pack(pady=20)

# Logo
try:
    logo_img = Image.open("logo.png").resize((120, 120))
    logo = ImageTk.PhotoImage(logo_img)
    tk.Label(app, image=logo, bg="#1e1e2e").pack()
except:
    tk.Label(app, text="\U0001F324", font=("Helvetica", 60), bg="#1e1e2e", fg="#f5c542").pack()

# Dropdown
tk.Label(app, text="Choose an Indian State:", font=("Calibri", 16, "bold"), bg="#1e1e2e", fg="white").pack(pady=15)
state_combo = ttk.Combobox(app, values=list(states.keys()), font=("Calibri", 14), state="readonly", width=32)
state_combo.pack()
state_combo.set("Select State")

# Result frame
result_frame = tk.Frame(app, bg="#29293d", bd=2, relief="ridge")
result_frame.pack(pady=25, padx=30, fill="both", expand=True)
result_label = tk.Label(
    result_frame,
    text="\nWeather report will be shown here.\n",
    font=("Georgia", 16),
    bg="#29293d",
    fg="#ffffff",
    justify="center",
    wraplength=500
)
result_label.pack(padx=20, pady=20)

# Button
def fetch_and_display():
    selected = state_combo.get()
    if selected not in states:
        messagebox.showerror("Invalid Selection", "Please select a valid state.")
        return
    capital = states[selected]
    weather = get_weather(capital)
    result_label.config(text=f"{selected} ({capital})\n\n{weather}")

tk.Button(
    app,
    text="Get Weather Report",
    font=("Verdana", 14, "bold"),
    bg="#f5c542",
    fg="#1e1e2e",
    activebackground="#f0d000",
    command=fetch_and_display
).pack(pady=10)

# Footer
footer = tk.Label(
    app,
    text="Made with ❤️ for college project",
    font=("Arial", 10),
    bg="#1e1e2e",
    fg="#aaaaaa"
)
footer.pack(side="bottom", pady=10)

app.mainloop()
