import requests

# Define the API endpoint URL
api_url = 'http://127.0.0.1:8000/pin'

# Define the pin URL to send in the request
pin_url = 'https://montapispriere.com/tapis-de-priere-uni/tapis-de-priere-beige/tapis-de-priere-beige-argente/'
url='https://universcendrier.com/pin?pin_url=https%253A%252F%252Fcouplesamoureux.com%252Fwp-content%252Fuploads%252F2023%252F03%252Falliances-coeur-graves-700206_1200x.webp'
# Send the POST request to the API
response = requests.get("http://127.0.0.1:8000/pin?pin_url=https://couplesamoureux.com/vetements-couple/pyjama-couple/pyjama-assorti-pour-couple-bleu-en-satin-de-soie-dragon/&pin_description=&pin_title=Pyjama%20assorti%20pour%20couple%20bleu%20en%20satin%20de%20soie%20dragon&img_url=https://couplesamoureux.com/wp-content/uploads/2023/03/H8b4fad6840f64316929a115f29b8f4ecq-150x150.jpg&website=retro%20verso&pin_table=Pyjama%20couple")

# Check the response
if response.status_code == 200:
    print('Pin posted successfully:', response.text)
else:
    print('Failed to post pin. Error:', response.text)
