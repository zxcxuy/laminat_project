
def scrapePageLinks(driver, xpath):
    links_sel = driver.find_elements("xpath", xpath)
    links = []

    for elem in links_sel:
        href = elem.get_attribute("href")
        if href:
            links.append(href)

    # print(f"Extracted {len(links)} links")

    return links

def scrapePageArts(driver):
    arts_sel = driver.find_elements("xpath", "//div[@class='card-title card-size-middle ccolor']/h6")
    arts = []

    for elem in arts_sel:
        art = elem.text
        if art:
            arts.append(art)
    
    # print(f"Extracted {len(arts)} arts")

    return arts
