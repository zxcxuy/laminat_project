from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utils
from scraper import scrapeAllLinks
from databaseCheck import init_database

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    for table_name in utils.table_names:
        init_database(utils.db_file, table_name)
    for link in utils.floorType:
        driver.get(link)
        scrapeAllLinks(driver, utils.db_file, EC, WebDriverWait)


    driver.quit()

if __name__ == "__main__":
    main()