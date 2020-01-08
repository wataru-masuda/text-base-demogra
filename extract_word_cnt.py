# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import MeCab
import matplotlib.pyplot as plt
from collections import Counter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--use_domain", action="store_true")
parser.add_argument("-w", "--create_wordcloud", action="store_true")
args = parser.parse_args()

word_list = []
word_cnt = Counter()

def get_title_and_description_of_webpage(encoding="UTF-8", use_domain=False):
    for url in sys.stdin:
        print(url.strip())
        try:
            res = requests.get("http://"+url.strip()) if use_domain else requests.get(url.strip(), timeout=3.0)
        except Exception:
            print("GET request failed")
            continue
        res.encoding = encoding
        soup = BeautifulSoup(res.text, 'html.parser')
        
        for meta_tag in soup.find_all('meta', attrs={'name': 'description'}):
            if soup.title:
                yield str(soup.title.string) + "\n" + meta_tag.get('content')
            else:
                yield None

def parse_text(text):
    m = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    for row in m.parse(text).split("\n"):
        word = row.split()[0]
        if word == "EOS":
            break
        pos = row.split()[-1]
        if "名詞-サ変接続" in pos or "数" in pos:
            continue
        if "名詞" in pos or "形容詞" in pos or "動詞" in pos:
            word_list.append(word)
            word_cnt.update([word])

            
def main():
    for i, text in enumerate(get_title_and_description_of_webpage(use_domain=args.use_domain)):
        print("url " + str(i))
        if text:
            parse_text(text)

    with open("word_cnt.txt","w") as wf:
        for word, cnt in word_cnt.items():
            wf.write("{}\t{}\n".format(word, cnt))


if __name__ == "__main__":
    main()
