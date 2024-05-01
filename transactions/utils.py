import requests
from .models import Notification

def get_currency_conversion(base_currency, target_currency, amount):
    # Construct the URL for the currency conversion service
    url = f"http://localhost:8000/webapps2024/conversion/{base_currency}/{target_currency}/{amount}"

    try:
        # Make a GET request to the currency conversion service
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response to a Python dict
            data = response.json()
            return data
        else:
            # Handle responses other than 200 OK
            return {"error": f"Failed to convert currency. Status Code: {response.status_code}", "details": response.text}
    except Exception as e:
        # Handle errors in making the request
        return {"error": "An error occurred while making the request.", "details": str(e)}
