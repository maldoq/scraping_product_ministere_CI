import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

url = "https://cnlvc.ci/"

def start_app(url):
    PATH = r'C:\Users\Uriel-Marie\Documents\School\scrapping\Projet_web_scraping-main\edgedriver_win64\msedgedriver.exe'
    # This creates a Service object for Microsoft Edge, using the WebDriver located at the given path.
    service = Service(PATH)

    # This initializes the Edge WebDriver using the service defined above
    driver = webdriver.Edge(service=service)
    # This opens the Edge browser and navigates to the webpage specified by the url variable
    driver.get(url)

    action = ActionChains(driver)
    li_archive_link = driver.find_element(By.CSS_SELECTOR, '#menu-td-demo-header-menu-1 > li.menu-item.menu-item-type-taxonomy.menu-item-object-category.menu-item-has-children.td-menu-item.td-normal-menu.menu-item-198')
    action.move_to_element(li_archive_link)
    action.perform()

    time.sleep(2)

    link_actualite = li_archive_link.find_element(By.CSS_SELECTOR, 'ul > li.menu-item.menu-item-type-post_type.menu-item-object-page.td-menu-item.td-normal-menu.menu-item-12107 > a')
    action.move_to_element(link_actualite)
    action.perform()


    time.sleep(5)
    
    driver.quit()



start_app(url)