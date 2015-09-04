from news_corpus_builder import NewsCorpusGenerator
from pprint import pprint
import sys
file_path = '/Users/skillachie/hand_selected_articles.txt'
corpus_dir = '/Users/skillachie/finance_corpus'

category_total = 300

article_links = []
ex = NewsCorpusGenerator(corpus_dir,'sqlite')

# Add hand selected articles 
article_links.extend(ex.read_links_file(file_path))


def get_links(terms,category):
    category_articles = []
    article_count = int(category_total/len(terms))
    for term in terms:
        category_articles.extend(ex.google_news_search(term,category,article_count))
    return category_articles


# Policy Articles
policy_terms = ['SEC','monetary','fed','fiscal']
policy = get_links(policy_terms,'Policy')
print len(policy)
article_links.extend(policy)

# International Finance 
if_terms = ['global finance','imf','ECB','RMB devaluation','international finance']
if_a = get_links(if_terms,'International_Finance')
print len(if_a)
article_links.extend(if_a)
#sys.exit(1)

# Economy 
eco_terms = ['GDP','jobs','unemployment','housing','economy']
eco = get_links(eco_terms,'Economy')
print(len(eco))
article_links.extend(eco)

# Capital
capital_terms = ['IPO','equity','initial public offering','equity capital']
capital = get_links(capital_terms,'Capital')
print(len(capital))
article_links.extend(capital)

# Real Estate
real_estate_terms = ['real estate']
rel_es = get_links(real_estate_terms,'Real_Estate')
print len(rel_es)
article_links.extend(rel_es)

# Mergers & Acquisitions
ma_terms = ['merger','acquisition','mergers','acquisitions']
ma = get_links(ma_terms,'Mergers_Acquisitions')
print(len(ma))
article_links.extend(ma)

# Oil
oil_terms = ['oil','oil prices','natural gas price']
oil = get_links(oil_terms,'Oil')
print len(oil)
article_links.extend(oil)

# Commodities
commodities_terms = ['silver','gold','commodities']
commo = get_links(commodities_terms,'Commodities')
print len(commo)
article_links.extend(commo)


# Fraud & Insider Trading
fraud_terms = ['insider trading','Ponzi Scheme','finance fraud']
fraud = get_links(fraud_terms,'Fraud')
print len(fraud)
article_links.extend(fraud)

# Litigation 
lit_terms = ['company settlement','company litigation','company lawsuit']
lit = get_links(lit_terms,'Litigation')
print len(lit)
article_links.extend(lit)

# Earning Reports
er_terms = ['earning reports','quarterly results','financial statement']
er = get_links(er_terms,'Earning_Reports')
print len(er)
article_links.extend(er)

# Extract Content & Create Corpus
print "Total %d links to extract" % len(article_links)
ex.generate_corpus(article_links)
print ex.get_stats()
