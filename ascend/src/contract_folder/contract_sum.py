from transformers import pipeline  # Initialize summarization pipeline
import re  # Import regex module for text processing
import PyPDF2

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
def extract_pdf(file_path):
  with open(file_path, 'rb') as file:
      pdf = PyPDF2.PdfReader(file)
      num_pages = len(pdf.pages)
      all_text = ""
      for page_num in range(num_pages):
          page = pdf.pages[page_num]
          text = page.extract_text()
          #print(text)
          # Clean text: remove newlines and extra spaces
          clean = re.sub(r'\s+', ' ', text).strip()
            
          all_text += clean + " "  # Add a space between pages

      return all_text
    
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

def price_extract(text):
    # Regex to find prices (e.g., $1000, €500, etc.)
    pattern = r'\b(?:\$|€|£|\b\d{1,3}(?:,\d{3})*)(?:\.\d{2})?\b'
    prices = re.findall(pattern, text)
    
    # Return the first found price or "Not found" if none is found
    return prices[1]
  
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
        price = price_extract(content)
        print("Price:", price)

# Path to your contract file
contract_file = "sample.txt"  # Specify file path
summarize_contract(contract_file)  # Call the function to summarize the contract