from flask import Flask, render_template
from werkzeug import SharedDataMiddleware
from helpers import getPlaylist
import os



app = Flask(__name__)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })



@app.route('/')
def main_page():

  options = []
  for item in getPlaylist():
    dict = {}
    dict['url'] = '/go/' + item
    dict['text'] = item

    options.append(dict)

  return render_template('home.html', stations = options)


@app.route('/go/<station>')
def go_to_station(station):
  fh = open('status', 'w')
  fh.write(station)
  fh.close()

  return main_page()

  
@app.route('/playlist')
def see_playlist():
  fh = open('playlist.json', 'rb')
  output = fh.read()
  fh.close()
  return output
    
if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')
        