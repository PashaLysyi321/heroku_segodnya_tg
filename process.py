import flask

app = flask.Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return 'Hello World'

if __name__ == "__main__":
    app.run()