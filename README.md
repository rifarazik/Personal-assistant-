# Personal Assistant Application

A desktop personal assistant application built with Python and Tkinter. This application helps you manage meetings by scheduling them, adding participants, taking text and voice notes, and generating summaries using the Hugging Face API.


## ✨ Features

* **Schedule Meetings**: Schedule new meetings with a specific title, date, and time using a calendar and time selector.
* **Add Participants**: Easily add participants to any scheduled meeting.
* **Take Text Notes**: Add written notes to your meetings to keep track of important details.
* **Take Voice Notes**: Use your microphone to dictate notes, which are automatically transcribed and saved.
* **Meeting Summarization**: Generate a concise summary of your meeting notes using a Hugging Face model.
* **Data Persistence**: All meeting data is saved to a `meetings.json` file and can be reloaded when the app starts.
* **Voice Feedback**: The assistant provides voice feedback for most actions, confirming what it's doing.
* **User-Friendly GUI**: A clean and simple graphical user interface built with Tkinter.

---

## 🛠️ Setup and Installation

Follow these steps to set up and run the project on your local machine.

### Prerequisites

* Python 3.x
* `pip` (Python package installer)
* For voice note functionality, you may need to install system-level dependencies for PyAudio:
    * **Windows**: PyAudio can be installed directly via pip.
    * **Mac**: `brew install portaudio`
    * **Linux**: `sudo apt-get install libasound-dev portaudio19-dev`

### Installation Steps

1.  **Clone the repository or download the files** to a local directory.

2.  **Create a virtual environment** (recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages** using the `requirements.txt` file:
    ```sh
    pip install -r requirements.txt
    ```

---

## ⚙️ Configuration

Before running the application, you need to configure your Hugging Face API key.

1.  Open the `assistant.py` file.
2.  Locate the following line:
    ```python
    self.huggingface_api_key = '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'  # Replace with your Hugging Face API key
    ```
3.  Replace the placeholder key with your own Hugging Face API key. If you don't have one, you can get it from the [Hugging Face website](https://huggingface.co/settings/tokens).

---

## 🚀 Usage

To run the application, execute the `main.py` script from your terminal:

```sh
python main.py
