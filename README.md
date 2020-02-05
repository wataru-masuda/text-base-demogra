# text-base-demogra

##  これは何？

ユーザの行動（訪問したurl）履歴からコンテンツ情報をスクレイピングにより抜き出し、そのユーザの特徴量として機械学習モデルの入力等に用いる。

作成手順は以下の通り。

1. urlのリストから単語の辞書を作成する。

   ```shell
   cat sample_urllist.txt | python make_common_dict.py
   ```

   

2. 単語辞書から不要な単語を除く（1でストップワードとして弾く処理を入れた方がいいかも）。

3. urlとBoWのマップを作る。

   ```shell
   cat sample_urllist.txt | python make_url2bow_map.py
   ```

   

4. 作成中...



