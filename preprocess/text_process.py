# -*- coding: utf-8 -*-
import requests
import sys

from gensim.corpora.dictionary import Dictionary
from bs4 import BeautifulSoup
import MeCab


def fetch_contents_from_url(url, encoding="UTF-8", use_domain=False, timeout=3.0):
    try:
        res = requests.get("http://"+url, timeout=timeout) if use_domain else requests.get(url, timeout=timeout)
    except Exception:
        print("GET request failed")
        return None

    res.encoding = encoding
    try:
        soup = BeautifulSoup(res.text, 'html.parser')
    except Exception:
        print("failed to parse html text")
        return None
        
    for meta_tag in soup.find_all('meta', attrs={'name': 'description'}):
        if soup.title:
            return str(soup.title.string) + "\n" + str(meta_tag.get('content'))
        else:
            return None
        
def doc2word_list(text):
    m = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

    with open("/Users/wataru-masuda/Documents/src/github/text-base-demogra/preprocess/stopwords.txt", "r") as f:
        stopwords = set(w.strip() for w in f.readlines())
    word_list = []
    for row in m.parse(text).split("\n"):
        word = row.split()[0]
        if word == "EOS":
            break
        pos = row.split()[-1]
        if "名詞-サ変接続" in pos or "数" in pos:
            continue
        if len(word) == 1:
            continue
        if word in stopwords:
            continue
        if "名詞" in pos or "形容詞" in pos or "動詞" in pos:
            word_list.append(word)
    return word_list
