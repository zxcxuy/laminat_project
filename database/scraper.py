from pageScrape import scrapePageLinks
from parse import parsePage

def scrapeAllLinks(driver, db_file, EC, WebDriverWait):
    pageCount = driver.find_element("xpath", '//div[@class="col-lg-8 col-md-6 col-12 mb-2"]/div/div[last()-1]/span[last()]').text
    links = []
    links += scrapePageLinks(driver)
    i = 1
    for _ in range(int(pageCount) - 1):
        try:
            
            nextPageBtn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(("xpath", '//div[@class="col-lg-8 col-md-6 col-12 mb-2"]/div/div[last()]')))

            driver.execute_script("arguments[0].scrollIntoView();", nextPageBtn)
            driver.execute_script("arguments[0].click();", nextPageBtn)

            links += scrapePageLinks(driver)
            i += 1
            print(i)

        except Exception as e:
            print(f"Error on page {i}: {str(e)}")
            break
    print(f"Total links collected: {len(links)}")
    parsePage(links, driver, db_file)

