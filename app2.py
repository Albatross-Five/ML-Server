import os
import hashlib
from flask import Flask, request, jsonify, render_template, session, redirect
from flask_cors import CORS
from flask_mysqldb import MySQL
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
CORS(app)
mysql = MySQL(app)

# MySQL 연결 정보 입력
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# 메인 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 로그인 페이지
@app.route('/login')
def login():
    return render_template('login.html')

# 로그인 API
@app.route('/login', methods=['POST'])
def login_api():
    # JSON 데이터 추출
    data = request.get_json()
    id = data['id']
    password = data['password']

    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

    # MySQL 데이터베이스에서 해당 회원 정보 추출
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM members WHERE id = %s AND password = %s"
    val = (id, hashed_password)
    cursor.execute(sql, val)
    member = cursor.fetchone()
    cursor.close()

    # 해당 회원 정보가 없는 경우
    if member is None:
        return jsonify({'message': 'Login failed'}), 400

    # 해당 회원 정보가 있는 경우
    else:
        session['user_id'] = id
        return redirect('/exercise')

# 회원가입 페이지
@app.route('/signup')
def siguup():
    return render_template('signup.html')

# 회원가입 API
@app.route('/signup', methods=['POST'])
def signup_api():
    # JSON 데이터 추출
    data = request.get_json()
    id = data['id']
    password = data['password']
    name = data['name']
    gender = data['gender']
    birthdate = data['birthdate']
    height = data['height']
    weight = data['weight']
    email = data['email']
    
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

    # MySQL 데이터베이스에 새로운 회원 정보 추가
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO members (id, password, name, gender, birthdate, height, weight, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (id, hashed_password, name, gender, birthdate, height, weight, email)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()

    # HTTP 응답으로 성공 메시지 반환
    return jsonify({'message': 'Signup successful'}), 200

# 운동정보 페이지
@app.route('/exercise')
def exercise():
    user_id = session.get('user_id')
    
    # 로그인하지 않은 경우 로그인 페이지로 리다이렉트
    if user_id is None:
        return redirect('/login')
    
    # 해당 사용자의 운동정보 조회
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM exercise_log JOIN exercise ON exercise_log.exercise_code = exercise.exercise_code WHERE id = %s"
    val = (user_id,)
    cursor.execute(sql, val)
    exercise = cursor.fetchall()
    cursor.close()
    
    return render_template('exercise.html', exercise = exercise)

# 운동정보 API
@app.route('/exercise', methods=['POST'])
def exercise_api():
    # JSON 데이터 추출
    data = request.get_json()
    id = data['id']
    date = data['date']
    start_time = data['start_time']
    exercise_time = data['exercise_time']
    end_time = start_time + exercise_time
    exercise_code = data['exercise_code']
    mass = data['mass']
    count = data['count']

    # MySQL 데이터베이스에 새로운 운동 정보 추가
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO exercise_log (id, date, start_time, end_time, exercise_code, mass, count) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (id, date, start_time, end_time, exercise_code, mass, count)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()

    # HTTP 응답으로 성공 메시지 반환
    return jsonify({'message': 'Signup successful'}), 200

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)