import what3words, requests
from os import environ

# public API
geocoder = what3words.Geocoder("what3words-api-key")

#API server
geocoder = what3words.Geocoder("what3words-api-key", end_point=)

def fetch(getcoder):
    try:
        response = request.get(geocoder)
        if response.status.code(200):
            return response.json()
        else:
            print(f"Error fetching API data {response.status_code}")
            
    except Exception as e:
        print(f"Exception occurred while fetching data: {e}")
    
