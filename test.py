import requests

# Define the API endpoint URL
api_url = ' http://164.68.105.49:8000/pin'

# Define the pin URL to send in the request
pin_url = 'https://couplesamoureux.com/wp-content/uploads/2023/03/alliances-coeur-graves-700206_1200x.webp'

# Send the POST request to the API
response = requests.get(api_url, data={'pin_url': pin_url})

# Check the response
if response.status_code == 200:
    print('Pin posted successfully:', response.text)
else:
    print('Failed to post pin. Error:', response.text)
