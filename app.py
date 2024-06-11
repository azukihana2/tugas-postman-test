from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL()
mysql.init_app(app)

@app.route('/provinces', methods=['GET'])
def get_provinces():
    url = f"{app.config['RAJAONGKIR_BASE_URL']}/province"
    headers = {'key': app.config['RAJAONGKIR_API_KEY']}
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

@app.route('/cities', methods=['GET'])
def get_cities():
    province_id = request.args.get('province_id')
    url = f"{app.config['RAJAONGKIR_BASE_URL']}/city"
    headers = {'key': app.config['RAJAONGKIR_API_KEY']}
    params = {'province': province_id} if province_id else {}
    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())

@app.route('/cost', methods=['POST'])
def get_shipping_cost():
    data = request.json
    url = f"{app.config['RAJAONGKIR_BASE_URL']}/cost"
    headers = {'key': app.config['RAJAONGKIR_API_KEY'], 'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=data)
    return jsonify(response.json())

@app.route('/users', methods=['GET'])
def get_users():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data['name'], data['email']))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'User added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
