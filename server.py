from flask import Flask, jsonify, request
import requests
import openai
import json

# API Token for News API
api_token = 'pub_26157f3b6e196ac47cfe1ced03eabd82b11ef'

# Text Summarization Openai API setup
openai.api_type = "azure"
openai.api_base = "https://dbhackathonai9-openai.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = "YOUR-API-KEY"


app = Flask(__name__)

def call_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('Error occurred while fetching data')
        return None

# Function to ping the API to get news feed
def fetch_financial_data(keywords,from_date,to_date):
    newsData = []
    url = 'https://newsdata.io/api/1/news?apikey='+api_token+  '&from_date='+from_date+'&to_date='+to_date+'&language=en&'+'&q='
    url_dup = url
    for keyword in keywords:
        url += keyword
        print(url)
        data = call_api(url)
        if data:
            newsData.append(data)
        url = url_dup
    
    articlesContent = []
    for news in newsData:
        contents = news['results']
        for cont in contents:
            articlesContent.append(cont['content'])

    return (articlesContent)

# Endpoint for fetching data from keywords
@app.route('/fetchDataFromKeywords', methods=['POST'])
def fetch_data_from_keywords():
    data = request.get_json()
    keywords = data.get('keywords')
    from_date = data.get('from_date')
    to_date = data.get('to_date')
    fetchedNewsArticles = fetch_financial_data(keywords,from_date,to_date)
    return jsonify(fetchedNewsArticles)

# Endpoint for getting a summary for an article
@app.route('/getSummaryForArticle', methods=['POST'])
def get_summary_for_article():
    data = request.get_json()
    article_text = data.get('text')
    summary = openai.Completion.create(
        engine="gpt-35-turbo",
        prompt="Below is an extract from the annual financial report of a company. Summarize it.\n\n# Start of Report\n" + article_text,
        temperature=0.3,
        max_tokens=350,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)

    return summary

# Endpoint for paraphrasing text
@app.route('/paraphraseText', methods=['POST'])
def paraphrase_text():
    data = request.get_json()
    text = data.get('text')

    paraphrase = openai.Completion.create(
        engine="gpt-35-turbo",
        prompt="Paraphrase the following text -\n "+ text,
        temperature=0.3,
        max_tokens=350,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    return paraphrase

if __name__ == '__main__':
    app.run(debug=True)
