from pageScrape import scrapePageLinks, scrapePageArts
from parse import parsePage, parseColl
from selenium.webdriver.common.by import By

def scrapeAllBrands(driver, db_file):
    xpath = "//div[@id='collapseTwo']/div[@class='card-body']/div/a"
    brandLinks = scrapePageLinks(driver, xpath)
    parseColl(brandLinks, driver, db_file)

def scrapeAllLinks(driver, db_file, EC, WebDriverWait):
    try:
        pageCount = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(("xpath", '//div[@class="col-lg-8 col-md-6 col-12 mb-2"]/div/div[last()-1]/span[last()]'))
        )
        pageCount = pageCount.text
    except:
        print("Не пошло в scrapeAllLinks")
        return
    xpath = '//div[@class="col-12"]/div[@class="row"]/div[@class="col-xl-3 col-md-4 col-sm-6 col-12 mb-4"]/a'
    links = []
    articuls = []
    links += scrapePageLinks(driver, xpath)
    articuls += scrapePageArts(driver)
    i = 1
    for _ in range(int(pageCount) - 1):
        try:
            
            nextPageBtn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(("xpath", '//div[@class="col-lg-8 col-md-6 col-12 mb-2"]/div/div[last()]')))

            driver.execute_script("arguments[0].scrollIntoView();", nextPageBtn)
            driver.execute_script("arguments[0].click();", nextPageBtn)

            links += scrapePageLinks(driver, xpath)
            articuls += scrapePageArts(driver)
            i += 1
            print(i)

        except Exception as e:
            print(f"Error on page {i}: {str(e)}")
            break
    links += articuls
    half = len(links) // 2
    first_half = links[:half]
    second_half = links[half:]
    links = [[first_half[i], second_half[i]] for i in range(half)]
    print(f"Total links collected: {len(links)}")
    scrapeAllBrands(driver, db_file)
    parsePage(links, driver, db_file)