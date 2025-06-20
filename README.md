# 📰 Newsly - AI Powered Hinglish News Assistant

**Newsly** is an AI-powered desktop application that delivers real-time news in both English and conversational Hindi ("Hinglish"). It combines web scraping, large language models, and text-to-speech synthesis to provide a multilingual, chat-based news experience.

## 🚀 Features

- 🔍 **Real-Time News Fetching** via scraping Hindustan Times and Yahoo search results.
- 🤖 **AI Chatbot** interface to interact with news and ask follow-up questions.
- 🧠 **LangChain + Gemini 2.0 Flash** powered agents for summarization, translation, and conversational memory.
- 🗣️ **Text-to-Speech in Hindi** for accessibility and immersive experience.
- 🎛️ **CustomTkinter UI** with chat-based interaction and voice playback controls.

## 📂 Project Structure

Newsly/
├── Newsly_main.py # Main app: news dashboard and interaction
├── NewsChat.py # Chat UI with AI and voice integration
├── Testagent.py # News summarization agent setup
├── genralscraper.py # Web scraping + Yahoo search powered tool
├── hindustandscaper.py # Specific scraper for Hindustan Times
├── hinditexttospeach.py # Hindi TTS using gTTS + pygame
├── yahoosearchengine.py # Yahoo search engine URL parser


## 🧠 How It Works

1. **Scraping**: Fetches real-time news articles from Hindustan Times or through Yahoo search.
2. **Summarization**: Uses Gemini-2 LLM to generate Hinglish news summaries with bullet points.
3. **Chat Mode**: Users can ask questions about specific news, and the chatbot answers factually using scraped content.
4. **Translation & Voice**: AI translates responses into casual Hindi and reads them aloud using TTS.

## 🛠️ Tech Stack

- **Python 3.10+**
- [LangChain](https://www.langchain.com/)
- [Google Gemini (Generative AI)](https://ai.google.dev/)
- [gTTS](https://pypi.org/project/gTTS/)
- **CustomTkinter** for modern UI

## 🎬 How to Run

### 1. Clone the repo:
```bash
git clone https://github.com/Ravishanker-sharma/Newsly
cd newsly
```
```
2. Install dependencies:
pip install -r requirements.txt
3. Run the app:
python Newsly_main.py
```
```
🔑 API Key Setup
Make sure to set your Google Generative AI API Key in:
Testagent.py
NewsChat.py
```
```
Replace:
api_key="YOUR_API_KEY"
```
## 🔄 Recent Enhancements (20 June 2025)

Newsly has recently been upgraded with major improvements to both functionality and intelligence:

- 🧠 **Conversational Memory in Chat**  
  The NewsChat module now retains context throughout a session, allowing it to answer follow-up questions naturally — just like a real assistant.

- 👤 **Impact-Based Personalization**  
  A second AI agent was added to assess how a news story might affect the user, based on their LinkedIn profile data (currently simulated; LinkedIn integration is under development).

- ⚙️ **Smart Tool Invocation**  
  NewsChat no longer fetches data blindly. It evaluates whether it already has enough context and only uses web scraping tools when truly needed — making the system faster and more efficient.

These enhancements move Newsly closer to the experience offered by apps like **Headlyne**, which inspired this project.


## Images
![image](https://github.com/user-attachments/assets/7bd26947-a179-4703-9721-0283a5d72e8c)
![image](https://github.com/user-attachments/assets/52a28448-85d4-4a2a-9116-4c64c03f5f2e)

## Newsly Updated Image
![image](https://github.com/user-attachments/assets/508b550e-506b-41a1-9067-371847400af1)

