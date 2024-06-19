# Innovators

#### Pre-requisites for this project to run is Python installed on your PC

## Description

This web application generates interview questions and feedback based on a candidate's resume, job description, and company applying for. It utilizes Google's Generative AI through the LangChain library to create relevant and customized interview questions. The application also provides feedback on answers given to the interview questions, helping interviewers to assess candidates effectively.

## Features

- PDF text extraction from resumes.
- Generation of interview questions tailored to the job position and company.
- One-by-one question presentation with a feedback mechanism.
- Full list display of generated interview questions.
- Secure file handling with secure_filename from Werkzeug.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/aryatalathi/Innovators.git
   cd interview-question-generator
   ```
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```
4. Install the required dependencies:
  ```
  pip install -r requirements.txt
   ```
## Usage

1. Start the Flask application:
   ```
    python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. Follow the on-screen instructions to upload a resume and generate interview questions.

## Configuration

- Set your Google Generative Language API key in the application code. It is recommended to use environment variables or a configuration file for this purpose.

## Security Note

The application code contains an API key in plain text, which is a security risk. Always keep API keys secret and do not include them in your source code. Use environment variables or a configuration file that is not checked into version control to manage your API keys and other sensitive information.

[//]: # (## License)

[//]: # ()
[//]: # (Include information about the license under which the project is made available.)
