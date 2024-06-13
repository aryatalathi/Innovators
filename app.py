from flask import Flask, request, render_template, jsonify
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

app = Flask(__name__)

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
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_interview', methods=['POST'])
def generate_interview():
    data = request.json
    company = data['company']
    post = data['post']
    include_answers = data['includeAnswers']

    response = generate_interview_content(company, post, include_answers)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
