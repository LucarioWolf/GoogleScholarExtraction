from playwright.sync_api import sync_playwright, Playwright
import json

globalIndex = 0;

def run(playwright: Playwright):
    
    #Google scholar varibles
    titleCell = ".gsc_a_t"

    print("START CODE")

    #Open chrome and go to link
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()

    #Go to professor google scholar
    page.goto("https://scholar.google.com/citations?user=k12ONA8AAAAJ&hl=en&oi=ao")

    #Gets the screenshot of the page
    page.screenshot(path="example.png")

    """
    for row in page.get_by_role("link").all():
        print(row.text_content())
    """

    #All titles in link
    articleList = []

    #for all table data that has a title, get the title text and add it to list
    for row in page.locator(titleCell).filter(has=page.get_by_role("link")).all():
        title = row.get_by_role("link").text_content()
        #print(title)
        articleList.append(title)

    articleList.remove("Title")
    page.get_by_role("link", name= articleList[0]).click()

    authors = getDivValues(page, "Authors")
    date = getDivValues(page, "Publication date")
    publisher = getDivValues(page, "Publisher")
    description = getDivValues(page,"Description")

    print("Title: " + articleList[0])
    print("Authors: " + authors)
    print("Date: " + date)
    print("Publisher: " + publisher)
    print("Description: " + description)

    page.screenshot(path="thelink.png")


    #page.get_by_role("listitem").filter() has=page.get_by_role("heading", name="Product 2")).get_by_role("button", name="Add to cart").click()

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
        .and_(page.get_by_text(textLocator))
    )

    #Extract the data
    textValue = currentDiv.locator(valueDiv).text_content()

    #Return data
    return textValue
"""
def createJsonFile(page, currentTitle):
    emptyJSON = {
    "id" : None,
    "link" : None,
    "title" : None,
    "date" : None,
    "authors" : [],
    "topics" : [],
    "form" : "paper",
    "doi" : None,
    "publisher" : "PUBLISHER",
    "cites" : [],
    "summary" : ""
    }

    #Click to the link with the title
    page.get_by_role("link", name = currentTitle).click()

    #Get all nesscary data
    authors = getDivValues(page, "Authors")
    date = getDivValues(page, "Publication date")
    publisher = getDivValues(page, "Publisher")
    description = getDivValues(page,"Description")

    print("Title: " + articleList[0])
    print("Authors: " + authors)
    print("Date: " + date)
    print("Publisher: " + publisher)
    print("Description: " + description)
"""


with sync_playwright() as playwright:
    run(playwright)