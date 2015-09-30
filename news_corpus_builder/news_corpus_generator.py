from goose import Goose
import feedparser
from pprint import pprint
import sys
import os
import json
import io
from collections import defaultdict
import sqlite3
import string
import urllib


class NewsCorpusGenerator(object):

    def __init__(self,corpus_dir,datastore_type='file',db_name='corpus.db'):
        '''
        Read links and associated categories for specified articles 
        in text file seperated by a space

        Args:
            corpus_dir (str): The directory to save the generated corpus
            datastore_type (Optional[str]): Format to save generated corpus.
                                            Specify either 'file' or 'sqlite'.
            db_name (Optional[str]): Name of database if 'sqlite' is selected.
        '''

        self.g = Goose({'browser_user_agent': 'Mozilla','parser_class':'soup'})
        #self.g = Goose({'browser_user_agent': 'Mozilla'})
        self.corpus_dir = corpus_dir
        self.datastore_type = datastore_type
        self.db_name = db_name
        self.stats = defaultdict(int)

        self._create_corpus_dir(self.corpus_dir)

        self.db = None
        if self.datastore_type == 'sqlite':
            self.db = self.corpus_dir + '/' + self.db_name
            self._set_up_db(self.db)

    def _create_corpus_dir(self,directory):

        if not os.path.exists(directory):
            os.makedirs(directory)


    def read_links_file(self,file_path):
        '''
        Read links and associated categories for specified articles 
        in text file seperated by a space

        Args:
            file_path (str): The path to text file with news article links
                             and category

        Returns:
            articles: Array of tuples that contains article link & cateogory
                      ex. [('IPO','www.cs.columbia.edu')]
        '''

        articles = []
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                #Ignore blank lines
                if len(line) != 0:
                    link,category = line.split(' ')
                    articles.append((category.rstrip(),link.strip()))

        return articles

    def generate_corpus(self,articles):
        
        # TODO parallelize extraction process
        print 'Extracting  content from links...'

        for article in articles:
            category = article[0]
            link = article[1]

	    ex_article = None

	    try:
            	ex_article = self.g.extract(url=link)
	    except Exception:
		print('failed to extract article..')
		continue

            ex_title = ex_article.title
            ex_body = ex_article.cleaned_text
	    #print ex_title
            #print ex_body
            #sys.exit(1)

            if ex_body == '':
                self.stats['empty_body_articles'] += 1
                continue

            self._save_article({'title':ex_title, 'body': ex_body,
                'category':category})

    def _save_article(self,clean_article):

        print "Saving article %s..." %(clean_article['title'])

        if self.datastore_type == 'file':
            self._save_flat_file(clean_article)
        elif self.datastore_type == 'sqlite':
            self._save_to_db(clean_article)
        else:
            raise Exception("Unsupported datastore type. Please specify file or sqlite")

    def _remove_punctuations(self,title):
        # TODO optimize for python 3
        #title.translate(title.maketrans("",""), string.punctuation)
        return "".join(char for char in title if char not in string.punctuation)

    def _save_flat_file(self,clean_article):

        directory = self.corpus_dir + '/' + clean_article['category']

        # create category directory
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = directory + '/' + \
        self._remove_punctuations(clean_article['title']).replace(" ","_") + '.json'

        with io.open(file_name, 'w', encoding='utf-8') as f:
              f.write(unicode(json.dumps(clean_article, ensure_ascii=False)))

    def _encode_query(self,query):
        # TODO Python 3 urllib.parse.quote 
        return urllib.quote(query)


    def google_news_search(self,query,category_label,num=50):
        '''
        Searches Google News.
        NOTE: Official Google News API is deprecated https://developers.google.com/news-search/?hl=en
        NOTE: Google limits the maximum number of documents per query to 100.
              Use multiple related queries to get a bigger corpus. 

        Args:
            query (str): The search term.
            category_label (str): The category to assign to the articles. These
                                  categories are the labels in the generated corpus

            num (Optional[int]): The numnber of results to return.

        Returns:
            articles: Array of tuples that contains article link & cateogory
                      ex. [('IPO','www.cs.columbia.edu')]
        '''

        url = 'https://news.google.com/news?hl=en&q='+self._encode_query(query) \
                +'&num='+str(num)+'&output=rss'

        rss = feedparser.parse(url)
        entries = rss['entries']
        articles = []

        for entry in entries:
            link = entry['link']
            articles.append((category_label,link))
        return articles

    def _set_up_db(self,db):

        if os.path.exists(db):
            print 'Database exists, assume schema does, too.'
        else:
            print 'Need to create schema'
            print 'Creating schema...'
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute("create table articles (Id INTEGER PRIMARY KEY,category, title,body)")
            cur.execute("CREATE UNIQUE INDEX uni_article on articles (category,title)")
            conn.close()

    def _save_to_db(self,clean_article):
        
        conn = sqlite3.connect(self.db)
        with conn:
            cur = conn.cursor()   
            try:
                cur.execute("INSERT INTO articles (Id,category,title,body)\
                    VALUES(?, ?, ?,?)",(None,clean_article['category'],clean_article['title'],clean_article['body']))
            except sqlite3.IntegrityError:
                self.stats['not_insert_db'] += 1
                print 'Record already inserted with title %s ' %(clean_article['title'])

    def get_stats(self):
        return self.stats


if __name__ == '__main__':
    pass
