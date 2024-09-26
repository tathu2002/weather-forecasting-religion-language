from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label  # Add this import
from kivy.uix.textinput import TextInput  # Add this import
from kivy.uix.button import Button  # Add this import
from kivy.network.urlrequest import UrlRequest
from googletrans import Translator
from kivy.uix.popup import Popup

class WeatherLayout(BoxLayout):
    city_entry = None
    result_label = None

    API_KEY = 'd7842c0b970d897c608c64e6b6cc0b8a'

    def fetch_weather(self, city_name, api_key):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        UrlRequest(url, on_success=self.success_callback, on_failure=self.failure_callback)

    def success_callback(self, request, result):
        try:
            temperature = result['main']['temp']
            description = result['weather'][0]['description']
            humidity = result['main']['humidity']
            wind_speed = result['wind']['speed']

            translated_description = self.translate_to_bengali(description)

            self.result_label.text = f"{self.city_entry.text} আবহাওয়া:\n" \
                                      f"তাপমাত্রা: {temperature}°C\n" \
                                      f"বর্ণনা: {translated_description}\n" \
                                      f"আর্দ্রতা: {humidity}%\n" \
                                      f"বায়ু বেগ: {wind_speed} m/s"
        except KeyError:
            self.show_error_popup("শহর খুঁজে পাওয়া যায়নি")

    def failure_callback(self, request, result):
        self.show_error_popup("আবহাওয়া তথ্য পাওয়া যায়নি")

    def detect_language(self, text):
        translator = Translator()
        detected_lang = translator.detect(text).lang
        return detected_lang

    def translate_to_english(self, text):
        translator = Translator()
        translated_text = translator.translate(text, src='bn', dest='en')
        return translated_text.text

    def translate_to_bengali(self, text):
        translator = Translator()
        translated_text = translator.translate(text, src='en', dest='bn')
        return translated_text.text

    def display_weather(self):
        city_name_bn = self.city_entry.text
        city_name_en = self.translate_to_english(city_name_bn)
        self.fetch_weather(city_name_en, self.API_KEY)

    def show_error_popup(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

class WeatherApp(App):
    def build(self):
        return WeatherLayout()

if __name__ == '__main__':
    WeatherApp().run()

