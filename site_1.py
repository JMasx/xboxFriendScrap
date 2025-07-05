from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def login_and_scrape(gamertag):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Relative path to chromedriver from script location
    chromedriver_path = os.path.join(BASE_DIR, 'chromedriver-win64', 'chromedriver.exe')

    service = Service(chromedriver_path)
    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 120)

    driver.get("https://www.xbox.com/en-US/play")
    print("Please log in manually in the opened browser window...")

    try:
        wait.until(EC.url_contains("/en-US/"))
        print("Login detected, navigating to user profile...")
    except:
        print("Login not detected within timeout. Exiting.")
        return []

    driver.get(f"https://www.xbox.com/en-US/play/user/{gamertag}")

    try:
        friends_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Friends')]/parent::div")))
        friends_button.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".FriendsAndFollowersList-module__userList___RYzIa")))
    except:
        print("Failed to load friends list.")
        return []

    friends = [elem.text for elem in driver.find_elements(By.CSS_SELECTOR, ".Gamertag-module__baseGamerTag___lwdQS")]

    print(f"Found {len(friends)} friends:")
    for f in friends:
        print(f)
    return friends



# Example usage
target_gamertag = "Jadenize"
login_and_scrape(target_gamertag)
