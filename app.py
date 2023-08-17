import datetime
import queue
import shutil
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
import threading
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import yagmail as yagmail


class PinDetails:
    def __init__(self, img_url, pin_url, pin_title, pin_description, pin_table):
        self.img_url = img_url
        self.pin_url = pin_url
        self.pin_title = pin_title
        self.pin_description = pin_description
        self.pin_table = pin_table
class Account:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class PinPoster:
    def __init__(self, account):
        self.account = account
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--window-size=1920x1080')
        self.driver = None

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

    """""""""""""""""""""""""""""""""""""""""Declaration"""""""""""""""""""""""""""""""""""""""""""""

    def create_pin_couples_amoureux(self, pin_details):
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.get('https://www.pinterest.fr/login/')

            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="email"]')))
            email_input.send_keys(self.account.email)

            password_input = self.driver.find_element(By.XPATH, '//*[@id="password"]')
            password_input.send_keys(self.account.password)

            login_button = self.driver.find_element(By.XPATH, '//*[@id="mweb-unauth-container"]/div/div[3]/div/div/div[3]/form/div[7]/button')
            login_button.click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="landing-page"]')))

            create_pin_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                '/html/body/div[1]/div/div[1]/div/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/button/div/div/div[1]/div')))
            create_pin_button.click()

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="create-menu-content"]'))
            )
            create_menu_content = self.driver.find_element(By.XPATH, '//*[@id="create-menu-content"]')
            create_pin_button_2 = create_menu_content.find_element(By.XPATH, './/*[text()="Créer une Épingle"]')
            create_pin_button_2.click()

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div'))
            )
            create_pin_button_3 = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, './/*[text()="Créer une nouvelle Épingle"]'))
            )
            create_pin_button_3.click()

            create_pin_by_url = self.driver.find_element(By.XPATH, '//*[@aria-label="Enregistrer depuis l’URL"]')
            create_pin_by_url.click()

            pin_url_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'scrape-view-website-link')))
            pin_url_input.send_keys(pin_details.pin_url)

            pin_url_go = self.driver.find_element(By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[3]/div/div/button/div/div')
            pin_url_go.click()

            time.sleep(3)
            image_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//img[contains(@alt, "Sélectionner l\'image dans")]'))
            )
            # Get the src attribute values
            image_sources = [image_element.get_attribute('src') for image_element in image_elements]
            result = self.find_closest_image(pin_details.img_url, image_sources)

            for image_element in image_elements:
                if image_element.get_attribute('src') == result:
                    image_element.click()
                    break

            pin_confirm = self.driver.find_element(By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/button/div/div')
            pin_confirm.click()


            pin_title_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/textarea'))
            )
            pin_title_input.send_keys(pin_details.pin_title)

            # Wait for the pin description input to be present
            pin_description_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/div'))
            )
            pin_description_input.send_keys(pin_details.pin_description)

            time.sleep(0.5)

            tables_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="board-dropdown-select-button"]'))
            )
            tables_button.click()

            tables_div = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div[2]'))
            )
            desired_element = tables_div.find_element(By.XPATH, f'.//*[contains(text(), "{pin_details.pin_table}")]')
            desired_element.click()

            time.sleep(0.5)

            submit_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="board-dropdown-save-button"]'))
            )
            publish_button = submit_button.find_element(By.XPATH, './/*[contains(text(), "Publier")]')
            time.sleep(0.5)
            publish_button.click()

            # Wait for the pin to be created
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="dismiss"]'))
            )

            # Close the browser
            self.driver.quit()
            return "success", "Pin posted: " + pin_details.pin_title  # Return success

        except Exception as e:
            print("An error occurred:", e)
            # No need to quit the driver here, it's done in the finally block

            return "error", "Error posting pin: " + str(e)  # Return error message
        finally:
            if self.driver:
                self.driver.quit()


    def create_pin_univers_peluche(self, pin_details):
            try:
                self.driver = webdriver.Chrome(options=self.chrome_options)
                self.driver.get('https://www.pinterest.fr/login/')

                email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="email"]')))
                email_input.send_keys(self.account.email)

                password_input = self.driver.find_element(By.XPATH, '//*[@id="password"]')
                password_input.send_keys(self.account.password)

                login_button = self.driver.find_element(By.XPATH, '//*[@id="mweb-unauth-container"]/div/div[3]/div/div/div[3]/form/div[7]/button')
                login_button.click()

                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="landing-page"]')))
                create_pin_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/button/div/div/div[1]/div')))
                create_pin_button.click()

                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="create-menu-content"]'))
                )
                create_menu_content = self.driver.find_element(By.XPATH, '//*[@id="create-menu-content"]')
                create_pin_button_2 = create_menu_content.find_element(By.XPATH, './/*[text()="Créer une Épingle Idée"]')
                create_pin_button_2.click()

                """WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div'))
                )
                create_pin_button_3 = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, './/*[text()="Créer une nouvelle Épingle"]'))
                )
                create_pin_button_3.click()"""

                create_pin_by_url = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Enregistrer depuis l’URL"]')))
                create_pin_by_url.click()

                pin_url_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'scrape-view-website-link')))
                pin_url_input.send_keys(pin_details.pin_url)

                pin_url_go = self.driver.find_element(By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[3]/div/div/button/div/div')
                pin_url_go.click()

                time.sleep(3)
                image_elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//img[contains(@alt, "Sélectionner l\'image dans")]'))
                )
                # Get the src attribute values
                image_sources = [image_element.get_attribute('src') for image_element in image_elements]
                result = self.find_closest_image(pin_details.img_url, image_sources)

                for image_element in image_elements:
                    if image_element.get_attribute('src') == result:
                        image_element.click()
                        break

                pin_confirm = self.driver.find_element(By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/button/div/div')
                pin_confirm.click()

                # Wait for the pin title input to be present
                pin_title_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/textarea'))
                )
                pin_title_input.send_keys(pin_details.pin_title)

                # Wait for the pin description input to be present
                pin_description_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/div'))
                )
                pin_description_input.send_keys(pin_details.pin_description)

                time.sleep(0.5)

                tables_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="board-dropdown-select-button"]'))
                )
                tables_button.click()

                tables_div = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div[2]'))
                )
                desired_element = tables_div.find_element(By.XPATH, f'.//*[contains(text(), "{pin_details.pin_table}")]')
                desired_element.click()

                time.sleep(0.5)

                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="board-dropdown-save-button"]'))
                )
                publish_button = submit_button.find_element(By.XPATH, './/*[contains(text(), "Publier")]')
                time.sleep(0.5)
                publish_button.click()

                # Wait for the pin to be created
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="dismiss"]'))
                )

                # Close the browser
                self.driver.quit()

                return "success", "Pin posted: " + pin_details.pin_title  # Return success

            except Exception as e:
                print("An error occurred:", e)
                # No need to quit the driver here, it's done in the finally block

                return "error", "Error posting pin: " + str(e)  # Return error message
            finally:
                if self.driver:
                    self.driver.quit()


    def create_pin_ma_robe_boheme(self, pin_details):
            try:
                self.driver = webdriver.Chrome(options=self.chrome_options)
                self.driver.get('https://www.pinterest.fr/login/')

                email_input = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="email"]')))
                email_input.send_keys(self.account.email)

                password_input = self.driver.find_element(By.XPATH, '//*[@id="password"]')
                password_input.send_keys(self.account.password)

                login_button = self.driver.find_element(By.XPATH,
                                                        '//*[@id="mweb-unauth-container"]/div/div[3]/div/div/div[3]/form/div[7]/button')
                login_button.click()

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="landing-page"]')))

                create_pin_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/button/div/div/div[1]/div')))
                create_pin_button.click()

                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="create-menu-content"]'))
                )
                create_menu_content = self.driver.find_element(By.XPATH, '//*[@id="create-menu-content"]')
                create_pin_button_2 = create_menu_content.find_element(By.XPATH, './/*[text()="Créer une Épingle Idée"]')
                create_pin_button_2.click()

                """WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[3]/div'))
                )
                create_pin_button_3 = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, './/*[text()="Créer une nouvelle Épingle"]'))
                )
                create_pin_button_3.click()"""

                create_pin_by_url = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Créer des Épingles à partir d’une URL"]')))
                create_pin_by_url.click()

                pin_url_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'scrape-view-website-link')))
                pin_url_input.send_keys(pin_details.pin_url)

                pin_url_go = self.driver.find_element(By.XPATH,
                                                      '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[3]/div/div/button/div/div')
                pin_url_go.click()

                time.sleep(3)
                image_elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//img[contains(@alt, "Sélectionner l\'image dans")]'))
                )
                # Get the src attribute values
                image_sources = [image_element.get_attribute('src') for image_element in image_elements]
                result = self.find_closest_image(pin_details.img_url, image_sources)

                for image_element in image_elements:
                    if image_element.get_attribute('src') == result:
                        image_element.click()
                        break

                pin_confirm = self.driver.find_element(By.XPATH,
                                                       '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/button/div/div')
                pin_confirm.click()

                # Wait for the pin title input to be present
                pin_title_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/textarea'))
                )
                pin_title_input.send_keys(pin_details.pin_title)

                # Wait for the pin description input to be present
                pin_description_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/div'))
                )
                pin_description_input.send_keys(pin_details.pin_description)

                time.sleep(0.5)

                tables_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="board-dropdown-select-button"]'))
                )
                tables_button.click()

                tables_div = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div[2]'))
                )
                desired_element = tables_div.find_element(By.XPATH, f'.//*[contains(text(), "{pin_details.pin_table}")]')
                desired_element.click()

                time.sleep(0.5)

                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="board-dropdown-save-button"]'))
                )
                publish_button = submit_button.find_element(By.XPATH, './/*[contains(text(), "Publier")]')
                time.sleep(0.5)
                publish_button.click()

                # Wait for the pin to be created
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Fermer"]'))
                )

                # Close the browser
                self.driver.quit()
                return "success", "Pin posted: " + pin_details.pin_title  # Return success

            except Exception as e:
                print("An error occurred:", e)
                # No need to quit the driver here, it's done in the finally block

                return "error", "Error posting pin: " + str(e)  # Return error message
            finally:
                if self.driver:
                    self.driver.quit()


    def create_pin_pyjama_dor(self, pin_details):
            try:
                self.driver = webdriver.Chrome(options=self.chrome_options)
                self.driver.get('https://www.pinterest.fr/login/')

                email_input = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="email"]')))
                email_input.send_keys(self.account.email)

                password_input = self.driver.find_element(By.XPATH, '//*[@id="password"]')
                password_input.send_keys(self.account.password)

                login_button = self.driver.find_element(By.XPATH,
                                                        '//*[@id="mweb-unauth-container"]/div/div[3]/div/div/div[3]/form/div[7]/button')
                login_button.click()

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="landing-page"]')))

                create_pin_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/button/div/div/div[1]/div')))
                create_pin_button.click()

                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="create-menu-content"]'))
                )
                create_menu_content = self.driver.find_element(By.XPATH, '//*[@id="create-menu-content"]')
                create_pin_button_2 = create_menu_content.find_element(By.XPATH, './/*[text()="Créer une Épingle Idée"]')
                create_pin_button_2.click()

                """WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[3]/div'))
                )
                create_pin_button_3 = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, './/*[text()="Créer une nouvelle Épingle"]'))
                )
                create_pin_button_3.click()"""

                create_pin_by_url = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Enregistrer depuis l’URL"]')))
                create_pin_by_url.click()

                pin_url_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'scrape-view-website-link')))
                pin_url_input.send_keys(pin_details.pin_url)

                pin_url_go = self.driver.find_element(By.XPATH,
                                                      '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[3]/div/div/button/div/div')
                pin_url_go.click()

                time.sleep(3)
                image_elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//img[contains(@alt, "Sélectionner l\'image dans")]'))
                )
                # Get the src attribute values
                image_sources = [image_element.get_attribute('src') for image_element in image_elements]
                result = self.find_closest_image(pin_details.img_url, image_sources)

                for image_element in image_elements:
                    if image_element.get_attribute('src') == result:
                        image_element.click()
                        break

                pin_confirm = self.driver.find_element(By.XPATH,
                                                       '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/button/div/div')
                pin_confirm.click()

                # Wait for the pin title input to be present
                pin_title_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/textarea'))
                )
                pin_title_input.send_keys(pin_details.pin_title)

                # Wait for the pin description input to be present
                pin_description_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/div'))
                )
                pin_description_input.send_keys(pin_details.pin_description)

                time.sleep(0.5)

                tables_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="board-dropdown-select-button"]'))
                )
                tables_button.click()

                tables_div = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div[2]'))
                )
                desired_element = tables_div.find_element(By.XPATH, f'.//*[contains(text(), "{pin_details.pin_table}")]')
                desired_element.click()

                time.sleep(0.5)

                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="board-dropdown-save-button"]'))
                )
                publish_button = submit_button.find_element(By.XPATH, './/*[contains(text(), "Publier")]')
                time.sleep(0.5)
                publish_button.click()

                # Wait for the pin to be created
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="dismiss"]'))
                )

                # Close the browser
                self.driver.quit()

                return "success", "Pin posted: " + pin_details.pin_title  # Return success

            except Exception as e:
                print("An error occurred:", e)
                # No need to quit the driver here, it's done in the finally block

                return "error", "Error posting pin: " + str(e)  # Return error message
            finally:
                if self.driver:
                    self.driver.quit()


    def create_pin_retro_verso(self, pin_details):
            try:
                self.driver = webdriver.Chrome(options=self.chrome_options)
                self.driver.get('https://www.pinterest.fr/login/')

                email_input = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="email"]')))
                email_input.send_keys(self.account.email)

                password_input = self.driver.find_element(By.XPATH, '//*[@id="password"]')
                password_input.send_keys(self.account.password)

                login_button = self.driver.find_element(By.XPATH,
                                                        '//*[@id="mweb-unauth-container"]/div/div[3]/div/div/div[3]/form/div[7]/button')
                login_button.click()

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="landing-page"]')))

                create_pin_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/button/div/div/div[1]/div')))
                create_pin_button.click()

                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="create-menu-content"]'))
                )
                create_menu_content = self.driver.find_element(By.XPATH, '//*[@id="create-menu-content"]')
                create_pin_button_2 = create_menu_content.find_element(By.XPATH, './/*[text()="Créer une Épingle Idée"]')
                create_pin_button_2.click()

                """WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[3]/div'))
                )
                create_pin_button_3 = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, './/*[text()="Créer une nouvelle Épingle"]'))
                )
                create_pin_button_3.click()"""

                create_pin_by_url = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Créer des Épingles à partir d’une URL"]')))
                create_pin_by_url.click()

                pin_url_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'scrape-view-website-link')))
                pin_url_input.send_keys(pin_details.pin_url)

                pin_url_go = self.driver.find_element(By.XPATH,
                                                      '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[3]/div/div/button/div/div')
                pin_url_go.click()

                time.sleep(3)
                image_elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//img[contains(@alt, "Sélectionner l\'image dans")]'))
                )
                # Get the src attribute values
                image_sources = [image_element.get_attribute('src') for image_element in image_elements]
                result = self.find_closest_image(pin_details.img_url, image_sources)

                for image_element in image_elements:
                    if image_element.get_attribute('src') == result:
                        image_element.click()
                        break

                pin_confirm = self.driver.find_element(By.XPATH,
                                                       '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/button/div/div')
                pin_confirm.click()

                # Wait for the pin title input to be present
                pin_title_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/textarea'))
                )
                pin_title_input.send_keys(pin_details.pin_title)

                # Wait for the pin description input to be present
                pin_description_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/div'))
                )
                pin_description_input.send_keys(pin_details.pin_description)

                time.sleep(0.5)

                tables_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="board-dropdown-select-button"]'))
                )
                tables_button.click()

                tables_div = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div[2]'))
                )
                desired_element = tables_div.find_element(By.XPATH, f'.//*[contains(text(), "{pin_details.pin_table}")]')
                desired_element.click()

                time.sleep(0.5)

                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="board-dropdown-save-button"]'))
                )
                publish_button = submit_button.find_element(By.XPATH, './/*[contains(text(), "Publier")]')
                time.sleep(0.5)
                publish_button.click()

                # Wait for the pin to be created
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="dismiss"]'))
                )

                # Close the browser
                self.driver.quit()

                return "success", "Pin posted: " + pin_details.pin_title  # Return success

            except Exception as e:
                print("An error occurred:", e)
                # No need to quit the driver here, it's done in the finally block

                return "error", "Error posting pin: " + str(e)  # Return error message
            finally:
                if self.driver:
                    self.driver.quit()


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



def send_email_to_blog(pin_details):

    email = "btissamloukili12@gmail.com"
    second_email = "zineb.aourfi@um5r.ac.ma"
    third_email = "ayoub.mzari@uit.ac.ma"
    email_content = "Posting " + pin_details.pin_title + " Failed"

    smtp_username = 'parkg821@gmail.com'
    smtp_password = 'ftrwnwnvprcavvyd'

    try:
        # Create a yagmail SMTP client
        yag = yagmail.SMTP(smtp_username, smtp_password)

        # Randomly select a subject from the objects list
        subject = "Pin Failed"

        # Send the email with the random subject
        yag.send(to=email, subject=subject, contents=email_content)
        yag.send(to=second_email, subject=subject, contents=email_content)
        yag.send(to=third_email, subject=subject, contents=email_content)

        print(f"Email sent to {email}, {second_email}, {third_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

pin_queue = queue.Queue()
pin_queue_lock = threading.Lock()  # Lock to synchronize access to the pin queue

@app.route('/pin')
@cross_origin()
def pin():
    img_url = request.args.get('img_url')
    pin_url = request.args.get('pin_url')
    pin_title = request.args.get('pin_title')
    pin_description = request.args.get('pin_description')
    pin_table = request.args.get('pin_table')
    website = request.args.get('website')  # New parameter to get the website name

    if pin_url:
        if website == 'Univers Peluche':
            email = 'contact@universpeluche.com'
            password = 'Ssjksj@2&&@'
        elif website == 'couples amoureux':
            email = 'contact@couplesamoureux.com'
            password = 'AyoubMamoun123'
        elif website == 'ma robe boheme':
            email = 'contact@marobeboheme.com'
            password = 'AyoubMamoun123'
        elif website == 'retro verso':
            email = 'ecomfranceltd@gmail.com'
            password = 'AyoubMamoun123'
        elif website == 'pyjama d\'or':
            email = 'pyjamadorrs@gmail.com'
            password = 'dznj2dsjz&@'
        else:
            return "Error: Not The Right Website"

        pin_details = PinDetails(img_url, pin_url, pin_title, pin_description, pin_table)
        account = Account(email, password)
        pin_poster = PinPoster(account)

        # Add the pin post to the queue
        with pin_queue_lock:
            pin_queue.put((pin_poster, pin_details))

        return "Pin added to the queue"
    else:
        return "Error: 'pin_url' parameter is missing"

# Function to process the pin queue
def process_pin_queue():
    while True:
        try:
            # Use queue.get() with a timeout to wait for new pins
            pin_poster, pin_details = pin_queue.get(timeout=1)
        except queue.Empty:
            # The timeout occurred, indicating no new pins within the specified time
            continue

        """current_time = datetime.datetime.now().time()
        while not ((current_time >= datetime.time(8) and current_time <= datetime.time(12)) or (current_time >= datetime.time(14) and current_time <= datetime.time(18))):
            # Current time is not within the allowed posting times
            print("Current time is not within the allowed posting times. Waiting...")
            time.sleep(60)  # Wait for 1 minute before checking the time again
            current_time = datetime.datetime.now().time()

        wait_time = random.randint(15, 20) * 60  # Convert minutes to seconds
        print("Waiting for", wait_time // 60, "minutes before processing the next pin...")
        time.sleep(wait_time)  # Wait for the specified duration"""

        try:
                if pin_poster.account.email == "admins@goldenparkproject.com":
                    print("Posting pin : " + pin_details.pin_title + "...")
                    result, response = pin_poster.create_pin_univers_peluche(pin_details)
                    print(result)  # Print the response
                    if result == "error":
                        send_email_to_blog(pin_details)
                        pin_queue.put((pin_poster, pin_details))
                elif pin_poster.account.email == "contact@couplesamoureux.com":
                    print("Posting pin : " + pin_details.pin_title + "...")
                    result, response = pin_poster.create_pin_couples_amoureux(pin_details)
                    print(result)  # Print the response
                    if result == "error":
                        send_email_to_blog(pin_details)
                        pin_queue.put((pin_poster, pin_details))
                elif pin_poster.account.email == "contact@marobeboheme.com":
                    print("Posting pin : " + pin_details.pin_title + "...")
                    result, response = pin_poster.create_pin_ma_robe_boheme(pin_details)
                    print(result)  # Print the response
                    if result == "error":
                        send_email_to_blog(pin_details)
                        pin_queue.put((pin_poster, pin_details))
                elif pin_poster.account.email == "ecomfranceltd@gmail.com":
                    print("Posting pin : " + pin_details.pin_title + "...")
                    result, response = pin_poster.create_pin_retro_verso(pin_details)
                    print(result)  # Print the response
                    if result == "error":
                        send_email_to_blog(pin_details)
                        pin_queue.put((pin_poster, pin_details))
                elif pin_poster.account.email == "iamfiles123@gmail.com":
                    print("Posting pin : " + pin_details.pin_title + "...")
                    result, response = pin_poster.create_pin_pyjama_dor(pin_details)
                    print(result)
                    if result == "error":
                        send_email_to_blog(pin_details)
                        pin_queue.put((pin_poster, pin_details))

        except Exception as e:

                print("An error occurred while processing pin:", str(e))

if __name__ == '__main__':
    process_pin_queue_thread = threading.Thread(target=process_pin_queue)
    process_pin_queue_thread.start()

    app.run(host='0.0.0.0', port=8000)
