import fitz

def extract_from_pdf(pdf_path):
    pdf_doc = fitz.open(pdf_path)
    text = ""
    for page_number in range(len(pdf_doc)):
        page = pdf_doc[page_number]
        text += page.get_text()
    pdf_doc.close()
    return text

sample_text = extract_from_pdf("FreelanceAgreement.pdf")
print(sample_text)

import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize

sample_text = extract_from_pdf("FreelanceAgreement.pdf")
sentences = sent_tokenize(sample_text)

from transformers import pipeline
import re
def find_negative_phrases(sentence, negative_phrases):
    for phrase in negative_phrases:
        if re.search(rf'\b{re.escape(phrase)}\b', sentence, re.IGNORECASE):
            return True
    return False

negative_phrases = ["non-refundable",
    "limited liability",
    "termination without notice",
    "subject to discretion",
    "no guarantee of performance",
    "at the sole discretion"
]

sentiment_classifier = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

results = []
for sentence in sentences:
    sentiment_result = sentiment_classifier(sentence)[0]
    custom_negative = find_negative_phrases(sentence, negative_phrases)
    
    results.append({
        "text": sentence,
        "sentiment_label": sentiment_result["label"],
        "custom_negative": custom_negative
    })

# Collect "red words" based on sentiment or custom negative phrase detection
red_words = [
    res["text"] for res in results
    if res["sentiment_label"] == "NEGATIVE" or res["custom_negative"]
]

def highlight_phrases_in_pdf(input_pdf, output_pdf, phrases):
    pdf_document = fitz.open(input_pdf)
    
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        for phrase in phrases:
            text_instances = page.search_for(phrase)
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.update()
    
    pdf_document.save(output_pdf)
    pdf_document.close()

highlight_phrases_in_pdf("FreelanceAgreement.pdf", "highlighted_contract.pdf", red_words)
