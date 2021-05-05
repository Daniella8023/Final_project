#FlaskInputApp.py
from flask import Flask, render_template, request
import Final_project
import requests
import time
import json
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)
movie_name = ''
Final_project.movie_cache = Final_project.load_cache()

@app.route('/')
def index():
    return render_template('FlaskInput_movie.html') # just the static HTML
    

@app.route('/actor_form', methods=['POST'])
def actor_form():
    global movie_name 
    movie_name = request.form["movie"]
    movie_info = Final_project.get_omdb_info_using_cache(movie_name, Final_project.movie_cache)
    #print(type(movie_info))
    #Final_project.movie[movie_name] = Final_project.Movie(movie_name,a[0], a[1], a[2])
    Final_project.movie[movie_name] = Final_project.Movie(movie_name,movie_info['imdbID'], movie_info['imdbRating'], movie_info['Actors'])
    return render_template('FlaskInput_actor.html', 
        movie_name=movie_name, 
        actor_list=movie_info['Actors'])

@app.route('/filmography_form', methods=['POST'])
def filmography_form():
    actor = request.form["actor"]
    #movie_name = request.form["movie"]
    url = Final_project.get_imdb_url_using_cache(actor, Final_project.movie[movie_name], Final_project.movie_cache)
    films =Final_project.get_imdb_filmography_using_cache(url, Final_project.movie_cache)
    rating = 0
    i = 0
    x_data = []
    y_data = []
    for film in films:
        film_info = Final_project.get_omdb_info_using_cache(film, Final_project.movie_cache)
        if (film_info['Response']=='False'):
            continue
        else:
            if not (film_info['imdbRating'] == 'N/A'):
                if film not in x_data:
                    i = i+1
                    rating = rating + float(film_info["imdbRating"])
                    y_data.append(float(film_info["imdbRating"]))
                    x_data.append(film)

    bar_data = go.Bar(x=x_data, y=y_data)
    fig = go.Figure(data=bar_data)
    fig.write_image("/Users/danqiao/Final_project/static/{}_rating.png".format(actor))
    a = "{:.3f}".format(rating/i)
    #print('average raing: ', a)    
    img_url = Final_project.get_google_picture_using_cache(actor, Final_project.movie_cache)
    req = requests.get(img_url)
    with open("/Users/danqiao/Final_project/static/{}_pic.jpg".format(actor),"wb")as f:
        f.write(req.content)
    #print(img_url)

    return render_template('FlaskOutput.html', 
        a=a, 
        actor_name=actor,
        img_url=img_url)
    
if __name__ == "__main__":
    app.run(debug=True) 