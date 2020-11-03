import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
from collections import Counter
from utils import UtilsFunction
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def readTxtFile(fileToParse):
    file = open(fileToParse , "r")
    gen_list = file.read().splitlines()
    print(gen_list)
    file.close()
    return gen_list

def createDirectory(name):
    try:
        os.mkdir(name)
    except OSError:
        pass
    else:
        print("Successfully created the directory!")


class SiteScrapper:
    article_title = list()
    article_text = list()
    articles = dict()
    dictionary = dict()

    def __init__(self, urls):
        self.urls = urls

    def m_get_article_title(self, soup):
        article_title = [p.text for p in soup.find(class_="column").find_all('h1')]
        return article_title

    def m_get_article_text(self,soup):
        article_text = [p.text for p in soup.find(class_="node-article").find_all('p')]
        return article_text

    def m_sites_data_to_soup(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, "lxml")
        r_title = self.m_get_article_title(soup)
        r_text = self.m_get_article_text(soup)
        for i, c in enumerate(r_title):
            self.dictionary.update({r_title[i]: r_text})
        return self.dictionary

    def m_get_article_pages_info(self):
        self.articles = [self.m_sites_data_to_soup(url) for url in self.urls]

    def m_save_articles_to_txt_file(self):
        for key in self.articles:
            for ele in key:
                with open("transcripts/article_" + str(ele) + ".txt", "w+") as file:
                    file.writelines(key.get(ele))

    def m_load_article_from_txt_file(self):
        data = {}
        for key in self.articles:
            for ele in key:
                with open("transcripts/article_" + str(ele) + ".txt","r+") as file:
                    data[ele] = key.get(ele)
        return data


def main():
    createDirectory("transcripts")
    urls = readTxtFile("Articles.txt")
    scrapper = SiteScrapper(urls)
    scrapper.m_get_article_pages_info()
    scrapper.m_save_articles_to_txt_file()
    data = scrapper.m_load_article_from_txt_file()

    utils = UtilsFunction()

    data_combined = {key: [utils.textCombination(value)] for (key, value) in data.items()}
    pd.set_option('max_colwidth', 150)
    data_df = pd.DataFrame.from_dict(data_combined).transpose()
    data_df.columns = ['story']

    # CLEANING DATA 1
    text_round = lambda x: utils.clean_text_round(x)
    data_clean = pd.DataFrame(data_df.story.apply(text_round))

    # CLEANING DATA 2
    text_round2 = lambda x: utils.clean_text_round_second(x)
    data_clean2 = pd.DataFrame(data_clean.story.apply(text_round2))

    # Exclude common English stop words
    cv = CountVectorizer(stop_words="english")
    data_cv = cv.fit_transform(data_clean2.story)
    # Split text to single words
    data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
    data_dtm.index = data_clean2.index
    data_dtm.to_pickle("dtm.pkl")
    data_clean2.to_pickle("data_clean.pkl")


    ###### LOAD DATA
    data = pd.read_pickle('dtm.pkl')
    data = data.transpose()
    #print(data.head())

    # Find the top 30 words in each article
    top_article_words = {}
    for c in data.columns:
        top = data[c].sort_values(ascending=False).head(30)
        top_article_words[c] = list(zip(top.index, top.values))

    # Print the top 15 words in each article
    for article, top_words in top_article_words.items():
        print(article)
        # print(', '.join([word for word, count in top_words[0:14]]))
        # print('---')

    words = []
    for art in data.columns:
        top = [word for (word, count) in top_article_words[art]]
        for t in top:
            words.append(t)
    print("=====================================")

    add_stop_words = [word for word, count in Counter(words).most_common() if count > 6]
    # print(add_stop_words)

    data_clean = pd.read_pickle('data_clean.pkl')
    stop_words = text.ENGLISH_STOP_WORDS.union(add_stop_words)
    cv = CountVectorizer(stop_words=stop_words)


    data_cv = cv.fit_transform(data_clean.story)
    data_stop = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
    data_stop.index = data_clean.index
    pickle.dump(cv, open("cv_stop.pkl", "wb"))
    data_stop.to_pickle("dtm_stop.pkl")
    wc = WordCloud(stopwords=stop_words, background_color="white", colormap="Dark2",
                   max_font_size=150, random_state=42)


    plt.rcParams['figure.figsize'] = [16, 6]


    # Create subplots for each comedian
    for index, comedian in enumerate(data.columns):
        wc.generate(data_clean.story[comedian])

        plt.subplot(3, 4, index + 1)
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        # plt.title(full_names[index])

    plt.show()


if __name__ == "__main__":
    main()

