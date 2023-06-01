import requests

# Define the API endpoint URL
api_url = 'http://127.0.0.1:8000/pin'

# Define the pin URL to send in the request
pin_url = 'https://montapispriere.com/tapis-de-priere-uni/tapis-de-priere-beige/tapis-de-priere-beige-argente/'
url='https://universcendrier.com/pin?pin_url=https%253A%252F%252Fcouplesamoureux.com%252Fwp-content%252Fuploads%252F2023%252F03%252Falliances-coeur-graves-700206_1200x.webp'
# Send the POST request to the API
response = requests.get(" http://164.68.105.49:8000/pin?pin_url=https://couplesamoureux.com/vetements-couple/pyjama-couple/pyjama-couple-manches-courtes-en-satin-imprime/&pin_description=&pin_title=Pyjama%20couple%20manches%20courtes%20en%20satin%20imprim%C3%A9&img_url=https://couplesamoureux.com/wp-content/uploads/2023/03/Hc8c89d44b2e043cabfcaa27d6606ec36u-150x150.jpg&website=couples%20amoureux")

# Check the response
if response.status_code == 200:
    print('Pin posted successfully:', response.text)
else:
    print('Failed to post pin. Error:', response.text)
