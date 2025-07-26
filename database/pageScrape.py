
def scrapePageLinks(driver):
    links_sel = driver.find_elements("xpath", '//div[@class="col-12"]/div[@class="row"]/div[@class="col-xl-3 col-md-4 col-sm-6 col-12 mb-4"]/a')
    links = []

    for elem in links_sel:
        href = elem.get_attribute("href")
        if href:
            links.append(href)

    print(f"Extracted {len(links)} links:")
    print(links)

    return links
    