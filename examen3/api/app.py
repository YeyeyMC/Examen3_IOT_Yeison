from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/datos')
def obtener_datos():
    cliente = MongoClient("mongodb://mongo:27017/")
    db = cliente["siata"]
    col = db["calidad_aire"]

    # Trae todos los documentos y elimina el campo "_id"
    documentos = list(col.find({}, {"_id": 0}))

    return jsonify(documentos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
