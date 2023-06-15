import requests

# Define the API endpoint URL
api_url = 'http://127.0.0.1:8000/pin'

# Define the pin URL to send in the request
pin_url = 'https://montapispriere.com/tapis-de-priere-uni/tapis-de-priere-beige/tapis-de-priere-beige-argente/'
url='https://universcendrier.com/pin?pin_url=https%253A%252F%252Fcouplesamoureux.com%252Fwp-content%252Fuploads%252F2023%252F03%252Falliances-coeur-graves-700206_1200x.webp'
# Send the POST request to the API
response = requests.get("http://127.0.0.1:8000/pin?pin_url=https://pyjamador.com/kigurumi/kigurumi-animaux/kigurumi-pingouin/kugurumi-pingouin-pour-adulte-rose/&pin_description=&pin_title=Kugurumi%20pingouin%20pour%20adulte%20rose&img_url=https://pyjamador.com/wp-content/uploads/2023/04/S17956326fbd642cea87d5d72e5e5ae92r-150x150.jpg&website=pyjama%20d%27or&pin_table=Kigurumi")

# Check the response
if response.status_code == 200:
    print('Pin posted successfully:', response.text)
else:
    print('Failed to post pin. Error:', response.text)
