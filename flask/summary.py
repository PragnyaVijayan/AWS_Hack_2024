from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
from transformers import pipeline
import re
import io

app = Flask(__name__)
CORS(app)  # Enable CORS to allow communication with React frontend

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_pdf(pdf_file):
    """
    Extract text from uploaded PDF.
    """
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
    all_text = ""
    for page in pdf_reader.pages:
        all_text += page.extract_text()
    return all_text

def extract_sections(text):
    """
    Extract contract sections using regex.
    """
    sections = {}
    pattern = r'(?P<heading>^[A-Za-z ]+[:])\s+(?P<content>.+?)(?=\n[A-Za-z ]+:|\Z)'
    matches = re.finditer(pattern, text, re.DOTALL | re.MULTILINE)
    for match in matches:
        heading = match.group("heading").strip(":")
        content = match.group("content").strip()
        sections[heading] = content
    return sections

def summarize_text(text, max_length=400):
    """
    Summarize text using the summarization pipeline.
    """
    summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
    return summary[0]['summary_text']

@app.route("/summarize", methods=["POST"])
def summarize_contract():
    """
    Endpoint to summarize contract.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    try:
        # Extract text from PDF
        text = extract_text_from_pdf(file)
        
        # Extract sections
        sections = extract_sections(text)
        
        # Summarize sections
        summaries = {}
        for heading, content in sections.items():
            summaries[heading] = summarize_text(content)

        return jsonify({"summaries": summaries})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5002)