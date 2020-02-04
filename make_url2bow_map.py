# -*- coding: utf-8 -*-
import argparse
import sys

from gensim.corpora.dictionary import Dictionary
import requests
from bs4 import BeautifulSoup
import MeCab
import matplotlib.pyplot as plt
from collections import Counter


def fetch_title_and_description(url, encoding="UTF-8", use_domain=False, timeout=3.0):
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
            return str(soup.title.string) + "\n" + meta_tag.get('content')
        else:
            return None
        
def doc2word_list(text):
    m = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    word_list = []
    for row in m.parse(text).split("\n"):
        word = row.split()[0]
        if word == "EOS":
            break
        pos = row.split()[-1]
        if "名詞-サ変接続" in pos or "数" in pos:
            continue
        if "名詞" in pos or "形容詞" in pos or "動詞" in pos:
            word_list.append(word)
    return word_list


def save_word_cnt():
    with open("word_cnt.txt","w") as wf:
        for word, cnt in word_cnt.items():
            wf.write("{}\t{}\n".format(word, cnt))
            
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_domain", action="store_true")
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    common_dict = Dictionary.load_from_text("./common_dic.txt")

    f = open("url2bow_map.csv", "a")
    for i, url in enumerate(sys.stdin):
        print("url " + str(i))
        text = fetch_title_and_description(url.strip(), use_domain=args.use_domain)
        if not text:
            continue
        
        word_list = doc2word_list(text)
        bow = common_dict.doc2bow(word_list)
        if bow:
            print(bow)
            for b in bow:
                f.write(url.strip() + "," + str(b[0]) + "," + str(b[1]) + "\n")
        if i % 100 == 99:
            f.close()
            f = open("url2bow_map.csv", "a")
    f.close()
            
if __name__ == "__main__":
    main()
