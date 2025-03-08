from flask import Flask, jsonify
from flask_cors import CORS  # cors stuff

app = Flask(__name__)
CORS(app)  

#First route!
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello World!")

if __name__ == '__main__':
    app.run(debug=True)