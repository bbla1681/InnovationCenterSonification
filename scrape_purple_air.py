from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os

def scrape_air_data(sensor):
    options = webdriver.ChromeOptions() 

    options.add_argument("--headless")

    prefs = {"profile.default_content_settings.popups": 0,
                "download.default_directory": 
                            r"C:\Users\bbla1\Projects\sonification\Wave Branch\InnovationCenterSonification\purple_data\\",#IMPORTANT - ENDING SLASH '\\' IMPORTANT
                "directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)

    #URL for the FLC Outdoor Sensor
    outside_url = "https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=127669#14.95/38.66004/-121.12714"

    #Url for the FLC Spider Shed
    spider_url = "https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=125385#14.95/38.66004/-121.12714"

    #Outdoor Sensor
    if sensor == 0:
        driver.get(outside_url)

        sleep(2)
        element = driver.find_element(By.CLASS_NAME, "highcharts-button-box")
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()

        sleep(1)
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "highcharts-menu-item"))
        )

        element_to_click = elements[5] 
        driver.execute_script("arguments[0].click();", element_to_click)

        sleep(2)

        download_directory = 'purple_data' 

        list_of_files = os.listdir(download_directory)

        new_file_name = "outdoor.csv"

        os.rename(os.path.join(download_directory, list_of_files[0]), os.path.join(download_directory, new_file_name))

    #Spider Shed
    if sensor == 1:
        driver.get(spider_url)

        sleep(2)
        element = driver.find_element(By.CLASS_NAME, "highcharts-button-box")
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()

        sleep(2)
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "highcharts-menu-item"))
        )
        element_to_click = elements[5] 

        driver.execute_script("arguments[0].click();", element_to_click)

        sleep(1)

        list_of_files = os.listdir(download_directory)

        new_file_name = "spider.csv"

        os.rename(os.path.join(download_directory, list_of_files[1]), os.path.join(download_directory, new_file_name))

