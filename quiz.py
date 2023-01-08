import main
from flask import Flask, render_template, request
import os
import openai
import json
import requests
import pydf

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        quiz_type = request.form["quiz_type"]
        num_q = request.form["number_of_questions"]
        print(quiz_type)
        # Do something with the quiz type here
        quiz = make_request(quiz_type, num_q)
        return render_template("quiz.html", quiz=quiz)
    return render_template("index.html")
         


def make_request(quiz_type, num_q):
# Make the API request
    response = requests.post(
        "https://api.openai.com/v1/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer ${{api_key}}",
    },
    json={
        "model": "text-davinci-003",
        "prompt": f"Make a {num_q} question quiz suitable for children about UK, European and USA {quiz_type} with answers",
        "max_tokens": 2049,
        "temperature": 1,
    }
)
# check server response, create python dict if all good
    if response.status_code == 200:
    # Convert the JSON response to a Python dictionary
        quiz = response.json()
        return '\n'.join(item['text'] for item in quiz['choices'])
    
    else:
        print(f"An error occurred: {response.status_code}")
        print(response.text)
        return f"An error occurred. Please try again."
    
    


if __name__ == "__main__":
    app.run(debug=True)
