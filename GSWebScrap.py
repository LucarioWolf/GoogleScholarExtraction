from playwright.sync_api import sync_playwright, Playwright, TimeoutError as PlaywrightTimeoutError
import json
import random

globalIndex = 0

def run(playwright: Playwright):
    
    #Google scholar varibles
    titleCell = ".gsc_a_t"

    url = "https://scholar.google.com/citations?user=k12ONA8AAAAJ&hl=en&oi=ao"

    

    print("START CODE")

    #Open chrome and go to link
    chromium = playwright.chromium
    browser = chromium.launch(
        headless= False, 
    )
    
    page = browser.new_page()
    page.set_default_timeout(3000)

    #Go to professor google scholar
    page.goto(url, wait_until="domcontentloaded", timeout=6000)

    #Gets the screenshot of the page
    page.screenshot(path="example.png")

    reloadPage(page)

    #All titles in link
    articleList = []
    linkAddresses = []

    with open("articles.json", "w", encoding="utf-8") as jsonFile:
        jsonFile.write("[")
        jsonFile.close

    
    #for all table data that has a title, get the title text and add it to list
    for row in page.locator(titleCell).filter(has=page.get_by_role("link")).all():
        title = row.get_by_role("link").text_content()
        linkAddress = row.get_by_role("link").get_attribute("href")
        #print(title)
        articleList.append(title)
        linkAddresses.append(linkAddress)

    articleList.remove("Title")
    linkAddresses.pop(0)   

    for currentArticle, currentLink in zip(articleList, linkAddresses):
        createJsonFile(page, currentArticle, currentLink)
        print("Article " + str(globalIndex) + ": " + currentArticle)
    

    with open("articles.json", "a", encoding="utf-8") as jsonFile:
        jsonFile.write("]")
        jsonFile.close

    

    
    
    page.screenshot(path="thelink.png")

    #Gets the HTMl of the page
    html = page.content();
    #print(html);

    browser.close()

#Get article data by div
def getDivValues(page, textLocator):

    #All classes in article page
    articleDiv = ".gs_scl"
    fieldDiv = ".gsc_oci_field"
    valueDiv = ".gsc_oci_value"

    #get the div containing the data
    currentDiv = page.locator(articleDiv).filter(
        has=page.locator(fieldDiv)
        .and_(page.get_by_text(textLocator, exact=True))
    )

    #Extract the data
    try:
        textValue = currentDiv.locator(valueDiv).text_content()
    except PlaywrightTimeoutError:
        return None

    #Return data
    return textValue

#Create a json file of an article
def createJsonFile(page, currentTitle, currentLink):
    
    global globalIndex

    #Click to the link with the title
    #page.get_by_role("link", name = currentTitle, exact=True).first.click()
    page.goto("https://scholar.google.com" + currentLink, wait_until="domcontentloaded", timeout=6000)

    #Get all nesscary data
    authors = getDivValues(page, "Authors")

    if(authors != None):
        authors = authors.split(", ")

    date = getDivValues(page, "Publication date")
    publisher = getDivValues(page, "Publisher")
    description = getDivValues(page,"Description")
    url = page.url

    newJson = {
        "id" : globalIndex,
        "link" : url,
        "title" : currentTitle,
        "date" : date,
        "authors" : authors,
        "topics" : [],
        "form" : "paper",
        "doi" : None,
        "publisher" : publisher,
        "cites" : [],
        "summary" : description
    }
    with open("articles.json", "a", encoding="utf-8") as articleFile:
        json.dump(newJson, articleFile, indent=4)
        articleFile.write(",")

    globalIndex += 1

    '''
    page.go_back()
    reloadPage(page)
    '''

def reloadPage(page):
    showMoreButton = page.get_by_role("Button", name="Show More")
    while(showMoreButton.is_enabled()):
        showMoreButton.click(no_wait_after=False)
        page.wait_for_timeout(2000);
    #page.wait_for_timeout(random.randint(3000, 30000));
    
    

with sync_playwright() as playwright:
    run(playwright)