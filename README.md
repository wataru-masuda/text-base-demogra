# text-base-demogra

##  これは何？

ユーザの行動（訪問したurl）履歴からコンテンツ情報をスクレイピングにより抜き出し、次元圧縮等を施したものをそのユーザの特徴量として機械学習モデルの入力等に用いる。

## Requirements

- gensim

- Mecab

  ```shell
  brew install mecab mecab-ipadic git curl xz # 必要なもののみインストールする
  git clone --depth 1 git@github.com:neologd/mecab-ipadic-neologd.git
  cd mecab-ipadic-neologd
  ./bin/install-mecab-ipadic-neologd -n
  ```

- beautifulsoup4



## 特徴量の作成手順

1. urlのリストから単語の辞書を作成する。

   ```shell
   cat sample_urllist.txt | pipenv run python make_common_dict.py
   ```

   

2. 単語辞書から不要な単語を除く（1でストップワードとして弾く処理を入れた方がいいかも）。

3. urlとBoW (Bag of Words) のマップを作る。

   ```shell
   cat sample_urllist.txt | pipenv run python make_url2bow_map.py
   ```

   

4. 3で作成した`url2bow.csv`を参照して、bqテーブルを作成する。

5. ユーザ行動履歴`masuda_partial_data.auction_user_actions_YYYYmmdd`テーブルと4で作成したテーブルから、gidごとのBoWを作成する。

6. LDAモデルでgidごとのBoWからgidごとの特徴量 (10~20dim?) に変換する。





