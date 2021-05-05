#################################
##### Name: Dan Qiao
##### Uniqname: jordannn
#################################

from bs4 import BeautifulSoup
import requests
import time
import json
import plotly.graph_objects as go
import plotly.io as pio
'''
class movie(self,id,rating,actors)
dict { actor:[movie1, movie2, movie3] }
movie_cache
pic_cache{} ???

enter movie
def get_obdb_movie_using_cache(movie_name) ___ return movie's rating, id, actor list
def save_cache
def load_cache
#and store
enter name(if in list)
def get_google_picture(actor's name) ___ return pictures
##if ok, we can save the picture.  

def get_imdb_actor(actor's name) __ return filmography + (get_obdb_movie)rartings 
and store the actor(filmography + avg_ratings)
'''

CACHE_FILE_NAME = 'cache_project.json'
movie_cache = {}  # {'The_Truman_Show': The_Truman_Show}  value type: class movie
movie = {}

class Movie:
    def __init__(self, name=None, Id=None, rating=None, actors_list=None):
        self.name = name
        self.Id = Id
        self.rating = rating
        self.actors_list = actors_list
    
    def printout(self):
        a = self.name + "'s raitng is " + self.rating + ", cast: " + self.actors_list
        print(a)

def save_cache(cache):
    ''' 
    Save Cache
    Parameter: cache
    Return: None
    '''
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

def load_cache():
    '''
    Load Cache
    Parameter: None
    Return: cache
    '''
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def get_omdb_info_using_cache(movie_name, cache):
    '''
    get movie info from OMDb website
    Parameters: movie_name (string) , cache (dict)
    Return: cache[movie_name] (class movie)
    '''
    movie_name = switch_name(movie_name)
    if(movie_name in cache.keys()):
        print('using cache')
        return cache[movie_name]

    else:
        url = 'http://www.omdbapi.com/?apikey=4cb0b69&t=' + movie_name 
        resp = requests.get(url)
        cache[movie_name] = resp.json()
        save_cache(cache)
        #return cache[movie_name]['imdbID'],cache[movie_name]['imdbRating'],cache[movie_name]['Actors']
        # cache['The Truman Show'] = json(omdb)
        return cache[movie_name]
'''
movie_info = get_omdb_info_using_cache('The_Truman_Show', movie_cache)
movie1 = Movie('The_Truman_Show',movie_info['imdbID'], movie_info['imdbRating'], movie_info['Actors'])
movie1.printout()
'''

def get_google_picture_using_cache(actor_name,cache):
    '''
    enter a actor, and search google picture.
    Parameter: actor_name(string)
    Return: 
    '''
    actor_list = actor_name.split()
    n = len(actor_list)
    google_name = ''
    for i in range(n):
        if (i != n-1):
            google_name = google_name + actor_list[i] + '+'
        else:
            google_name = google_name + actor_list[i] #jim+carrey
    
    if(google_name in cache.keys()):
        print('using cache')
        return cache[google_name]

    else:
        url = 'https://www.google.com/search?q=' + google_name + '&tbm=isch' 
        #https://www.google.com/search?q=jim+carrey
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup_body  = soup.body
        img_url = ''
        
        for img in soup_body.find_all('img'):
            if not img['alt'] == 'Google':
                img_url = img['src']
                break
        cache[google_name] = img_url 
        save_cache(cache)   
        return cache[google_name] #cache['jim+carrey']='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRyE4sZsklTbWj-4moHZPm075AG3vTivu_unU5DcAF03qZFUZNLGWqmH4qkCoA&s'
#print(get_google_picture_using_cache('jim carrey',movie_cache))

def get_imdb_url_using_cache(actor_name, movie, cache):
    '''
    IMDb-- get the actor's website
    Parameter: actor_name (string) , movie(class movie) , CACHE_DICT (dict)
    Return: actor_url (string)
    '''
    url = 'https://www.imdb.com/title/' + movie.Id + '/'
    if (actor_name in cache.keys()):
        print('using cache')
        return cache[actor_name]
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for k in soup.find('table',class_='cast_list').find_all('a'):
            if actor_name in k.text:
                actor_url = k['href']
        actor_url = 'https://www.imdb.com' + actor_url
            
        #using cache
        cache[actor_name] = actor_url
        save_cache(cache)  # cache['Jim Carrey'] = 'https://www.imdb.com/name/nm0000120/'
        return actor_url  
#print(get_imdb_url_using_cache('Jim Carrey', movie1, movie_cache))

def get_imdb_filmography_using_cache(url,cache):
    '''
    get filmography from IMDb.
    Parameter: url(string) enter the actor website
    Return: filmography(list)
    '''
    if (url in cache.keys()):
        print('using cache')
        return cache[url]
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        cache[url] = []
        for k in soup.find('div',class_='filmo-category-section').find_all('b'):
            cache[url].append(k.text)
        save_cache(cache)

        return cache[url]  #cache['https://www.imdb.com/name/nm0000120/'] = filmography
#print(get_imdb_filmography_using_cache('https://www.imdb.com/name/nm0000120/',movie_cache))
    
def switch_name(name):
    '''
    switch 'The Truman Show' to 'The_Truman_Show'
    Parameter: name(string)
    Return: imdb_name(string)
    '''
    name_list = name.split()
    n = len(name_list)
    imdb_name = ''
    for i in range(n):
        if (i != n-1):
            imdb_name = imdb_name + name_list[i] + '_'
        else:
            imdb_name = imdb_name + name_list[i]
    return imdb_name
#print(switch_name('a b c'))

if __name__ == "__main__":
    movie = {}
    movie_cache = load_cache()

    movie_name = input('Enter a movie name: ')
    movie_info = get_omdb_info_using_cache(movie_name, movie_cache)

    movie[movie_name] = Movie(movie_name,movie_info['imdbID'], movie_info['imdbRating'], movie_info['Actors'])
    print('Actor List Here: ')
    print(movie[movie_name].actors_list)

    actor = input('Enter a actor name you want to search: ')
    url = get_imdb_url_using_cache(actor, movie[movie_name], movie_cache)
    #print(url)#https://www.imdb.com/name/nm0000120/
    print(get_google_picture_using_cache('jim carrey',movie_cache))

    films = get_imdb_filmography_using_cache(url, movie_cache)
    rating = 0
    i = 0
    x_data = []
    y_data = []
    for film in films:
        a = get_omdb_info_using_cache(film, movie_cache)
        if (a['Response'] == 'False'):
            continue
        else:
            movie[film] = Movie(film, a[0], a[1], a[2])
            #print(film_info['imdbRating'])
            #rating = rating + int(film_info['imdbRating'])
            if not (film_info['imdbRating'] == 'N/A'):
                if film not in x_data:
                    i = i+1
                    rating = rating + float(film_info["imdbRating"])
                    y_data.append(float(film_info["imdbRating"]))
                    x_data.append(film)
                    
    bar_data = go.Bar(x=x_data, y=y_data)
    fig = go.Figure(data=bar_data)
    fig.write_image("1.png")
    a = "{:.3f}".format(rating/i)
    print('average raing: ', a)