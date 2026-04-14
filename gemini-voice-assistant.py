import os
import time
import datetime
import smtplib
import webbrowser
from email.message import EmailMessage

import speech_recognition as sr
from google import genai
import wikipedia
import pyjokes
import pygame
from gtts import gTTS

# Initialize the Gemini client 

client = genai.Client(api_key="YOUR_API_KEY_HERE")

# Hook up Brave browser
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))

# Init audio mixer for TTS
pygame.mixer.init()

def speak(text):
    """Converts text to speech and plays it immediately."""
    print(f"AI: {text}")
    tts = gTTS(text=text, lang='en')
    filename = "voice_response.mp3"
    tts.save(filename)
    
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    pygame.mixer.music.unload()
    time.sleep(0.2) 
    
    # Clean up the audio file so they don't pile up
    try:
        os.remove(filename)
    except PermissionError:
        pass 

def send_email(receiver, subject, message):
    """Sends a basic email using Gmail SMTP."""
    sender_email = "YOUR GMAIL ADDRESS"
    app_password = "YOUR_APP_PASSWORD" 
    
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        print(f"Email error: {e}")
        speak("I ran into an issue and couldn't send the email.")

def open_local_file(command_text):
    """Maps spoken commands to local file paths."""
    file_map = {
        "mountain climber project": r"C:\Users\YourName\Documents\IoT_Mountain_Climber_Project.pdf",
        "raspberry pi code": r"C:\Users\YourName\Desktop\pi_script.py",
        "sppu study materials": r"C:\Users\YourName\Documents\SPPU_Fiber_Optics.pdf",
        "kitten diet plan": r"C:\Users\YourName\Documents\raw_chicken_head_schedule.txt",
        "need for speed": r"C:\Games\nfsmw12\Need for Speed Most Wanted Limited Edition"
    }
    
    for key, path in file_map.items():
        if key in command_text:
            try:
                os.startfile(path)
                speak(f"Opening {key}")
                return True
            except FileNotFoundError:
                speak("I couldn't find that file. Did it get moved?")
                return True
    return False

def take_note(text):
    """Saves a timestamped text file in an AI_Notes directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(script_dir, "AI_Notes")
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"note_{timestamp}.txt"
    filepath = os.path.join(save_dir, filename)
    
    with open(filepath, "w") as f:
        f.write(text)
        
    speak("Note saved in your AI Notes folder.")

def listen():
    """Listens to the mic and returns the spoken text as a lowercase string."""
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        listener.pause_threshold = 1
        listener.adjust_for_ambient_noise(source, duration=1) 
        try:
            voice = listener.listen(source, timeout=5, phrase_time_limit=10)
            command = listener.recognize_google(voice).lower()
            print(f"You said: {command}")
            return command
        except Exception:
            return "none"

if __name__ == "__main__":
    # Figure out the time of day for the greeting
    hour = datetime.datetime.now().hour
    if hour < 12:
        greeting = "Good Morning"
    elif hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
        
    speak(f"{greeting}. I am online and ready.")
    
    # Spin up the Gemini chat session so it remembers context
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": "You are a highly intelligent, sharp, and helpful AI assistant. Give very natural, conversational, and short answers (1-2 sentences). Since you are speaking out loud, never use asterisks, emojis, or bullet points."
        }
    )
    
    # Main listening loop
    while True:
        command = listen()

        if command == "none":
            continue
            
        # 1. YouTube
        if 'play' in command and 'on youtube' in command:
            song = command.replace('play', '').replace('on youtube', '').strip()
            speak(f"Opening Brave to play {song}")
            url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"
            webbrowser.get('brave').open(url)

        # 2. Email
        elif 'send an email' in command:
            speak("Who should I send it to? Please type the email address in the terminal.")
            receiver_address = input("Type email here: ") 
            
            speak("What is the subject?")
            subject = listen()
            
            speak("What should the email say?")
            body = listen()
            
            speak("Sending your message now.")
            send_email(receiver_address, subject, body)

        # 3. Local Files
        elif 'open' in command and any(word in command for word in ['file', 'project', 'materials', 'plan', 'resume']):
            success = open_local_file(command)
            if not success:
                speak("I don't have that file mapped in my database.")

        # 4. Wikipedia
        elif 'wikipedia' in command:
            speak('Searching Wikipedia...')
            search_query = command.replace("wikipedia", "").strip()
            try:
                results = wikipedia.summary(search_query, sentences=2)
                speak("According to Wikipedia:")
                speak(results)
            except wikipedia.exceptions.DisambiguationError:
                speak("That topic is a bit too broad. Could you be more specific?")
            except wikipedia.exceptions.PageError:
                speak("I couldn't find a Wikipedia page for that.")

        # 5. Time & Date
        elif 'the time' in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")
            
        elif 'the date' in command:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today's date is {current_date}")

        # 6. Jokes
        elif 'joke' in command:
            speak(pyjokes.get_joke())

        # 7. Note Taking
        elif 'take a note' in command or 'write this down' in command:
            speak("What should I write down?")
            note_content = listen()
            if note_content != "none":
                take_note(note_content)
            else:
                speak("I didn't catch that. Canceling note.")

        # 8. Shutdown
        elif 'go to sleep' in command or 'exit' in command:
            speak("Goodbye!")
            break 
            
        # 9. General Conversation (Gemini API)
        else:
            print("Thinking...")
            try:
                response = chat.send_message(command)
                if response.text:
                    speak(response.text)
                else:
                    speak("My bad, I drew a blank. Try again?")
                    
            except Exception as e:
                if "503" in str(e):
                    print("Servers busy, retrying...")
                    time.sleep(3)
                    speak("The servers are a bit crowded right now. Give me a second and try again.")
                else:
                    print(f"API Error: {e}")
                    speak("I lost connection to the main brain. Check the terminal.")
