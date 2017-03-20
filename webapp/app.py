import os, sys
if 'DYNO' in os.environ:
    HEROKU = True
else:
    HEROKU = False


from flask import Flask
app = Flask(__name__)

# Start with the views
@app.route('/')
def hello():
    return 'Hello World with Flask!'

# ... add the main method for Heroku at the end
if HEROKU:
    if __name__ == '__main__':
        # Bind to PORT if defined, otherwise default to 5000.
        port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
