from flask import Flask
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_cors import CORS
import os
import ibm_db


app = Flask(__name__)
CORS(app)

try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30367;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=gdj87934;PWD=2OYOHzMQ8MrMcFpa",'','')
    print("Connected")
except:
    print("Error")
picFolder = os.path.join('static','images')
app.config['UPLOAD_FOLDER'] = picFolder
@app.route("/signup/user")
def index(name = None, error = False):
    if request.args:
        error = request.args['error']
        # error = session['']
    img = os.path.join(app.config['UPLOAD_FOLDER'], 'undraw_mobile_ux_re_59hr.png')
    sql = "SELECT * FROM LOGIN"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    return render_template('index.html', name=name, image = img, error = False)

@app.route('/signup')

def signup():
    return render_template('signup.html')

@app.route('/login')
def login(name = None):
    return render_template('Login.html', name = name)

@app.route('/register', methods = ["POST", "GET"])
def register():
    name = 'blank'
    if request.method == "POST":

        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        select_sql = "SELECT * from signup WHERE email = ?"
        std = ibm_db.prepare(conn, select_sql)
        ibm_db.bind_param(std, 1, email)
        ibm_db.execute(std)
        account = ibm_db.fetch_assoc(std)
        if account:
            return render_template('index.html', error = True)
        insert_sql = "INSERT INTO signup VALUES (?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, name)
        ibm_db.bind_param(prep_stmt, 2, email)
        ibm_db.bind_param(prep_stmt, 3, password)
        ibm_db.execute(prep_stmt)
        return render_template('result.html', names = name)
    return render_template('result.html', names = name )

@app.route('/loginapi', methods = ["POST", "GET"])
def sign():
    if request.method == 'POST':
        email = request.form.get('email')
        passw = request.form.get('password')
        sql = "SELECT * from signup where email = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if not account:
            return render_template('login.html', error = 'Accound not Found')
        if account['PASS'] == passw:
            return render_template('result.html', names = account['USERNAME'])
        else:
            return render_template('login.html', error = 'Password is Wrong')
    return render_template('index.html')

@app.route('/adminLogin', methods = ["POST", "GET"])
def adminLogin():
    if request.method == "POST":
        email = request.form.get('email')
        p = request.form.get('password')
        sql = "SELECT * from adlogin where email = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if not account:
            return render_template('Admin.html', error = True)
        if account['PASS'] == p:
            return render_template('AdminDashboard.html', names = account['USERNAME'])
        else:
            render_template('Admin.html', error = True)

@app.route('/loginadmin')
def log():
    return render_template('Admin.html')

@app.route('/hospitalsign', methods=["POST", "GET"])
def hosRegis():
    if request.method == "POST":
        email = request.form.get('email')
        p = request.form.get('password')
        name = request.form.get("name")
        select_sql = "SELECT * from HOSPITALRECORD WHERE email = ?"
        std = ibm_db.prepare(conn, select_sql)
        ibm_db.bind_param(std, 1, email)
        ibm_db.execute(std)
        account = ibm_db.fetch_assoc(std)
        if account:
            return render_template('hospitasignup.html', error = True)
        insert_sql = "INSERT INTO hospitalrecord VALUES (?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, name)
        ibm_db.bind_param(prep_stmt, 2, email)
        ibm_db.bind_param(prep_stmt, 3, p)
        ibm_db.execute(prep_stmt)
        return render_template('hospitalDashboard.html', hospitalName = name)
@app.route('/hospital/dashboard', methods = ["POST", "GET"])
def hoplog():
    if request.method == "POST":
        email = request.form.get('email')
        passw = request.form.get('password')
        sql = "SELECT * from HOSPITALRECORD where email = ?"
        
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if not account:
            return render_template('hospitaloign.html', error = 'Accound not found')
        if account['PASS'] == passw:
            return render_template('hospitalDashboard.html', hospitalName = account['NAME'])
        else:
            return render_template('hospitaloign.html', error = 'Password is Wrong')

@app.route('/hospitalSignup')

def hospsign():
    return render_template('hospitasignup.html')

@app.route('/hospitallogin')
def hospLogin():
    return render_template('hospitaloign.html')

@app.route('/log')

def applog():
    return render_template('log.html')

@app.route('/home', methods = ['POST'])
def disp():
    if request.method == 'POST':
        _json = request.json
        print(_json)
        return jsonify({'data': 3})