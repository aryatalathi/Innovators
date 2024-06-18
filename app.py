# from flask import Flask, request, render_template, jsonify
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_google_genai import ChatGoogleGenerativeAI

# app = Flask(__name__)

# # Set your Generative Language API key
# gemini_api_key = "AIzaSyASANd1igp-XvBIV3Yy9UuIcmu6YPyRkHw"

# # Initialize Gemini model
# model = ChatGoogleGenerativeAI(
#     model="gemini-pro",
#     temperature=0.7,
#     top_p=0.85,
#     google_api_key=gemini_api_key,
#     convert_system_message_to_human=True
# )

# # Prompts
# questions_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are an interviewer preparing for a job interview."),
#     ("user", "Please generate a list of interview questions for the position of {post} at {company}.")
# ])

# qa_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are an interviewer and also providing sample answers for a job interview."),
#     ("user", "Please generate a list of interview questions and provide sample answers for the position of {post} at {company}.")
# ])

# # Output parser
# output_parser = StrOutputParser()

# def generate_interview_content(company, post, include_answers=False):
#     if include_answers:
#         chain = qa_prompt | model | output_parser
#     else:
#         chain = questions_prompt | model | output_parser

#     user_input = {"company": company, "post": post}
#     response = chain.invoke(user_input)
#     return response

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/generate_interview', methods=['POST'])
# def generate_interview():
#     data = request.json
#     company = data['company']
#     post = data['post']
#     include_answers = data['includeAnswers']

#     response = generate_interview_content(company, post, include_answers)
#     return jsonify({"response": response})


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
    temperature=0.7,
    top_p=0.85,
    google_api_key=gemini_api_key,
    convert_system_message_to_human=True
)

# Prompts
questions_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an interviewer preparing for a job interview."),
    ("user", "Please generate a list of interview questions for the position of {post} at {company}.")
])

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an interviewer and also providing sample answers for a job interview."),
    ("user", "Please generate a list of interview questions and provide sample answers for the position of {post} at {company}.")
])

# Output parser
output_parser = StrOutputParser()

def generate_interview_content(company, post, include_answers=False):
    if include_answers:
        chain = qa_prompt | model | output_parser
    else:
        chain = questions_prompt | model | output_parser

    user_input = {"company": company, "post": post}
    response = chain.invoke(user_input)
    
    # Split the response into lines and filter out non-question lines
    lines = response.split('\n')
    questions = [line.strip() for line in lines if line.strip().endswith('?')]
    
    return questions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_interview', methods=['POST'])
def generate_interview():
    data = request.json
    company = data['company']
    post = data['post']
    include_answers = data['includeAnswers']

    questions = generate_interview_content(company, post, include_answers)
    
    # Store questions in session
    session['questions'] = questions
    session['current_question'] = 0
    session['answers'] = {}  # Initialize answers storage

    return jsonify({"redirect_one_by_one": url_for('questions_one_by_one'), "redirect_full_list": url_for('questions_full_list')})

# @app.route('/questions_one_by_one', methods=['GET', 'POST'])
# def questions_one_by_one():
#     questions = session.get('questions', [])
#     answers = session.get('answers', {})

#     current_question = session.get('current_question', 0)
    
#     if not questions or current_question >= len(questions):
#         return redirect(url_for('index'))
    
#     question = questions[current_question]

#     if request.method == 'POST':
#         user_answer = request.form['answer']
#         answers[question] = user_answer  # Store user's answer in session
#         session['answers'] = answers  # Update session with answers
        
#         # Provide user's answer to the GPT model for feedback
#         feedback = model.ask(question, user_answer)
#         # Store or display feedback as needed
        
#         # Move to the next question
#         session['current_question'] += 1
        
#         # Check if it's the last question
#         if session['current_question'] >= len(questions):
#             return redirect(url_for('feedback'))  # Redirect to feedback page
        
#         return redirect(url_for('questions_one_by_one'))

#     return render_template('questions_one_by_one.html', question=question, total=len(questions), current=current_question + 1)

@app.route('/questions_one_by_one', methods=['GET', 'POST'])
def questions_one_by_one():
    questions = session.get('questions', [])
    answers = session.get('answers', {})

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
        # Store or display feedback as needed
        
        # Move to the next question
        session['current_question'] += 1
        
        # Check if it's the last question
        if session['current_question'] >= len(questions):
            return redirect(url_for('feedback'))  # Redirect to feedback page
        
        return redirect(url_for('questions_one_by_one'))

    return render_template('questions_one_by_one.html', question=question, total=len(questions), current=current_question + 1)


# @app.route('/feedback')
# def feedback():
#     questions = session.get('questions', [])
#     answers = session.get('answers', {})

#     if not questions or not answers:
#         return redirect(url_for('index'))

#     feedback_messages = []
#     for question in questions:
#         if question in answers:
#             user_answer = answers[question]
#             feedback = model.ask(question, user_answer)
#             feedback_messages.append(feedback)
#         else:
#             feedback_messages.append("No answer provided")  # Or handle as per your requirement

#     return render_template('feedback.html', feedback_messages=feedback_messages)

@app.route('/feedback')
def feedback():
    questions = session.get('questions', [])
    answers = session.get('answers', {})

    if not questions or not answers:
        return redirect(url_for('index'))

    feedback_messages = []
    for question in questions:
        if question in answers:
            user_answer = answers[question]
            feedback = model.ask(question, user_answer)
            feedback_messages.append(feedback)
        else:
            feedback_messages.append("No answer provided") 

    return render_template('feedback.html', feedback_messages=feedback_messages)

@app.route('/questions_full_list')
def questions_full_list():
    questions = session.get('questions', [])
    
    if not questions:
        return redirect(url_for('index'))
    
    return render_template('questions_full_list.html', questions=questions)

@app.route('/next_question', methods=['POST'])
def next_question():
    session['current_question'] = session.get('current_question', 0) + 1
    return redirect(url_for('questions_one_by_one'))

if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == '__main__':
#     app.run(debug=True)
