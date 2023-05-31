import time
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_cors import CORS, cross_origin
import Levenshtein
import random
import time
import schedule

class PinDetails:
    def __init__(self, img_url, pin_url, pin_title, pin_description):
        self.img_url = img_url
        self.pin_url = pin_url
        self.pin_title = pin_title
        self.pin_description = pin_description

class Account:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class PinPoster:
    def __init__(self, account):
        self.account = account
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--window-size=1920x1080')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')


    def find_closest_image(self, img_url, images_list):
        # Remove extension from the original img_url
        img_url_base, img_extension = img_url.rsplit('.', 1)

        if '-' in img_url_base[-0:]:
            img_url_base = img_url_base.rsplit('-', 1)[0]

        # Check if img_url_base is in images_list
        if img_url_base + '.' + img_extension in images_list:
            return img_url_base + '.' + img_extension

        distances = [(url, Levenshtein.distance(img_url, url)) for url in images_list]

        # Sort distances in ascending order
        distances.sort(key=lambda x: x[1])

        # Return the closest URL as it is (with extension)
        return distances[0][0]

    def create_pin(self, pin_details):
        driver = webdriver.Chrome(options=self.chrome_options)
        driver.get('https://www.pinterest.fr/login/')

        email_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="email"]')))
        email_input.send_keys(self.account.email)

        password_input = driver.find_element(By.XPATH, '//*[@id="password"]')
        password_input.send_keys(self.account.password)

        login_button = driver.find_element(By.XPATH, '//*[@id="mweb-unauth-container"]/div/div[3]/div/div/div[3]/form/div[7]/button')
        login_button.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="landing-page"]')))

        create_pin_button = driver.find_element(By.XPATH, '//*[@id="HeaderContent"]/div/div/div/div/div[2]/div/div/div/div[2]/div/button/div/div')
        create_pin_button.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="create-menu-content"]'))
        )
        create_menu_content = driver.find_element(By.XPATH, '//*[@id="create-menu-content"]')
        create_pin_button_2 = create_menu_content.find_element(By.XPATH, './/*[text()="Créer une Épingle"]')
        create_pin_button_2.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[3]/div'))
        )
        create_pin_button_3 = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, './/*[text()="Créer une nouvelle Épingle"]'))
        )
        create_pin_button_3.click()

        create_pin_by_url = driver.find_element(By.XPATH, '//*[@aria-label="Enregistrer depuis l’URL"]')
        create_pin_by_url.click()

        pin_url_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'scrape-view-website-link')))
        pin_url_input.send_keys(pin_details.pin_url)

        pin_url_go = driver.find_element(By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[3]/div/div/button/div/div')
        pin_url_go.click()

        time.sleep(3)
        image_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//img[contains(@alt, "Sélectionner l\'image dans")]'))
        )
        # Get the src attribute values
        image_sources = [image_element.get_attribute('src') for image_element in image_elements]
        result = self.find_closest_image(pin_details.img_url, image_sources)

        for image_element in image_elements:
            if image_element.get_attribute('src') == result:
                image_element.click()
                break

        pin_confirm = driver.find_element(By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/button/div/div')
        pin_confirm.click()

        # Wait for the pin title input to be present
        pin_title_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/textarea'))
        )
        pin_title_input.send_keys(pin_details.pin_title)

        # Wait for the pin description input to be present
        pin_description_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/div'))
        )
        pin_description_input.send_keys(pin_details.pin_description)

        submit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="board-dropdown-save-button"]'))
        )
        publish_button = submit_button.find_element(By.XPATH, './/*[contains(text(), "Publier")]')
        time.sleep(0.5)
        publish_button.click()

        # Wait for the pin to be created
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="dismiss"]'))
        )

        # Close the browser
        driver.quit()

        return "Pin posted: " + pin_details.pin_title

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

pin_queue = []

def post_pin(pin_poster, pin_details):
    pin_poster.create_pin(pin_details)

@app.route('/pin')
@cross_origin()
def pin():
    img_url = request.args.get('img_url')
    pin_url = request.args.get('pin_url')
    pin_title = request.args.get('pin_title')
    pin_description = request.args.get('pin_description')
    website = request.args.get('website')  # New parameter to get the website name

    if pin_url:
        if website == 'Univers Peluche':
            email = 'admins@goldenparkproject.com'
            password = 'bhjbhj2@Ss'
        elif website == 'mon pilou pilou':
            email = 'contact@monpiloupilou.com'
            password = 'bhjbhj2@Ss'
        elif website == 'couples amoureux':
            email = 'contact@couplesamoureux.com'
            password = 'bhjbhj2@Sssa'
        elif website == 'ma robe boheme':
            email = 'contact@marobeboheme.com'
            password = 'bhjbhj2@Ss'
        elif website == 'robe princesse':
            email = 'contact@robeprincesse.com'
            password = 'bhjbhj2@Ss'
        elif website == 'esprit polaire':
            email = 'contact@espritpolaire.com'
            password = 'bhjbhj2@Ss'
        elif website == 'retro verso':
            email = 'ecomfranceltd@gmail.com'
            password = 'bhjbhj2@Ss'
        elif website == 'mon tapis priere':
            email = 'contact@montapispriere.com'
            password = 'bhjbhj2@Ss'
        elif website == 'applique murale':
            email = 'contact@appliquemurale.com'
            password = 'bhjbhj2@Ss'
        else:
            return "Error: Not The Right Website"

        pin_details = PinDetails(img_url, pin_url, pin_title, pin_description)
        account = Account(email, password)
        pin_poster = PinPoster(account)

        # Add the pin post to the queue
        pin_queue.append((pin_poster, pin_details))

        return "Pin added to the queue"
    else:
        return "Error: 'pin_url' parameter is missing"

# Function to process the pin queue
def process_pin_queue():
    if len(pin_queue) > 0:
        # Get a random interval between 8 am and 6 pm
        random_hour = random.randint(8, 17)
        random_minute = random.randint(0, 59)

        # Schedule the pin post with a random delay
        schedule.every().day.at(f"{random_hour:02d}:{random_minute:02d}").do(post_next_pin)

def post_next_pin():
    if len(pin_queue) > 0:
        # Get the next pin post from the queue
        pin_poster, pin_details = pin_queue.pop(0)
        post_pin(pin_poster, pin_details)

        # Schedule the next pin post with a random delay
        min_delay = 1  # Minimum delay between pin posts (in minutes)
        max_delay = 5  # Maximum delay between pin posts (in minutes)
        random_delay = random.randint(min_delay, max_delay)
        schedule.every(random_delay).minutes.do(post_next_pin)

# Schedule the pin queue processing to start at 8 am
schedule.every().day.at("08:00").do(process_pin_queue)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
