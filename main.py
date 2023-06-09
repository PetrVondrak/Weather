from tkinter import *
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import ttkbootstrap as ttk


# Nastavení okna aplikace.
window = ttk.Window(themename="morph")
window.minsize(width=600, height=300)
window.resizable(False, False)
window.title("Weather")
window.iconbitmap("icon.ico")


# Funkce pro získávání aktuálních informací o počasí z OpenWeatherMap API.
def get_weather(city):
    api_key = "da204a60696ea6b5fd647e9e913493fd"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    res = requests.get(url)

    # Pokuď město není nalezeno.
    if res.status_code == 404:
        messagebox.showerror("Weather", "City not found!")
        return None

    # Analýza JSON souborů a získávání informací o počasí.
    weather = res.json()
    weather_icon = weather["weather"][0]["icon"]
    weather_status = weather["weather"][0]["description"]
    country = weather["sys"]["country"]
    real_temp = weather["main"]["temp"] - 273.15
    feels_like = weather["main"]["feels_like"] - 273.15
    temp_min = weather["main"]["temp_min"] - 273.15
    temp_max = weather["main"]["temp_max"] - 273.15
    pressure = weather["main"]["pressure"]
    humidity = weather["main"]["humidity"]
    wind_speed = weather["wind"]["speed"]

    # Získání URL ikony a návrat všech informací o počasí.
    icons_url = f"https://openweathermap.org/img/wn/{weather_icon}@2x.png"
    return icons_url, real_temp, temp_min, temp_max, feels_like, city, country,\
        weather_status, humidity, wind_speed, pressure


# Spustí vyhledávání aktuálního počasí pro zadané město.
def search():
    city = search_label.get()
    result = get_weather(city)
    if result is None:
        return

    # Pokud je město nalezeno , rozbalí tyto informace o městě a uloží do výsledku.
    icons_url, real_temp, temp_min, temp_max, feels_like, city, country,\
        weather_status, humidity, wind_speed, pressure = result

    # Získání ikony aktuálního počasí z URL.
    image = Image.open(requests.get(icons_url, stream=True).raw)
    weather_icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=weather_icon)
    icon_label.image = weather_icon

    # Aktualizace všech údajů o počasí a jejich vypsání.
    city_label.configure(text=f"{city}, {country}")
    weather_status_label.configure(text=weather_status)
    real_temp_label.configure(text=f"Real temp: {real_temp:.1f}°C")
    feels_like_label.configure(text=f"Feels temp: {feels_like:.1f}°C")
    temp_min_label.configure(text=f"Min temp: {temp_min:.1f}°C")
    temp_max_label.configure(text=f"Max temp: {temp_max:.1f}°C")
    humidity_label.configure(text=f"Humidity: {humidity}%")
    pressure_label.configure(text=f"Pressure: {pressure} hPa")
    wind_speed_label.configure(text=f"Wind speed: {wind_speed} m/s")


# Rozmístění prvků aplikace a jejich vzhled.
# Zadání vyhledávání města.
search_label = ttk.Entry(window, font=("Calibri", 16), foreground="black", justify=CENTER,
                        bootstyle="primary")
search_label.focus()
search_label.place(x=50, y=10)

# Stylování tlačítka.
button_style = ttk.Style()
button_style.configure("warning.TButton", font=("Calibri", 14), foreground="black")

# Tlačítko pro vyhledávání města.
search_button = ttk.Button(window, text="Search weather", command=search,
                            style="warning.TButton")
search_button.place(x=380, y=12.5)

# Zvolené město.
city_label = ttk.Label(window, font=("Calibri", 20, "bold"), foreground="black")
city_label.place(x=30, y=70)

# Ikona aktuálního stavu počasí v dané lokaci.
icon_label = ttk.Label(window)
icon_label.place(x=40, y=120)

# Popis stavu počasí.
weather_status_label = ttk.Label(window, font=("Calibri", 16), foreground="black")
weather_status_label.place(x=40, y=230)

# Skutečná teplota.
real_temp_label = ttk.Label(window, font=("Calibri", 14, "bold"), foreground="black")
real_temp_label.place(x=230, y=80)

# Pocitová teplota.
feels_like_label = ttk.Label(window, font=("Calibri", 14), foreground="black")
feels_like_label.place(x=230, y=120)

# Minimální a maximální teplota.
temp_min_label = ttk.Label(window, font=("Calibri", 14), foreground="black")
temp_min_label.place(x=420, y=80)

temp_max_label = ttk.Label(window, font=("Calibri", 14), foreground="black")
temp_max_label.place(x=420, y=120)

# Rychlost větru.
wind_speed_label = ttk.Label(window, font=("Calibri", 14), foreground="black")
wind_speed_label.place(x=390, y=230)

# Tlak.
pressure_label = ttk.Label(window, font=("Calibri", 14), foreground="black")
pressure_label.place(x=390, y=170)

# Vlhkost.
humidity_label = ttk.Label(window, font=("Calibri", 14), foreground="black")
humidity_label.place(x=230, y=170)

window.mainloop()
