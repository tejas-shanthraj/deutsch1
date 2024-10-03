# Pronunciation Application

## Overview
The **Pronunciation Application** is a web-based tool built using the Django framework, designed to help users practice and improve their pronunciation in various languages. It leverages cutting-edge technology such as **Microsoft Azure's Pronunciation Assessment**, **OpenAI's ChatGPT 3.5 Turbo**, and **Groq's LLAMA Model** to provide an interactive and immersive learning experience.

### Features
- **Speech-to-Text Pronunciation Analysis**: Users can record their speech, and the application evaluates pronunciation accuracy using **Microsoft Azure's Pronunciation Assessment API**.
- **AI Assistance for Language Learning**: The application offers language learning support through **OpenAI's ChatGPT 3.5 Turbo**, which interacts with users and provides feedback on pronunciation.
- **Real-Time Feedback and Grading**: Scores pronunciation based on fluency, accuracy, and tone, helping users to identify areas of improvement.
- **Multilingual Support**: Utilizes **Groq's LLAMA Model** to create a platform for interacting and learning daily conversations.

## Technologies Used
- **Django Framework**: Backend framework for building the web application and API endpoints.
- **Microsoft Azure's Pronunciation Assessment**: Evaluates the user's speech input for accuracy and provides detailed feedback.
- **OpenAI's ChatGPT 3.5 Turbo**: Provides interactive and conversational support to guide the learning process.
- **Groq's LLAMA Model**: A machine learning model for advanced language processing and multilingual support.

## Prerequisites
Before you start, ensure you have the following installed on your system:
- Python 3.8 or higher
- Django 3.2 or higher
- Microsoft Azure SDK (`azure-cognitiveservices-speech`)
- OpenAI SDK (`openai`)
- Groq's LLAMA SDK

### Environment Variables
You will need to set up the following environment variables:

| Variable Name                | Description                            |
|------------------------------|----------------------------------------|
| `AZURE_SPEECH_KEY`           | Azure Speech API key                   |
| `AZURE_SPEECH_REGION`        | Azure region for the Speech API        |
| `PERSONAL_KEY`               | API key for OpenAI ChatGPT             |
| `ASSISTANT_ID_EN`            | Assistant ID for support               |
| `GROQ_API_KEY`               | API key for Groq LLAMA model           |
| `DJANGO_SECRET_KEY`          | Django's secret key                    |
| `DEBUG`                      | Debug mode (`True` or `False`)         |

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/tejas-shanthraj/deutsch1.git
    cd deutsch1
    ```

2. **Create and Activate a Virtual Environment**:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:  
   Create a `.env` file in the project root and add your credentials:
    ```bash
    AZURE_SPEECH_KEY=your_azure_speech_key
    AZURE_SPEECH_REGION=your_azure_speech_region
    PERSONAL_KEY=your_openai_key
    ASSISTANT_ID_EN=your_assistant_id
    GROQ_API_KEY=your_groq_api_key
    DJANGO_SECRET_KEY=your_django_secret_key
    DEBUG=True
    ```

5. **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Start the Server**:
    ```bash
    python manage.py runserver
    ```

7. **Open the Application**:  
   Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the Pronunciation Application.

## Usage
1. **Navigate to the Practice Page**:
   - Choose a language or word set to practice.
   - Click the microphone button to start recording.
  
2. **Receive Feedback**:
   - View the detailed feedback on pronunciation accuracy.
   - Use the AI chat feature to ask questions or seek guidance.

3. **Track Progress**:
   - Save your scores and track your progress over time.

## Contribution Guidelines
If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes. Make sure to follow the coding standards and provide appropriate documentation.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
