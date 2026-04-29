from playwright.sync_api import sync_playwright, Playwright, TimeoutError as PlaywrightTimeoutError
import json

globalIndex = 0

def run(playwright: Playwright):
    
    #Google scholar varibles
    titleCell = ".gsc_a_t"

    print("START CODE")

    #Open chrome and go to link
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()
    page.set_default_timeout(3000)

    #Go to professor google scholar
    page.goto("https://scholar.google.com/citations?user=k12ONA8AAAAJ&hl=en&oi=ao")

    #Gets the screenshot of the page
    page.screenshot(path="example.png")

    reloadPage(page)

    #All titles in link
    articleList = []

    
    #for all table data that has a title, get the title text and add it to list
    for row in page.locator(titleCell).filter(has=page.get_by_role("link")).all():
        title = row.get_by_role("link").text_content()
        #print(title)
        articleList.append(title)

    articleList.remove("Title")

    for currentArticle in articleList:
        createJsonFile(page, currentArticle)
        print("Article " + str(globalIndex) + ": " + currentArticle)
    
    
    
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
def createJsonFile(page, currentTitle):
    
    global globalIndex

    #Click to the link with the title
    page.get_by_role("link", name = currentTitle, exact=True).first.click()

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

    globalIndex += 1

    page.go_back()
    reloadPage(page)
    

def reloadPage(page):
    showMoreButton = page.get_by_role("Button", name="Show More")
    while(showMoreButton.is_enabled()):
        showMoreButton.click(no_wait_after=False)
        page.wait_for_timeout(1000);
    
    

with sync_playwright() as playwright:
    run(playwright)