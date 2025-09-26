import logging
import time
import os
from selenium.common import NoSuchElementException, TimeoutException
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

PROMISED_DOWN = 150
PROMISED_UP = 10
X_EMAIL = os.getenv("x_email")
X_PASSWORD = os.getenv("x_password")
X_USER_NAME = os.getenv("x_username")
SPEEDTEST_URL = "https://www.speedtest.net"
X_URL = "https://x.com/i/flow/login"

#loggin configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers = [
        logging.StreamHandler(),
        logging.FileHandler("Internet-Speed-bot.log")
    ]
)

#setting chrome profile
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

class InternetSpeedTwitterBot:
    def __init__(self):
        self.up = PROMISED_UP
        self.down = PROMISED_DOWN
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)

    def get_internet_speed(self) ->tuple[str, str] | None:
        '''
        login to speedtest website, test internet upload speed and download speed
        :return: internet upload speed and download speed
        '''
        try:
            logging.info("Fetching speedtest URL")
            self.driver.get(SPEEDTEST_URL)
            #test internet speed
            go_button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "start-text")))
            logging.info("Successfully fetched go button")
            go_button.click()
            time.sleep(40)
            #fetching upload and download speed
            down_element = self.driver.find_element(By.CSS_SELECTOR, f"span[class*='download-speed']")
            up_element = self.driver.find_element(By.CSS_SELECTOR, f"span[class*='upload-speed']")
            down_speed = down_element.text
            up_speed = up_element.text
            logging.info(f"Download speed {down_speed}")
            logging.info(f"Upload speed {up_speed}")
            return down_speed, up_speed
        except (NoSuchElementException, TimeoutException) as ex:
            logging.error(f"Error fetching SpeedTest - {str(ex)}")
            return None
        except Exception as ex:
            logging.error(f"Error fetching SpeedTest - {str(ex)}")
            return None

    def tweet_at_provider(self, message:str) -> None:
        '''
        login to X
        post a post in X
        :param message:
        :return:
        '''
        try:
            logging.info("Searching for X login...")
            self.driver.get(X_URL)
            logging.info("Entering login info...")

            if not X_EMAIL or not X_USER_NAME or not X_PASSWORD:
                logging.error("Error in fetching X logging details")
                return

            #entering email
            email = self.wait.until(EC.presence_of_element_located((By.NAME, "text")))
            email.send_keys(X_EMAIL)
            next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]")))
            next_button.click()
            logging.info("Successfully entered the email")

            #entering user name
            try:
                user_name = self.wait.until(EC.presence_of_element_located((By.NAME, "text")))
                user_name.send_keys(X_USER_NAME)
                user_name_next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]")))
                user_name_next_button.click()
                logging.info("Successfully entered user name")
            except TimeoutException:
                logging.info("User name step skipped. proceed to password")

            #entering password
            password = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password.send_keys(X_PASSWORD)
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Log in']]")))
            login_button.click()
            logging.info("Successfully entered the password")
            time.sleep(20)

            #Enter X post
            logging.info("Searching to enter a post")
            text_area = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"div[class^='public-DraftStyleDefault']")))
            text_area.send_keys(message)
            post_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Post']]")))
            post_button.click()
            logging.info(f"Successfully entered the post - {message}")

        except (NoSuchElementException, TimeoutException) as ex:
            logging.error(f"Error login to X - {str(ex)}")
        except Exception as ex:
            logging.error(f"Error login to X - {str(ex)}")



def main():
    speed_bot = InternetSpeedTwitterBot()
    result = speed_bot.get_internet_speed()
    if not result:
        logging.error("Error fetching internet speed, Aborting...")
        return
    down_speed, up_speed = result
    if float(down_speed) <= PROMISED_DOWN and float(up_speed) <= PROMISED_UP:
        message = (f"Hay Internet Provider, why is my internet speed {down_speed}down/{up_speed}up "
                   f"when I pay {PROMISED_DOWN}down/{PROMISED_UP}up")
        speed_bot.tweet_at_provider(message)
    else:
        logging.info("Your internet speed is up to standard.")
    speed_bot.driver.quit()

if __name__ == "__main__":
    main()

