from flask import Flask
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/getmap/', methods=['GET', 'POST'])
def getmap():
    return jsonify({'id':'1234','name':'Gabba Gabba Hey', 'venue':'Madison Square Garden', 'performer':"Ramones", "when":"16MAY1993"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)