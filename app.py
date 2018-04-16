from flask import Flask

# default code
app = Flask(__name__)


@app.route('/')
def hello_world():
    """ This is the MAIN PAGE of this Server Application"""
    return 'Hello World!'


""" Include new pages below this """

if __name__ == '__main__':
    app.run()
