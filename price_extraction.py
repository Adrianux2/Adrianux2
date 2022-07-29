import time
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
warnings.filterwarnings("ignore")


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


driver, wait = browser_load()

site = input("Enter the URL of the catalog: ")

if "contacts" in site:
    product_type = "div[3]/div[2]/div/div/div[1]"
else:
    product_type = "div[3]/div[2]/div/div/div[2]"

print("Loading site...", end='\r')

URL = site
driver.get(URL)

load_more_b = "//div[@class='w4f4-dSrOfUwxLg3A_yvN']"

wait.until(expected_conditions.presence_of_element_located((By.XPATH, load_more_b)))
print("Loading the whole catalog", end='\r')
time.sleep(5)

try:
    driver.find_element(By.XPATH, "//*[@id='close-btn-action']").click()
except:
    time.sleep(0.2)

try:
    while expected_conditions.presence_of_element_located((By.XPATH, load_more_b)):
        driver.find_element(By.XPATH, load_more_b).click()
        time.sleep(2.2)

except:
    print("Successfully loaded the whole catalog")
    time.sleep(1)


def obtaining_values():
    Name = catalog.find_element_by_xpath("div[3]/div[1]/div").text.replace(",", "")
    price = catalog.find_element_by_xpath(product_type).text
    sku = catalog.get_attribute("href").split("/product/", 1)[1].split("-")[0]
    return sku, Name, price


print("Beginning extraction process")
time.sleep(2)
frames = driver.find_elements(By.XPATH, "//div[@class= '_3Sj7PI7iAN1htrQ78RifQ0']/a")
with open('catalog_prices_extraction.csv', 'w') as csv:
    for catalog in frames:
        colors = catalog.find_elements_by_xpath("div[2]/div/div")
        if colors:
            for color in colors:
                color.click()
                Extracted_color = color.find_element(By.CLASS_NAME, "_27UKDhewEZeIDXgKo63X2z").text
                sku, Name, price = obtaining_values()
                print(sku + " | " + Name + " | " + price + " | " + Extracted_color)
                csv.write(f"{sku}, {Name}, {price}, {Extracted_color}\n")

        else:
            sku, Name, price = obtaining_values()
            print(sku + " | " + Name + " | " + price)
            csv.write(f"{sku}, {Name}, {price}\n")

print("Successfully extracted the catalog")
driver.close()
