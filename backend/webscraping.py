from flask import Flask

import http.client
from fiverr_api import session

app = Flask(__name__)
@app.route('/fiver')
def diver():
    # url = "https://www.fiverr.com/categories/graphics-design/creative-logo-design?source=category_tree"
    # session.set_scraper_api_key("56570d84cd3f1319e7023d9cfd1b1805")
    # response = session.get(url) # your fiverr url should be here
    # # json_data = response.props_json() # gives you JSON
    # # print(json_data) # gives you beautiful soup instance
    # # # You can use `response.soup` to further extract your information. 

    # # Parse the JSON response or BeautifulSoup object
    # json_data = response.props_json()  # Extract JSON data
    # soup = response.soup  # Use BeautifulSoup to parse HTML
    # print(json_data)
    # return json_data

    conn = http.client.HTTPSConnection("upwork17.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "faa9720e69mshcac603914b87ed2p132eddjsne9bb8946d2cf",
        'x-rapidapi-host': "upwork17.p.rapidapi.com"
    }

    conn.request("GET", "/getListingByURL", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    return(data.decode("utf-8"))

if __name__ == '__main__':
    app.run(debug=True)

# Extract relevant details (from soup if JSON is incomplete)
# gigs = []
# for gig in soup.find_all('div', class_='gig-card-layout'):  # Adjust class to Fiverr's current structure
#     try:
#         title = gig.find('a', class_='gig-title').text.strip()
#         price = gig.find('span', class_='price').text.strip() if gig.find('span', class_='price') else "No price"
#         seller = gig.find('a', class_='seller-name').text.strip() if gig.find('a', class_='seller-name') else "No seller"
#         link = "https://www.fiverr.com" + gig.find('a', class_='gig-title')['href'] if gig.find('a', class_='gig-title') else "No link"
        
#         # Append gig details
#         gigs.append({
#             "title": title,
#             "price": price,
#             "seller": seller,
#             "link": link
#         })
#     except AttributeError:
#         continue

# # Output data in JSON format
# import json
# print(json.dumps(gigs, indent=4))
