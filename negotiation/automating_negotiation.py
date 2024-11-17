import os
import base64
import boto3
import json
import re
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
import torch
import warnings
from sklearn.metrics.pairwise import cosine_similarity

# Silence unnecessary outputs
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

# Set up constants
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
S3_BUCKET_NAME = "inrixhack2024"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # Example model for embeddings
TOKEN_FILE = "token.json"  # Path to your Gmail API token
CREDENTIALS_FILE = "credentials.json"  # Path to your Gmail API credentials

# Initialize AWS S3
s3 = boto3.client(
    's3',
    aws_access_key_id={os.getenv('AWS_ACCESS_KEY')},
    aws_secret_access_key={os.getenv('AWS_SECRET_ACCESS_KEY')},
    region_name='us-west-2'
)

# Function to authenticate Gmail
def authenticate_gmail():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise Exception("Missing 'credentials.json'. Please set up Gmail API credentials.")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES, redirect_uri='http://localhost:53909/')
            creds = flow.run_local_server(port=53909) 
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

# Function to get all emails (unread and read)
def get_all_emails(service):
    try:
        results = service.users().messages().list(userId='me', q="").execute()  # Empty query to fetch all emails
        messages = results.get('messages', [])
        all_emails = []

        if not messages:
            return []

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg['payload']
            headers = payload['headers']
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
            sender = next((header['value'] for header in headers if header['name'] == 'From'), None)
            body = get_email_body(payload)
            is_unread = 'UNREAD' in msg['labelIds']
            all_emails.append({'id': msg['id'], 'subject': subject, 'sender': sender, 'body': body, 'threadId': msg['threadId'], 'is_unread': is_unread})

        return all_emails

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

# Function to parse email body
def get_email_body(payload):
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
    elif 'body' in payload:
        return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    return ""

# Function to clean the email body
def clean_email_body(text):
    text = re.sub(r'http[s]?://\S+', '', text)  # Remove all HTTP URLs
    text = re.sub(r'mailto:\S+', '', text)  # Remove mailto links
    text = text.replace('\n', ' ').replace('\r', ' ')  # Replace newline chars with a space
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^\w\s,.!?]', '', text)  # Remove non-word characters except punctuation
    return text.strip()

# Function to save the conversation to S3 (only saving read emails)
def save_conversation_to_s3(conversation, thread_id, is_unread=False):
    key = f"emails/{thread_id}.json"
    
    try:
        # Try to retrieve the existing conversation from S3
        existing_conversation = s3.get_object(Bucket=S3_BUCKET_NAME, Key=key)
        existing_data = json.loads(existing_conversation['Body'].read())
        
        # Check if the 'emails' key exists; if not, initialize it
        if 'emails' not in existing_data:
            existing_data['emails'] = []
        
        # Append the new email to the existing conversation
        existing_data['emails'].extend(conversation)
        
        # Update the object in S3
        s3.put_object(Bucket=S3_BUCKET_NAME, Key=key, Body=json.dumps(existing_data))
    
    except s3.exceptions.ClientError as e:
        # If the file doesn't exist or any other S3 error occurs, create a new one
        if e.response['Error']['Code'] == 'NoSuchKey':
            s3.put_object(Bucket=S3_BUCKET_NAME, Key=key, Body=json.dumps({'emails': conversation}))
        else:
            raise e  # Reraise unexpected errors

# Function to generate embeddings
def generate_embeddings(texts, model, tokenizer):
    inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True)
    embeddings = model(**inputs).last_hidden_state.mean(dim=1).detach().tolist()
    return embeddings

# Function to calculate cosine similarity between embeddings
def calculate_cosine_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

# Function to find the most similar past email to the new email based on sender
def find_most_similar_email(new_email, past_emails, model, tokenizer):
    sender = new_email['sender']
    new_email_body = new_email['body']
    embeddings = generate_embeddings([new_email_body], model, tokenizer)
    max_similarity = -1
    most_similar_email = None

    for email in past_emails:
        if email['sender'] == sender:
            past_email_body = email['body']
            past_embedding = generate_embeddings([past_email_body], model, tokenizer)
            similarity = calculate_cosine_similarity(embeddings[0], past_embedding[0])

            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_email = email

    return most_similar_email

# Function to generate GPT-like response based on similar past email
def generate_gpt_like_response(new_email_body, past_email_body, past_receiver_response):
    model_name = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    
    prompt = (
        f"You are an AI assistant responding as a freelancer to a business owner's inquiry about a logo design.\n\n"
        f"Past freelancer response: {past_receiver_response}\n\n"
        f"New business inquiry: {new_email_body}\n\nResponse:"
    )
    
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(
        inputs, 
        max_new_tokens=250, 
        num_return_sequences=1, 
        no_repeat_ngram_size=2, 
        temperature=0.1,  # Very low temperature to avoid hallucination
        do_sample=True   # Enable sampling for temperature to work
    )
    
    generated_response = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_response

# Main function
def main():
    service = authenticate_gmail()
    all_emails = get_all_emails(service)
    
    # Fetch all emails and print them
    s3_objects = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)
    for obj in s3_objects.get('Contents', []):
        file_content = s3.get_object(Bucket=S3_BUCKET_NAME, Key=obj['Key'])
        print(file_content['Body'].read().decode())  # Print content of each file in S3

    # Assuming you already have the unread email here
    new_unread_email = {
        'sender': 'john.doe@example.com',
        'body': "I'm interested in your logo design services. Can you provide more details?"
    }

    # Find most similar email and draft a response
    similar_email = find_most_similar_email(new_unread_email, all_emails, model, tokenizer)

    if similar_email:
        past_receiver_response = similar_email['body']
        new_email_body = new_unread_email['body']
        response = generate_gpt_like_response(new_email_body, similar_email['body'], past_receiver_response)
        print(f"Generated Response: {response}")
    else:
        print("No similar email found.")

if __name__ == "__main__":
    main()
