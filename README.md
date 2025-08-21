# 🤖 ZenZoneBot  

ZenZoneBot is a **Flask-based AI chatbot** designed to assist users in understanding their emotional state, detecting potential mental health concerns, and providing helpful resources.  
The bot leverages **sentiment analysis, disorder keyword detection, and intent prediction** to deliver meaningful, context-aware responses.  


## ✨ Features
- 🧠 **Sentiment Analysis** – Detects user emotions (joy, fear, anger, sadness, etc.)  
- 🩺 **Disorder Keyword Detection** – Identifies potential mental health concerns  
- 🎯 **Intent Prediction** – Understands user needs (advice, resources, emotional support)  
- 🔄 **Context-Aware Conversations** – Maintains flow of interaction

## Installation

### Prerequisites
Make sure you have the following installed on your system:
- Python 3.7+
- Flask
- Joblib
- Required Python libraries

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/mondal-paushali03/ZenZoneBot.git
   cd ZenZoneBot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```

### Where to Run
After starting the Flask application, open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```
This will open the chatbot interface where you can interact with ZenZoneBot.

## Project Structure
```
ZenZoneBot/
│── templates/
│   ├── index.html
│   ├── about_us.html
│   ├── chatui.html
│── keyword1.py  # Disorder keyword matching
│── text_sum1.py # Text summarization module
│── int.py       # Intent prediction module
│── sent.py      # Sentiment analysis module
│── app.py       # Flask application
│── requirements.txt
```

## API Endpoints

### Home Page
- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Renders the home page.

### About Us Page
- **Endpoint:** `/about_us`
- **Method:** `GET`
- **Description:** Renders the About Us page.

### Chat UI
- **Endpoint:** `/chatui`
- **Method:** `GET`
- **Description:** Renders the chatbot UI.

### Process User Input
- **Endpoint:** `/process_input`
- **Method:** `POST`
- **Description:** Processes user input, detects sentiment, identifies disorder-related keywords, predicts intent, and provides appropriate responses.
- **Request Body:**
  ```json
  {
    "user_prompt": "I feel really anxious about my exams."
  }
  ```
- **Response:**
  ```json
  {
    "message": "We all face worries. What's been on your mind recently?"
  }
  ```

## Conversation Flow
1. **Sentiment Detection:** Identifies user emotions such as joy, fear, anger, sadness, etc.
2. **Disorder Detection:** Detects keywords related to mental health conditions like depression, anxiety, PTSD, ADHD, and eating disorders.
3. **Intention Detection:** Determines whether the user is expressing distress, asking for resources, or seeking advice.
4. **Confirmation Response:** Provides final reassurance and additional resources if needed.

## License
This project is licensed under the MIT License.

## Contact
For questions or suggestions, feel free to reach out at mondal.paushali384@gmail.com.

