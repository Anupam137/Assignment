import requests
import re
from flask import Flask, jsonify

# Function to get data from paginated API
def fetch_data_from_api(base_url):
    all_data = []
    page = 1
    
    while True:
        response = requests.get(f"{base_url}?page={page}")
        if response.status_code != 200:
            break
        
        data = response.json()
        if not data:
            break
        
        all_data.extend(data)
        page += 1
        
    return all_data

# Function to find citations
def find_citations(data):
    citations = []
    
    for item in data:
        response_text = item.get("response", "")
        sources = item.get("sources", [])
        
        matched_sources = []
        
        for source in sources:
            source_context = source.get("context", "")
            if re.search(re.escape(source_context), response_text, re.IGNORECASE):
                citation = {"id": source.get("id")}
                if "link" in source:
                    citation["link"] = source["link"]
                matched_sources.append(citation)
        
        citations.append(matched_sources)
        
    return citations

# Flask app setup
app = Flask(__name__)

@app.route('/get_citations', methods=['GET'])
def get_citations():
    api_url = "https://devapi.beyondchats.com/api/get_message_with_sources"
    data = fetch_data_from_api(api_url)
    citations = find_citations(data)
    return jsonify(citations)

if __name__ == "__main__":
    app.run(debug=True)
