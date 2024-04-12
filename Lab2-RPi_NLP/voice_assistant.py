import lgpio
import speech_recognition as sr
import pyttsx3
import openai

# Initializing pyttsx3
listening = True
engine = pyttsx3.init()

# Set your openai api key and customize the chatgpt role
openai.api_key = "ABC"
messages = [{"role": "system", "content": "Your name is Tom and give answers in 2 lines"}]

# Customizing the output voice
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')

# Define the GPIO pin number for the relay
RELAY_GPIO_PIN = 18

# Initialize the GPIO
h = lgpio.gpiochip_open(4)

# Set up GPIO pin as output for the relay
lgpio.gpio_claim_output(h, RELAY_GPIO_PIN)

def get_response(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

def turn_on_light():
    lgpio.gpio_write(h, RELAY_GPIO_PIN, 1)
    print("Light turned ON")

def turn_off_light():
    lgpio.gpio_write(h, RELAY_GPIO_PIN, 0)
    print("Light turned OFF")

while listening:
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 3000

        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5.0)
            response = recognizer.recognize_google(audio)
            print(response)

            if "tom" in response.lower():
           
                response_from_openai = get_response(response)
                engine.setProperty('rate', 120)
                engine.setProperty('volume', volume)
                engine.setProperty('voice', 'greek')
                engine.say(response_from_openai)
                engine.runAndWait()
            
            elif "turn on the light" in response.lower():
                turn_on_light()

            elif "turn off the light" in response.lower():
                turn_off_light()
                
            else:
                print("Didn't recognize 'turn on the light' or 'turn off the light'.")

        except sr.UnknownValueError:
            print("Didn't recognize anything.")

# Clean up GPIO on exit
lgpio.gpiochip_close(h)
print("GPIO cleanup completed")
