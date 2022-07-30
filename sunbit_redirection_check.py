import time
import warnings
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from alive_progress import alive_bar

warnings.filterwarnings("ignore")

texts_to_replace = {'Now Optics - Stanton Optical- ': 'Stanton Optical - ',
                    ' (Jensen Beach)': '',
                    '- Gainesville': '- Gainesville (Archer Road)',
                    '- Dallas Midway': '- Dallas (Midway)'}


def prRed(skk): print("\033[91m{}\033[00m".format(skk))


def prGreen(skk): print("\033[92m{}\033[00m".format(skk))


def prYellow(skk): print("\033[93m{}\033[00m".format(skk))


def browser_load():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--start-mini")
    # chrome_options.add_argument("headless")
    chrome_options.add_argument("--log-level=4")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    s = Service('C:\\chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 60)

    return driver, wait


def env_ecommerce():
    global brand, environment
    d1a = input("Do you want to test in: \n a) MyEyelab. b) StantonOptical. [a/b]? : ")
    if d1a == "a":
        prGreen("\nMyeyelab Selected\n")
        brand = "myeyelab"
    elif d1a == "b":
        prGreen("\nStantonOptical Selected\n")
        brand = "stantonoptical"

    d1a = input("Do you want to test in: \n a) Staging. b) UAT. c) Production. [a/b/c]? : ")
    if d1a == "a":
        prGreen("\nStaging Selected")
        environment = "https://www.web.staging." + brand + ".merce.io/"
    elif d1a == "b":
        prGreen("\nUAT Selected")
        environment = "https://www.web.uat." + brand + ".merce.io/"
    elif d1a == "c":
        prGreen("\nProduction Selected")
        environment = "https://www." + brand + ".com/"
    return environment, brand


driver, wait = browser_load()

environment, brand = env_ecommerce()

data = pd.read_csv("eCommerce_SEO_Pages.csv")

if brand == "myeyelab":
    stores = data.myeyelab
else:
    data = data.dropna()
    stores = data.stantonoptical

sunbit_banner_loc = "//img[contains(@src,'sunbit-test')]/parent::div"
sunbit_text_loc = "div.jOQZaH"
with alive_bar(len(stores), length=150, spinner='dots_waves') as bar:
    for urls in stores:
        url = environment + urls
        driver.get(url)
        time.sleep(1)
        try:
            driver.find_element(By.XPATH, sunbit_banner_loc)
        except NoSuchElementException:
            sunbit_banner_presence = False
        else:
            sunbit_banner_presence = True

        if sunbit_banner_presence:
            strname = driver.find_element(By.CSS_SELECTOR, "label._2oVjpCRS_TYuY8JtDwuphv").text
            driver.find_element(By.XPATH, sunbit_banner_loc).click()
            parent_window = driver.window_handles[0]
            child_window = driver.window_handles[1]
            driver.switch_to.window(child_window)
            wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//a[contains(@href,'sunbit.com')]")))
            sunbit_url = driver.current_url
            if sunbit_url == "https://sunbit.com/":
                prRed("The location page " + url + " is not redirecting correctly")
                driver.close()
                driver.switch_to.window(parent_window)
            else:
                wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, sunbit_text_loc)))
                full_text = driver.find_element(By.CSS_SELECTOR, sunbit_text_loc).text
                for key, value in texts_to_replace.items():
                    subrand = full_text.replace(key, value)
                    suname = full_text.replace(key, value)
                subrand = subrand.split(" - ")[0].split("at ")[1].replace(" ", "").lower()
                suname = suname.split(" - ")[1]
                if strname == suname and subrand == brand:
                    prGreen(url + " have the corresponding sunbit page")
                    driver.close()
                    driver.switch_to.window(parent_window)
                else:
                    prRed("Discrepancy detected on " + sunbit_url)
                    driver.close()
                    driver.switch_to.window(parent_window)

        else:
            prYellow(str(url) + " doesn't have Sunbit Banner")
        bar()
driver.quit()
