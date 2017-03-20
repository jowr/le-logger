import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World with Flask!'

if 'DYNO' in os.environ:
    HEROKU = True
else:
    HEROKU = False
 
if HEROKU:
    if __name__ == '__main__':
        # Bind to PORT if defined, otherwise default to 5000.
        port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

## Default pythonanywhere flask app
## A very simple Flask Hello World app for you to get started with...
#from flask import Flask
#app = Flask(__name__)
#@app.route('/')
#def hello_world():
#    return 'Hello from Flask!'
#