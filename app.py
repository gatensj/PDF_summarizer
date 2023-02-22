from flask import Flask, redirect, render_template, request, url_for
from PyPDF2 import PdfReader

import openai
import os
import io

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        file = request.files['file']
        file_results = process_file_upload(file)

        '''
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_summary_prompt(file_results),
            temperature=0.6,
            max_tokens=64,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        '''
        temp = "hello world"
        return redirect(url_for("index", result=temp))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_summary_prompt(file_results):
    return """Please provide a list of 3 bullet points that summarize this File.
File: {}
"""

def process_file_upload(file):
    # Open the PDF file
    #pdf = PdfFileReader(file.stream.read())
    pdf = PdfReader(file.stream)
 
    # Get the number of pages in the PDF
    num_pages = len(pdf.pages)
    # Initialize a variable to store the text
    text = ""
    # Iterate through each page
    for i in range(0, num_pages):
        # Get the page object
        page = pdf.pages[i]
        # Extract the text from the page
        text += page.extract_text()
    
    #text = 'Goodbye moon'
    return text