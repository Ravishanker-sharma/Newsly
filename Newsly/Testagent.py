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
    api_key="yourapi",
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
    if "json" in text:
        cleaned = re.sub(r"```json|```", "", text).strip()
    else:
        cleaned = re.sub(r"```python|```", "", text).strip()
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

instructions2 = '''You will get the news and the data of user on basis of these two you have to tell how the news will affect the user.
Write News in Hinglish language.
Keep the sequence of news same.
Summarize the affect on the user into 4 to 5 main bullet points.
You should look like you are telling the news directly to the user.
Avoid including irrelevant things in the Output.
Your headline will always remain same : ~Impact On You~ , bullets will change.
Format the response as a list of dictionaries like:
    [{"title":"Headline","Bullets":["point1","point2","point3"]},{"title":"Headline","Bullets":["point1","point2","point3"]}]
    ~ Do not return it like a Json , Handle it like a string
'''

llmwithtool = llm.bind_tools(tools)

# Agent initialization
agent = initialize_agent(
    llm=llmwithtool,
    tools=tools,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    agent_kwargs={"system_message": instructions},
    verbose=True
)

agent_for_custom = initialize_agent(
    llm=llm,
    tools=[],
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    agent_kwargs={"system_message": instructions2},
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

def get_user_profile(url):
    profile =""" Provide Profile Data
"""
    return profile

def customized_news(url,news):
    profile = get_user_profile(url)
    prompt = f"Instructions : {instructions2} , User data : {profile}, News:{news}"
    result2 = llm.invoke(prompt)
    # return result2.content
    return extract_json_from_llm_output(result2.content)

