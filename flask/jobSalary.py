import requests
import os
from urllib.parse import urlencode
from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import json
import matplotlib

matplotlib.use('Agg')  # Use a non-interactive backend

app = Flask(__name__)
CORS(app)

@app.route('/jobSalary', methods=['GET'])
def jobSalary():
  # get query parameter
  location = request.args.get('location')  
  occupation = request.args.get('occupation') 

  # create request url
  base_url = f"https://api.careeronestop.org/v1/comparesalaries/{os.getenv('USER_ID')}/wage"
  params = {
      'keyword': occupation, # ex: 'Data%20Scientists', 
      'location': location, # ex: 'CA'
      'enableMetaData': 'false'
  }
  url = f"{base_url}?{urlencode(params)}"

  # Set headers for the request
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {os.getenv('TOKEN')}" 
  }

  # Send GET request to the API
  try:
      response = requests.get(url, headers=headers)
      if response.status_code != 200:
          print(f"Error: {response.status_code}")
          return response.text 
  except Exception as e:
      print(f"An error occurred: {e}")

  return response.json()["OccupationDetail"]["Wages"]["StateWagesList"][0]

# TODO: change api to call occuptation first
@app.route('/occupation', methods=['GET'])
def occupation():
  # get query parameter
  keyword = request.args.get('keyword')  

  # create request url
  url = f"https://api.careeronestop.org/v1/occupation/{os.getenv('USER_ID')}/{keyword}/N/0/50"

  # Set headers for the request
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {os.getenv('TOKEN')}" 
  }

  # Send GET request to the API
  try:
      response = requests.get(url, headers=headers)
      if response.status_code != 200:
          print(f"Error: {response.status_code}")
          return response.text 
  except Exception as e:
      print(f"An error occurred: {e}")

  return [occupation['OnetTitle'] for occupation in response.json()['OccupationList']]


s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-west-2',
)

@app.route('/s3_user_upload', methods=['POST'])
def upload_to_s3():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Convert the received data to JSON string
    file_content = json.dumps(data)
    
    try:
        s3_client.put_object(Bucket="inrixhack2024", Key="UserData.json", Body=file_content)
        return jsonify({"message": "Data uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/s3_user_read', methods=['GET'])
def read_from_s3():
    try:
        response = s3_client.get_object(Bucket="inrixhack2024", Key="UserData.json")
        file_content = response['Body'].read().decode('utf-8')
        data = json.loads(file_content)
        
        return jsonify(data), 200 
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
