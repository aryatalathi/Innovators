import fitz  # PyMuPDF
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Set your Generative Language API key
gemini_api_key = "AIzaSyASANd1igp-XvBIV3Yy9UuIcmu6YPyRkHw"

# Initialize Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.5,
    #top_p=0.85,
    google_api_key=gemini_api_key,
    convert_system_message_to_human=True
)

# Prompts
questions_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an interviewer preparing for a job interview."),
    ("user", "Please generate a list of interview questions for the position of {post} at {company} based on the following resume: {resume}. Make sure questions align with the {company} interest and the {post} role based on the candidates resume. You can follow the template – "+
                         "1. First Introduction questions which align with the candidate’s resume."+
                         "2. Next come up with technical questions which should align with the {post} role. Keep the questions straight and purely technical."+
                         "3. Next Experience-Based Questions, which should be based on resume of candidate."+
                         "4. Then you can ask some {company} specific questions."+
                         "5. Lastly, give some Behavioral Questions."
    )
])

# Output parser
output_parser = StrOutputParser()

def extract_text_from_pdf(pdf_file):
    # Open the PDF file
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def generate_interview_content(company, post, resume_text):
    chain = questions_prompt | model | output_parser

    user_input = {"company": company, "post": post, "resume": resume_text}
    response = chain.invoke(user_input)
    # Log the full response for debugging
    print("Full model response:", response)

    # Split the response into lines and filter out non-question lines
    lines = response.split('\n')
    questions = [line.strip() for line in lines if (line.strip().endswith('?') | line.strip().endswith('.'))]
    # for testing truncating length of questions list
    return questions[:4]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_interview', methods=['POST'])
def generate_interview():
    company = request.form['company']
    post = request.form['post']
    resume_file = request.files['resume']

    # Extract text from the resume PDF
    resume_text = extract_text_from_pdf(resume_file)

    questions = generate_interview_content(company, post, resume_text)
    
    # Store questions in session
    session['questions'] = questions
    session['current_question'] = 0
    session['answers'] = {}  # Initialize answers storage

    return jsonify({"redirect_one_by_one": url_for('questions_one_by_one'), "redirect_full_list": url_for('questions_full_list')})

@app.route('/questions_one_by_one', methods=['GET', 'POST'])
def questions_one_by_one():
    questions = session.get('questions', [])
    answers = session.get('answers', {})
    print(questions)
    print(answers)

    current_question = session.get('current_question', 0)

    if not questions or current_question >= len(questions):
        return redirect(url_for('index'))

    question = questions[current_question]

    if request.method == 'POST':
        user_answer = request.form['answer']
        answers[question] = user_answer  # Store user's answer in session
        session['answers'] = answers  # Update session with answers
        
        # Provide user's answer to the GPT model for feedback
        feedback = model.ask(question, user_answer)

        # Store the feedback in the session or another appropriate place
        if 'feedback' not in session:
            session['feedback'] = {}
            print(feedback)
        session['feedback'][question] = feedback
        
        # Move to the next question
        session['current_question'] += 1
        
        # Check if it's the last question
        if session['current_question'] >= len(questions):
            return redirect(url_for('feedback'))  # Redirect to feedback page
        
        return redirect(url_for('questions_one_by_one'))

    return render_template('questions_one_by_one.html', question=question, total=len(questions), current=current_question + 1)

@app.route('/feedback')
def feedback():
    questions = session.get('questions', [])
    answers = session.get('answers', {})
    feedback_messages = session.get('feedback', {})

    feedback_display = []
    for question in questions:
        answer = answers.get(question, "No answer provided")
        feedback = feedback_messages.get(question, "No feedback available")
        feedback_display.append((question, answer, feedback))
    return render_template('feedback.html', feedback_messages=feedback_display)

@app.route('/questions_full_list')
def questions_full_list():
    questions = session.get('questions', [])
    
    if not questions:
        return redirect(url_for('index'))
    
    return render_template('questions_full_list.html', questions=questions)

@app.route('/next_question', methods=['POST'])
def next_question():
    session['current_question'] = session.get('current_question', 0) + 1
    user_answer = request.form['answer']
    print(user_answer)
    return redirect(url_for('questions_one_by_one'))

if __name__ == '__main__':
    app.run(debug=True)

