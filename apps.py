import streamlit as st
import nltk
import bs4 as bs
import urllib.request
import re


def load_css(file_name:str)->None:
    """
    Function to load and render a local stylesheet
    """
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css('style.css')
st.title ('Summarizing Your Article')
# url = 'https://www.esquire.com/uk/culture/advice/a9641/things-men-dont-know-about-women-caitlin-moran/'

url = st.text_input("Url",value="insert url here")

if url is not 'insert url here':
    scrabed_data = urllib.request.urlopen(url)
    article =scrabed_data.read()

    parsed_article = bs.BeautifulSoup(article,'lxml')

    paragraphs = parsed_article.find_all('p')
    article_text = ""
    for p in paragraphs:
        article_text += p.text



    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)



    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)



    sentence_list = nltk.sent_tokenize(article_text)


    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1


    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)



    sentence_score = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_score.keys():
                        sentence_score[sent] = word_frequencies[word]
                    else:
                        sentence_score[sent] += word_frequencies[word]


    import heapq
    def load_css(file_name:str)->None:
    load_css('style.css')
    sentences = st.slider('Please choose the number of sentences to display',min_value= 5,max_value= 30, value=10, step=1, key = 'First Slider')
    summary_sentences = heapq.nlargest(sentences, sentence_score, key=sentence_score.get)

    summary = ' '.join(summary_sentences)

    st.write(summary)