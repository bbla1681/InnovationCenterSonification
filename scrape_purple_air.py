from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep

options = webdriver.ChromeOptions() 

prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory": 
                        r"your\path\here\\",#IMPORTANT - ENDING SLASH '\\' IMPORTANT
             "directory_upgrade": True}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)

#URL for the FLC Outdoor Sensor
outside_url = "https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=127669#14.95/38.66004/-121.12714"

#Url for the FLC Spider Shed
spider_url = "https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=125385#14.95/38.66004/-121.12714"

driver.get(outside_url)

sleep(5)
element = driver.find_element(By.CLASS_NAME, "highcharts-button-box")
actions = ActionChains(driver)
actions.move_to_element(element).click().perform()

elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "highcharts-menu-item"))
)

element_to_click = elements[5] 
element_to_click.click()

sleep(5)