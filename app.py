from flask import Flask, redirect, render_template, request, url_for
from PyPDF2 import PdfReader
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        file = request.files['file']
        file_results = process_file_upload(file)

        if len(file_results) > 5000:
            file_results = file_results[:5000]

        prompt = f"I am trying to summarize the following file:\n\n{file_results}\n\nMy summary is:"

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
        )

        print(file_results)
        print(completion)

        summary = completion.choices[0].message.content
        return redirect(url_for("index", result=summary))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def process_file_upload(file):
    # Open the PDF file
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
    
    return text
