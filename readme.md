**How to use:**<br/>
Just run:
```
python3.5 arXiv-metadata-extract.py '2019-11-19' '2019-11-22'
python3.5 arXiv-metadata-embetter.py
```
First script downloads all the articles from arXiv via its API and creates xml file; second script makes a neat html out of xml.<br/>
'2019-11-19' '2019-11-22' means range of data (both inclusive).  If you want only one date, you can omit second date.<br/>
Feel free to change your own preferences (of what articles are of interest to you) in the second script.<br/>

**Possible errors:**
(1) If you see too few articles, then change two first lines in second script (current month). <br/>
(2) On some systems, scripts don't work until you change file paths to global. <br/>

**Other notes:**
Files "arXiv-metadata-extract-for-prediction.py" and "xgboost_on_articles_data.py" are not involved in what described above; 
they are separate project trying to predict importance of articles based on already existing database (with my subjective labels of importance).<br/>
Files "arXiv-articles.html" and "arXiv-articles.xml" are given for illustrative purposes. You can open first file in any browser.<br/>

**Credits:**
Much of content for downloading arXiv metadata has been taken from https://github.com/rocksonchang/arXiv-metadata