import re
import time

import requests
from selenium import webdriver

proxy_url = 'http://geo.iproyal.com:12321:sxxq:Sjdjd3ds_country-fr'

# Parse the proxy URL to extract the hostname and port number
match = re.match(r'http://(.*):(\d+):(.+):(.+)', proxy_url)
hostname = match.group(1)
port = int(match.group(2))
username = match.group(3)
password = match.group(4)

# Create a proxy configuration dictionary for use with requests and Selenium
proxies = {
    'http': f'http://{username}:{password}@{hostname}:{port}',
    'https': f'https://{username}:{password}@{hostname}:{port}'
}

# Use requests library to fetch the IP through the proxy
response = requests.get('https://ipv4.icanhazip.com', proxies=proxies)
print(response.text.strip())  # This should print the IP address fetched through the proxy

# Set the proxy options for the Chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--proxy-server={proxies["http"]}')
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.pinterest.fr/login/')
time.sleep(100)