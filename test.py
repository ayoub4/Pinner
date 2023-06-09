import requests

# Define the API endpoint URL
api_url = 'http://127.0.0.1:8000/pin'

# Define the pin URL to send in the request
pin_url = 'https://montapispriere.com/tapis-de-priere-uni/tapis-de-priere-beige/tapis-de-priere-beige-argente/'
url='https://universcendrier.com/pin?pin_url=https%253A%252F%252Fcouplesamoureux.com%252Fwp-content%252Fuploads%252F2023%252F03%252Falliances-coeur-graves-700206_1200x.webp'
# Send the POST request to the API
response = requests.get("http://127.0.0.1:8000/pin?pin_url=https://montapispriere.com/tapis-de-priere-uni/tapis-de-priere-violet/tapis-de-priere-violet-argente/&pin_description=&pin_title=Tapis%20de%20pri%C3%A8re%20violet%20argent%C3%A9&img_url=https://montapispriere.com/wp-content/uploads/2023/04/Tapis-de-pri-re-Hexagonal-violet-110x77cm-appel-Dodya-pri-re-musulmane-islamique-tat-de-la.jpg_Q90.jpg_-wpp1680950543805-150x150.webp&website=mon%20tapis%20priere&pin_table=Tapis%20de%20Pri%C3%A8re%20Pliable")

# Check the response
if response.status_code == 200:
    print('Pin posted successfully:', response.text)
else:
    print('Failed to post pin. Error:', response.text)
