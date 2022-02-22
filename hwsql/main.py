import sqlite3
import json
from flask import Flask, request, render_template, helpers, debughelpers
from utils import get_result
app = Flask(__name__)



@app.get("/movie/<title>")
def get_by_title(title: str):
    sql = f'''SELECT *
    from netflix n
    where n.title = {title} and n.date_added = (SELECT max(date_added)
    from netflix n
    where n.title = {title})'''
    result = []
    for own in get_result(sql):
        res = {
            "title": own.get("title"),
            "country": own.get("country"),
            "release_year": own.get("release_year"),
            "genre": own.get("listed_in"),
            "description": own.get("description"),
        }
        result.append(res)
    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")


@app.get("/movie/<year1>/to/<year2>")
def get_by_date(year1: str, year2: str):
    sql = f'''
    SELECT *
    from netflix n
    where release_year >= {year1} and release_year <= {year2}
    LIMIT 100
    '''
    result = []
    for own in get_result(sql):
        res = {
            "title": own.get("title"),
            "release_year": own.get("release_year")
        }
        result.append(res)
    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")


@app.get("/rating/<value>")
def get_by_rating(value: str):
    sql = f'''
    SELECT *
    from netflix n
    '''

    if value == 'children':
        sql += f'''WHERE rating ='G' '''
    elif value == 'family':
        sql += f'''WHERE rating  LIKE ='%G' '''
    elif value == 'adult':
        sql += f'''WHERE rating ='R' or rating = 'NC-17'  '''
    else:
        app.response_class(response=json.dumps({}),
                           status=204,
                           mimetype="application/json")

    result = []
    for own in get_result(sql):
        res = {
            "title": own.get("title"),
            "release_year": own.get("release_year"),
            "description": own.get("description")
        }
        result.append(res)
    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")



@app.get("/genre/<genre>")
def get_by_genre(genre: str):
    sql = f'''
    SELECT *
    from netflix n
    where listed_in ={genre}
    LIMIT 10
    '''
    result = []
    for own in get_result(sql):
        res = {
            "title": own.get("title"),
            "description": own.get("description")
        }
        result.append(res)
    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")


if __name__ == '__main__':
    app.run(host="localhost", port=8080).

# sql = f'''
# SELECT *
# from netflix n
# where n.show_id = "s2"
# '''
# print(get_result(sql))


# sql = f'''
# SELECT *
# from netflix n
# where n.show_id
# '''

# format = {
#   "title": "title",
#   "country": "country",
#   "release_year": 2021,
#   "genre": "listed_in",
#   "description": "description"
# }
