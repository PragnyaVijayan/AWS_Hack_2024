import requests
import os
from urllib.parse import urlencode

import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
from flask import Flask, request

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
