
import requests
from url_to_llm_text.get_html_text import get_page_source   # you can also use your own code or other services to get the page source
from url_to_llm_text.get_llm_input_text import get_processed_text   # pass html source text to get llm ready text
import asyncio

async def main():
    url = "https://www.ikea.com/in/en/cat/corner-sofas-10671/"

    # get page html source text using this library function or any other means
    page_source = await get_page_source(url)

    # get llm ready text and pass the text to your LLM prompt template
    llm_text = await get_processed_text(page_source, url)

    # prompt template
    prompt_format = """extract the product name, product link, image link and price for all the products given in the below webpage. The format should be:
    {{
    "1": {{
            "Product Name": ,
            "Product Link": ,
            "Image Link": ,
            "Price":
            }},
    "2": {{
            "Product Name": ,
            ...
            }},
    }}

    webpage:
    {llm_friendly_webpage_text}
    """

    # calculate tokens and truncate the llm_text to fit your model context length and your requirements. sometimes you may need only initial part of the webpage.
    # below we are manually truncating to 40000 characters. create a seperate function as per your need.
    prompt = prompt_format.format(llm_friendly_webpage_text=llm_text[:40000])

    api_key = "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"
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }
    payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            }
    ]}],
    'seed': 0,
    "temperature": 0,
    "top_p": 0.001,
    # "max_tokens": 1024, # if you want to limit the output tokens. this may keep the output json structure incomplete.
    "n": 1,
    "frequency_penalty": 0, "presence_penalty": 0
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json()['choices'][0]['message']['content'])

asyncio.run(main())