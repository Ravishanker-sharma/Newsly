from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from Newsly.genralscraper import smart_scrape
from langchain.agents import tool
from Newsly.hindustandscaper import scrape_ht_world_news_page
from typing import Dict, List
import json
import re

# Google Gemini LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key="AIzaSyA-Dk7dhyut4IZHFLBTSzQcC_tAaYwYqoU",
    temperature=0.5
)

@tool
def format(response:List[Dict[str,List[str]]]):
    """

    :param response: Uses Json format then print response
                    Example Input: [{"title":"Headline","Bullets":["point1","point2","point3"]},{"title":"Headline","Bullets":["point1","point2","point3"]}]
    :return: Returns response
    """
    print(response)


def extract_json_from_llm_output(text):
    # Remove Markdown code fences (```json or ```), if present
    cleaned = re.sub(r"```json|```", "", text).strip()
    try:
        data = json.loads(cleaned)
        return data
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return []

# Register tools
tools = [format]

# Agent prompt instructions
instructions = """You are a News agent which summarizes the news on the basis of provided data.
Write News in Hinglish language.
Summarize the news into headlines and 4 to 5 main bullet points.
Avoid including irrelevant things in the Output.
Make Different headlines and different points for different News.
Do not make Headline: other news.
Format the response as a list of dictionaries like:
    [{"title":"Headline","Bullets":["point1","point2","point3"]},{"title":"Headline","Bullets":["point1","point2","point3"]}]
    ~ Do not return it like a Json , Handle it like a string
"""

llmwithtool = llm.bind_tools(tools)

# Agent initialization
agent = initialize_agent(
    llm=llmwithtool,
    tools=tools,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    agent_kwargs={"system_message": instructions},
    verbose=True
)
r=0
links=[]
# Scrape and prepare input
def genrate_data():
    global r, links
    if not links:
        r = r + 1
        print("Processing Page Number :",r)
        links = list(set(scrape_ht_world_news_page(r)))
    data = []
    for link in links[:5]:
        print("Scraping:", link)
        try:
            rawdata = smart_scrape(link)
            data.append(rawdata)
        except Exception as e:
            print(f"Error scraping {link}: {e}")
    del links[:5]
    return data


# Call agent with formatted input
def get_ai_news():
    content = genrate_data()
    full_prompt = f"{instructions}\n{content}"
    result = llmwithtool.invoke(full_prompt)
    return extract_json_from_llm_output(result.content)

