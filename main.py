from flask import Flask, jsonify
from utils import get_one, get_all

app = Flask(__name__)


@app.get('/movie/<title>')
def get_title(title: str):
    inquiry = f"""
    SELECT * FROM netflix
    WHERE title = '{title}'
    ORDER BY date_added desc
    """
    inquiry_result = get_one(inquiry)

    conclusion = {
        "title": inquiry_result["title"],
        "country": inquiry_result["country"],
        "release_year": inquiry_result["release_year"],
        "genre": inquiry_result["listed_in"],
        "description": inquiry_result["description"]
    }
    return jsonify(conclusion)


@app.get('/movie/<year1>/to/<year2>')
def get_movie_year(year1: str, year2: str):
    inquiry = f"""
    SELECT * FROM netflix
    WHERE release_year BETWEEN {year1} and {year2}
    LIMIT 100
    """
    result = []
    for element in get_all(inquiry):
        result.append({
            "title": element["title"],
            "release_year": element["release_year"]
        })
    return jsonify(result)


@app.get('/movie/rating/<bound>')
def get_movie_rating(bound: str):
    inquiry = """
    SELECT * FROM netflix
    """
    if bound == 'children':
        inquiry += 'WHERE rating = "G"'
    elif bound == 'family':
        inquiry += 'WHERE rating = "G" or rating = "PG" or rating = "PG-13"'
    elif bound == 'adult':
        inquiry += 'WHERE rating = "R" or rating = "NC-17"'
    else:
        return jsonify(status=400)

    result = []

    for element in get_all(inquiry):
        result.append({
            "title": element["title"],
            "rating": element["rating"],
            "description": element["description"]
        })
    return jsonify(result)


@app.get('/genre/<genre>')
def get_movie_genre(genre: str):
    inquiry = f"""
    SELECT * FROM netflix
    WHERE listed_in LIKE '%{genre}%'
    ORDER BY date_added desc
    LIMIT 10
    """

    result = []

    for element in get_all(inquiry):
        result.append({
            "title": element["title"],
            "description": element["description"]
        })
    return jsonify(result)


app.run()
