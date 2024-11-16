from transformers import pipeline  # Initialize summarization pipeline
import re  # Import regex module for text processing

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

def extract_sections(file_path):
    """
    Extract contract sections using regex.
    """
    sections = {}  # Dictionary to store sections
    with open(file_path, 'r') as file:
        text = file.read()  # Read the file content
    
    # Regex pattern to capture headings and their content
    pattern = r'(?P<heading>^[A-Za-z ]+[:])\s+(?P<content>.+?)(?=\n[A-Za-z ]+:|\Z)'
    matches = re.finditer(pattern, text, re.DOTALL | re.MULTILINE)  # Find matches
    
    for match in matches:  # Store heading-content pairs
        heading = match.group("heading").strip(":")
        content = match.group("content").strip()
        sections[heading] = content
        
    return sections

def summarize_text(text, max_length=150):
    """
    Summarizes text using the summarization pipeline.
    """
    # using hugging face pipeline
    summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
    return summary[0]['summary_text']  # Return the summarized text

def summarize_contract(file_path):
    """
    Summarizes contract by section.
    """
    sections = extract_sections(file_path)  # Extract sections from contract
    
    print("Contract Summary\n" + "="*20)
    
    for heading, content in sections.items():  # Loop through sections
        print(f"Section: {heading}")
        summary = summarize_text(content)  # Summarize section content
        print("Summary:", summary)
        print("-" * 40)

# Path to your contract file
contract_file = "sample.txt"  # Specify file path
summarize_contract(contract_file)  # Call the function to summarize the contract