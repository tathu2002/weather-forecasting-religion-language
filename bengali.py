from tkinter import *
import requests
import tkinter as tk
from googletrans import Translator
from tkinter import messagebox

HEIGHT = 400
WIDTH = 800

API_KEY = 'd7842c0b970d897c608c64e6b6cc0b8a'

def fetch_weather(city_name, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error making request:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def detect_language(text):
    translator = Translator()
    detected_lang = translator.detect(text).lang
    return detected_lang

def translate_to_english(text):
    translator = Translator()
    translated_text = translator.translate(text, src='bn', dest='en')
    return translated_text.text

def translate_to_bengali(text):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='bn')
    return translated_text.text

def display_weather():
    city_name_bn = city_entry.get()

    city_name_en = translate_to_english(city_name_bn)

    weather_data = fetch_weather(city_name_en, API_KEY)
    if weather_data:
        try:
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']

            translated_description = translate_to_bengali(description)
        
            result_label.config(text=f"{city_name_bn} আবহাওয়া:\n"
                                      f"তাপমাত্রা: {temperature}°C\n"
                                      f"বর্ণনা: {translated_description}\n"
                                      f"আর্দ্রতা: {humidity}%\n"
                                      f"বায়ু বেগ: {wind_speed} m/s")
        except KeyError:
            messagebox.showerror("Error", "শহর খুঁজে পাওয়া যায়নি")
            result_label.config(text="")
    else:
        result_label.config(text="আবহাওয়া তথ্য পাওয়া যায়নি.")

root = tk.Tk()
root.title("weatherB")

background_img = PhotoImage(file="D:/projectW/pic.gif")
Label(root,image=background_img).place(relx=0,rely=0,relwidth=1,relheight=1)

icon_image = tk.PhotoImage(file="D:\projectW\weatherB- icon.png")
root.iconphoto(True, icon_image)

city_label = Label(root, text="শহরের নাম: ")
city_label.pack()

city_entry = Entry(root)
city_entry.pack()

fetch_button = Button(root, text="তথ্য প্রাপ্ত করুন", command=display_weather)
fetch_button.pack()

result_label = Label(root, text="", font=("Arial", 15), wraplength=300, justify=LEFT)
result_label.pack()

root.mainloop()
