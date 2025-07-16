import json
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
import requests
import speech_recognition as sr
from tkcalendar import DateEntry
import pyttsx3

class PersonalAssistant:
    def __init__(self):
        self.meetings = []
        self.load_meetings()  # Load meetings at startup
        self.huggingface_api_key = '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'  # Replace with your Hugging Face API key
        self.engine = pyttsx3.init()  # Initialize the text-to-speech engine
        self.engine.setProperty('rate', 150)  # Set speech rate
        self.engine.setProperty('volume', 1)  # Set volume level (0.0 to 1.0)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()  # Wait for the speech to finish

    def schedule_meeting(self, title, date_time):
        meeting = {
            'title': title,
            'date_time': date_time,
            'participants': [],
            'notes': f"Meeting '{title}' scheduled on {date_time}.\n"
        }
        self.meetings.append(meeting)
        self.save_meetings()
        messagebox.showinfo("Meeting Scheduled", f'Meeting scheduled: {title} at {date_time}')
        self.speak(f'Meeting scheduled: {title} at {date_time}')

    def add_participant(self, meeting_title, participant):
        meeting_title = meeting_title.strip().lower()
        for meeting in self.meetings:
            if meeting['title'] == meeting_title:
                meeting['participants'].append(participant)
                self.save_meetings()
                messagebox.showinfo("Participant Added", f'Participant {participant} added to meeting: {meeting_title}')
                self.speak(f'Participant {participant} added to meeting: {meeting_title}')
                return
        messagebox.showwarning("Meeting Not Found", f'Meeting {meeting_title} not found.')
        self.speak(f'Meeting {meeting_title} not found.')

    def take_notes(self, meeting_title, notes):
        for meeting in self.meetings:
            if meeting['title'] == meeting_title:
                meeting['notes'] += notes + '\n'
                self.save_meetings()
                messagebox.showinfo("Notes Added", f'Notes added to meeting: {meeting_title}')
                self.speak(f'Notes added to meeting: {meeting_title}')
                return
        messagebox.showwarning("Meeting Not Found", f'Meeting {meeting_title} not found.')
        self.speak(f'Meeting {meeting_title} not found.')

    def generate_summary_with_huggingface(self, meeting_title):
        meeting_title = meeting_title.strio().lower()
        for meeting in self.meetings:
            if meeting['title'] == meeting_title:
                notes = meeting['notes']
                summary = self.call_huggingface_api(notes)
                if summary:
                    return summary
                else:
                    return "No summary could be generated."
        return "Meeting not found."

    def call_huggingface_api(self, notes):
        api_url = "https://api-inference.huggingface.co/models/personal_assistant"
        headers = {
            "Authorization": f"Bearer {self.huggingface_api_key}",
            "Content-Type": "application/json"
        }
        data = {"inputs": notes}

        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()[0]['summary_text']
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None  # Changed to return None on error

    def save_meetings(self, filename='meetings.json'):
        with open(filename, 'w') as f:
            json.dump(self.meetings, f)

    def load_meetings(self, filename='meetings.json'):
        try:
            with open(filename, 'r') as f:
                self.meetings = json.load(f)
        except FileNotFoundError:
            self.meetings = []

    def take_voice_notes(self, meeting_title):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            messagebox.showinfo("Listening", "Please speak your notes...")
            self.speak("Please speak your notes...")
            audio = recognizer.listen(source)
            try:
                notes = recognizer.recognize_google(audio)
                self.take_notes(meeting_title, notes)
                return notes
            except sr.UnknownValueError:
                messagebox.showwarning("Audio Error", "Could not understand audio.")
                self.speak("Could not understand audio.")
                return ""
            except sr.RequestError:
                messagebox.showwarning("Request Error", "Could not request results from the speech recognition service.")
                self.speak("Could not request results from the speech recognition service.")
                return ""

class PersonalAssistantApp:
    def __init__(self, root):
        self.assistant = PersonalAssistant()

        self.root = root
        self.root.title("Personal Assistant")
        self.root.geometry("500x600")
        self.root.configure(bg="#e8f0fe")

        # Center Frame
        center_frame = ttk.Frame(root, padding="10", style="TFrame")
        center_frame.pack(expand=True)

        # Title Label
        title_label = ttk.Label(center_frame, text="Personal Assistant", font=("Helvetica", 24, 'bold'), background="#e8f0fe", foreground="#333333")
        title_label.pack(pady=10)

        # Welcome message
        self.speak_welcome_message()

        # Button Frame
        button_frame = ttk.Frame(center_frame, padding="10", relief="groove")
        button_frame.pack(pady=20, fill='x')

        # Buttons with customized styles
        button_style = ttk.Style()
        button_style.configure("TButton", padding=6, relief="flat", background="#4a90e2", foreground="#333333", font=("Arial", 12, 'bold'))
        button_style.map("TButton", background=[("active", "#0056b3")], foreground=[("active", "#FFFFFF")])

        # Buttons
        ttk.Button(button_frame, text="Schedule Meeting", command=self.schedule_meeting, width=20, style="TButton").grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="Add Participant", command=self.add_participant, width=20, style="TButton").grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(button_frame, text="Take Notes", command=self.take_notes, width=20, style="TButton").grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="Summarize Meeting", command=self.summarize_meeting, width=20, style="TButton").grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(button_frame, text="Voice Note", command=self.voice_note, width=20, style="TButton").grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="Save Meetings", command=self.save_meetings, width=20, style="TButton").grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(button_frame, text="Load Meetings", command=self.load_meetings, width=20, style="TButton").grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="Exit", command=root.quit, width=20, style="TButton").grid(row=3, column=1, padx=10, pady=10)

        # Calendar for scheduling meetings
        self.calendar_frame = ttk.Frame(center_frame)
        self.calendar_frame.pack(pady=10)
        self.calendar = DateEntry(self.calendar_frame, width=12, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.calendar.grid(row=0, column=0, padx=10, pady=10)

        self.time_entry = ttk.Combobox(self.calendar_frame, values=[f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in (0, 30)],
                                        width=10)
        self.time_entry.grid(row=0, column=1, padx=10, pady=10)
        self.time_entry.set("Select Time")

    def speak_welcome_message(self):
        welcome_message = "Welcome to your Personal Assistant! How can I help you today?"
        self.assistant.speak(welcome_message)

    def schedule_meeting(self):
        title = simpledialog.askstring("Input", "Enter meeting title:")
        self.assistant.speak("Enter meeting title:")
        date_time = f"{self.calendar.get()} {self.time_entry.get()}"
        if title and self.time_entry.get() != "Select Time":
            try:
                datetime.strptime(date_time, '%Y-%m-%d %H:%M')  # Validate datetime format
                self.assistant.schedule_meeting(title, date_time)
            except ValueError:
                messagebox.showerror("Invalid Date Format", "Please enter the date in the correct format.")
                self.assistant.speak("Invalid date format. Please enter the date in the correct format.")

    def add_participant(self):
        meeting_title = simpledialog.askstring("Input", "Enter meeting title:")
        self.assistant.speak("Enter meeting title:")
        participant = simpledialog.askstring("Input", "Enter participant name:")
        self.assistant.speak("Enter participant name:")
        if meeting_title and participant:
            self.assistant.add_participant(meeting_title, participant)

    def take_notes(self):
        meeting_title = simpledialog.askstring("Input", "Enter meeting title:")
        self.assistant.speak("Enter meeting title:")
        notes = simpledialog.askstring("Input", "Enter your notes:")
        self.assistant.speak("Enter your notes:")
        if meeting_title and notes:
            self.assistant.take_notes(meeting_title, notes)

    def voice_note(self):
        meeting_title = simpledialog.askstring("Input", "Enter meeting title:")
        self.assistant.speak("Enter meeting title:")
        if meeting_title:
            self.assistant.take_voice_notes(meeting_title)

    def summarize_meeting(self):
        meeting_title = simpledialog.askstring("Input", "Enter meeting title:")
        self.assistant.speak("Enter meeting title:")
        summary = self.assistant.generate_summary_with_huggingface(meeting_title)
        if summary:
            messagebox.showinfo("Meeting Summary", summary)
            self.assistant.speak(summary)
        else:
            messagebox.showwarning("Meeting Not Found", f'Meeting {meeting_title} not found.')
            self.assistant.speak(f'Meeting {meeting_title} not found.')

    def save_meetings(self):
        self.assistant.save_meetings()
        self.assistant.speak("Meetings saved successfully.")

    def load_meetings(self):
        self.assistant.load_meetings()
        self.assistant.speak("Meetings loaded successfully.")

def main():
    root = tk.Tk()
    app = PersonalAssistantApp(root)
    root.mainloop()

if __name__ == "__main__":
     main()