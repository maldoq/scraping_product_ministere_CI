from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

url = ""

def start_app(url):
    PATH = r'C:\Users\Uriel-Marie\Documents\School\scrapping\Projet_web_scraping-main\edgedriver_win64\msedgedriver.exe'
    service = Service(PATH)

    driver = webdriver.Edge(service=service)
    driver.get(url)


start_app(url)