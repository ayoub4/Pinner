import requests

# Define the API endpoint URL
api_url = 'http://127.0.0.1:8000/pin'

# Define the pin URL to send in the request
pin_url = 'https://montapispriere.com/tapis-de-priere-uni/tapis-de-priere-beige/tapis-de-priere-beige-argente/'
url='https://universcendrier.com/pin?pin_url=https%253A%252F%252Fcouplesamoureux.com%252Fwp-content%252Fuploads%252F2023%252F03%252Falliances-coeur-graves-700206_1200x.webp'
# Send the POST request to the API
response = requests.get("http://127.0.0.1:8000/pin?pin_url=https://marobeboheme.com/robe-longue-boheme/robe-cocktail-style-boheme-chic-florale-rose-longue/&pin_description=&pin_title=Robe%20cocktail%20style%20boh%C3%A8me%20chic%20Florale%20rose%20longue&img_url=https://marobeboheme.com/wp-content/uploads/2023/06/Robe-Longue-Manches-sulfpour-Femme-Mode-Cor-enne-l-gante-Florale-D-contract-e-Vacances-Printemps.jpg_640x640-150x150.jpg&website=ma%20robe%20boheme&pin_table=Robe%20Longue%20Boh%C3%A8me")

# Check the response
if response.status_code == 200:
    print('Pin posted successfully:', response.text)
else:
    print('Failed to post pin. Error:', response.text)
