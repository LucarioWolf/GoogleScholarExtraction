from playwright.sync_api import sync_playwright, Playwright, TimeoutError as PlaywrightTimeoutError
import json
import random

globalIndex = 0

def run(playwright: Playwright):
    

    url = "https://borisk.dreamhosters.com/public_html//cv/publ.htm"

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
    page.screenshot(path="example2.png")


    #All titles in link
    articleList = []
    linkAddresses = []

    with open("articlesWeb.json", "w", encoding="utf-8") as jsonFile:
        jsonFile.write("[")
        jsonFile.close

    webVar = ".MsoListParagraph"

    for citation in page.locator(webVar).all():
       text = citation.inner_text()
       print(text)

    
    

    with open("articlesWeb.json", "a", encoding="utf-8") as jsonFile:
        jsonFile.write("]")
        jsonFile.close

    

    
    
    page.screenshot(path="thelink.png")

    #Gets the HTMl of the page
    html = page.content();
    #print(html);

    browser.close()


#Create a json file of an article
def createJsonFile(page, currentTitle, currentLink):
    
    global globalIndex

    #Click to the link with the title
    #page.get_by_role("link", name = currentTitle, exact=True).first.click()
    page.goto("https://scholar.google.com" + currentLink, wait_until="domcontentloaded", timeout=6000)

    #Get all nesscary data

    if(authors != None):
        authors = authors.split(", ")

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
    with open("articlesWeb.json", "a", encoding="utf-8") as articleFile:
        json.dump(newJson, articleFile, indent=4)
        articleFile.write(",")

    globalIndex += 1

    '''
    page.go_back()
    reloadPage(page)
    '''  
    

with sync_playwright() as playwright:
    run(playwright)