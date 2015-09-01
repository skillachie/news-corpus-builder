#from distutils.core import setup
from setuptools import setup, find_packages
#import setuptools

setup(
    name='news-corpus-builder',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    #zip_safe=False,
    #package_dir={'news_corpus_generator': 'news_corpus_generator'},
    author='Dwayne V Campbell',
    author_email='dwaynecampbell13 _at_ gmail.com',
    description='Quickly build a news/web corpus with specifc topics or terms automatically from Google News or by specifying \
                article links in a file. This module automatically extracts the body and title from each article and saves\
                the result to either flatfiles or sqlite database.',
    long_description=open('README.md').read(),
    url='https://github.com/skillachie/news_corpus_builder',
    download_url='https://github.com/skillachie/news_corpus_builder',
    keywords='corpus, nlp news,extractor,web scrapping, natural language processing'.split(','),
    license='MIT License',
    install_requires=[
        "goose-extractor >= 1.0.25",
        "feedparser >= 5.2.1"
                     ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering',
      ]
 )

