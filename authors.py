import nltk
import spacy
import mysql.connector as mysql
import traceback
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize
import re

nlp = spacy.load("en_core_web_sm")

#for the entities, we need the title and body of the article and the database article id
sql = "SELECT author, id FROM articles where body like '%%'"
cavdailydb = mysql.connect(
        host="usersrv01.cs.virginia.edu",
        password="F4Vswt5L!",
        database="cavdaily",
        username="cavdaily",
        autocommit=True,
    )
mycursor = cavdailydb.cursor()
mycursor.execute(sql)
selected_articles = mycursor.fetchall()

author_dict = {}


def add_author(authors, author_dict, article_id):
    for author in authors:
        try:
            if article_id not in author_dict[author]:
                author_dict[author][0].append(article_id)
                print(author)
                print(author_dict[author][0])

        except:
            author_dict[author] = [[article_id]]
        

for item in selected_articles:  
    article_id = item[1]
    authors = item[0]
    authors = re.split(" and |, | & ", authors) 
    add_author(authors, author_dict, article_id)

for key in author_dict.keys():
    for art in author_dict[key][0]:
        sql_authors = "INSERT INTO authors (author, article_id) VALUES (%s, %s)"
        vals_authors = (key, art)
        mycursor.execute(sql_authors,vals_authors)
        cavdailydb.commit()





    