import sqlite3


def get_all(inquiry: str):
    with sqlite3.connect('netflix.db') as f:
        f.row_factory = sqlite3.Row
        result = []
        for element in f.execute(inquiry).fetchall():
            result.append(dict(element))
        return result


def get_one(inquiry: str):
    with sqlite3.connect('netflix.db') as f:
        f.row_factory = sqlite3.Row
        result = f.execute(inquiry).fetchone()
        if result is None:
            return None
        else:
            return dict(result)


def get_movie_genre(type_movie, release_year, listed_in):
    inquiry = f"""
    SELECT title, description FROM netflix
    WHERE "type" = '{type_movie}' 
    AND release_year = {release_year} 
    AND listed_in LIKE '%{listed_in}%'
    """
    result = []
    for element in get_all(inquiry):
        result.append({
            "title": element["title"],
            "release_year": element["release_year"]
             })
    return result


def search_cast(name1: str = 'Jack Black', name2: str = 'Dustin Hoffman'):
    inquery = f"""
    SELECT * FROM netflix
    WHERE netflix."cast" LIKE '%Jack Black%' AND netflix."cast" LIKE '%Dustin Hoffman%'
    """
    cast = []
    set_cast = set()
    result = get_all(inquery)
    for element in result:
        for actor in element['cast'].split(','):
            cast.append(actor)
    for actor in cast:
        if cast.count(actor) > 2:
            set_cast.add(actor)
    return list(set_cast)

