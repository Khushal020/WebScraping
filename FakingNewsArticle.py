import json
import logging
import time
import os
import csv

import requests
from tqdm import tqdm
from newspaper import Article
import sys



def crawl_link_article(url):
    result_json = None

    try:
        if 'http' not in url:
            if url[0] == '/':
                url = url[1:]
            try:
                article = Article('http://' + url)
                article.download()
                time.sleep(2)
                article.parse()
                flag = True
            except:
                logging.exception("Exception in getting data from url {}".format(url))
                flag = False
                pass
            if flag == False:
                try:
                    article = Article('https://' + url)
                    article.download()
                    time.sleep(2)
                    article.parse()
                    flag = True
                except:
                    logging.exception("Exception in getting data from url {}".format(url))
                    flag = False
                    pass
            if flag == False:
                return None
        else:
            try:
                article = Article(url)
                article.download()
                time.sleep(2)
                article.parse()
            except:
                logging.exception("Exception in getting data from url {}".format(url))
                return None

        if not article.is_parsed:
            return None

        visible_text = article.text
        top_image = article.top_image
        images = article.images
        keywords = article.keywords
        authors = article.authors
        canonical_link = article.canonical_link
        title = article.title
        meta_data = article.meta_data
        movies = article.movies
        publish_date = article.publish_date
        source = article.source_url
        summary = article.summary
        
        images = create_string(images)
        authors = create_string(authors)
        movies = create_string(movies)
        keywords = create_string(keywords)

        result_json = {'url': url, 'text': visible_text, 'images': images, 'top_img': top_image, 'keywords': keywords, 
                       'authors': authors, 'canonical_link': canonical_link, 'title': title, 'movies': movies, 
                       'publish_date': get_epoch_time(publish_date), 'source': source, 'summary': summary}
    except:
        logging.exception("Exception in fetching article form URL : {}".format(url))

    return result_json

def create_string(list):
    string = ''
    for i in list:
        string = string + str(i) + '\t'
    return string
	
def get_epoch_time(time_obj):
    if time_obj:
        return time_obj.timestamp()

    return None


def get_web_archieve_results(search_url):
    try:
        archieve_url = "http://web.archive.org/cdx/search/cdx?url={}&output=json".format(search_url)

        response = requests.get(archieve_url)
        response_json = json.loads(response.content)

        response_json = response_json[1:]

        return response_json

    except:
        return None


def get_website_url_from_arhieve(url):
    """ Get the url from http://web.archive.org/ for the passed url if exists."""
    archieve_results = get_web_archieve_results(url)
    if archieve_results:
        modified_url = "https://web.archive.org/web/{}/{}".format(archieve_results[0][1], archieve_results[0][2])
        return modified_url
    else:
        return None


def crawl_news_article(url):
    news_article = crawl_link_article(url)

    # If the news article could not be fetched from original website, fetch from archieve if it exists.
    if news_article is None:
        archieve_url = get_website_url_from_arhieve(url)
        if archieve_url is not None:
            news_article = crawl_link_article(archieve_url)

    return news_article




def load_news_file(source, label):
        maxInt = sys.maxsize
        while True:
            # decrease the maxInt value by factor 10
            # as long as the OverflowError occurs.
            try:
                csv.field_size_limit(maxInt)
                break
            except OverflowError:
                maxInt = int(maxInt / 10)

        news_list = []
        with open('{}_{}_links.csv'.format(source, label), encoding="UTF-8") as csvfile:
            reader = csv.reader(csvfile)
            for news in reader:
                news_list += news
                #print(news)
        return news_list
    
    
def collect_news_articles(news_list, source, label):
    
    save_dir = 'Data'

    for news in tqdm(news_list):
        news_article = crawl_news_article(news)
        if news_article:
            if not os.path.exists('{}/{}_{}.csv'.format(save_dir, source, label)):
                file = open('{}/{}_{}.csv'.format(save_dir, source, label),'w+', newline='')
                csv_file = csv.writer(file)
                csv_file.writerow(news_article.keys())
                file.close()
            file = open('{}/{}_{}.csv'.format(save_dir, source, label), 'a+', newline='')
            csv_file = csv.writer(file)
            csv_file.writerow(news_article.values())
            file.close()
            #json.dump(news_article,
             #         open("{}/{}/news content.json".format(save_dir, news.news_id), "w", encoding="UTF-8"))
                      


class NewsContentCollector():

    def __init__(self, source, label):
        self.source = source
        self.label = label
        

    def collect_data(self):
        news_list = load_news_file(self.source, self.label)
        collect_news_articles(news_list, self.source, self.label)
        
        
news_collector = NewsContentCollector('fakingnews', 'fake')

news_collector.collect_data()

