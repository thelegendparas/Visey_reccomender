import requests

# Direct API key (replace with your actual API key)
GOOGLE_MAPS_API_KEY = "AIzaSyCuoL6iJnlWF9GWpucqiaCEV8iGZCb2sls"

def get_lat_lon(location: str):
    """
    Convert a location string into latitude and longitude using the Google Maps API.
    """
    try:
        # Construct the API URL with the provided location and API key
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}"
        
        # Make the GET request to the Google Maps API
        response = requests.get(url=url)
        data = response.json()
        
        # Check if the request was successful
        if data['status'] == 'OK':
            location_data = data['results'][0]['geometry']['location']
            latitude = location_data['lat']
            longitude = location_data['lng']
            return latitude, longitude
        else:
            print(f"Error: {data['status']}")
            return None, None
    except Exception as e:
        print(f"Error converting location: {e}")
        return None, None

# Test the function
if __name__ == "__main__":
    # Replace with your test address
    test_address = "Delhi Technological University, Rohini, New Delhi"
    lat, lon = get_lat_lon(test_address)
    print(f"Latitude: {lat}, Longitude: {lon}")
