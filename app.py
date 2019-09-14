import os
from flask import render_template, request, json, redirect, url_for, session,Flask
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.secret_key = "sandipdas"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'sandip'
app.config['MYSQL_DATABASE_PASSWORD'] = 'toce1234'
app.config['MYSQL_DATABASE_DB'] = 'bucketlist'

mysql = MySQL(app)  

@app.route("/")
def main():
    return render_template('home.html')

@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    # read the posted values from the UI
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    print("hello",name)
    
    # validate the received values

    cur = mysql.get_db().cursor()
    cur.execute("INSERT INTO student(name, email,password) VALUES (%s, %s,%s)", (name, email, password))
    mysql.get_db().commit()
    return render_template('login.html')

@app.route("/showlogin")
def showlogin():
    return render_template('login.html')

@app.route('/login',methods=['POST','GET'])
def login():

    if request.method == 'POST':
        print("inside post")
        print(request.form)
        username=request.form['inputemail']
        password=request.form['inputpassword']
        session['email']=username 
        cur = mysql.get_db().cursor()
        sql = "select * from student where email='%s' and password='%s'" % (username,password)
        if(cur.execute(sql)):
            if 'email' in session:
                results = cur.fetchall()
                return json.dumps({"name":results[0][1], "student_id":results[0][0],"email":results[0][2]})
        else:
            return json.dumps({'html':'<span>Invalid ID and Password</span>'})

        return redirect(url_for('login')) 




@app.route("/sdetails")
def sdetails():
    return redirect(url_for('sdetails.html'))


@app.route("/student_details",methods=['POST','GET'])
def student_details():

    if request.method=='POST' :
            print("== student ==")
            print(request.form)
            target =os.path.join(APP_ROOT,'static')
            if not os.path.isdir(target):
                os.mkdir(target)
            file = request.files['image']
            print("uplod files",file.filename)            
            file.save(os.path.join(target,file.filename))
            address=request.form['address']
            phone_no=request.form['phone_no']
            dob=request.form['dob']
            student_id=request.form['student_id']
            student_name=request.form['student_name']
            student_email=request.form['student_email']
            print("till here",student_email)
            cur = mysql.get_db().cursor()
            cur.execute("INSERT INTO student_details(student_id, address,phone_no,dob,profile_url) VALUES (%s, %s,%s,%s,%s)", (student_id,address,phone_no,dob,file.filename))
            mysql.get_db().commit()  
            return json.dumps({"student_id":student_id})          
            #return render_template('show_details.html',s_id=student_id,s_dob=dob,s_phone=phone_no,s_address=address,s_name=student_name,s_email=student_email,profile_image="/static/"+file.filename)

@app.route("/show_details",methods=['GET'])
def show_details():
    if request.method == 'GET':
        print("get is called")
        student_id = request.args['student_id']
        print("student id ==",student_id)
        cur = mysql.get_db().cursor()
        sql1 = "select * from student where id='%s' " % (student_id)
        cur.execute(sql1)
        results = cur.fetchall()
        print("results-----------",results)
        if len(results) > 0:
            return render_template('sdetails.html',name=results[0][1], student_id=results[0][0],email=results[0][2])
        else:
            return render_template('sdetails.html')

@app.route("/show_all_details",methods=['GET'])
def show_all_details():
    if request.method =='GET' :
        student_id=request.args['student_id']
        print("iiiiiiiiiiiiiiiiidddddddddddddddddddd: ",student_id)
        cur = mysql.get_db().cursor()
        sql="select student.name,student.id,student.email,student_details.address,student_details.phone_no,student_details.dob,student_details.profile_url from student join student_details on student.id=student_details.student_id where student.id='%s' "%(student_id)
        cur.execute(sql)
        results = cur.fetchall()
        print(results)
        return render_template('show_details.html',name=results[0][0], student_id=results[0][1],email=results[0][2],address=results[0][3],phn=results[0][4],dob=results[0][5],img="/static/"+results[0][6])

@app.route('/logout')  
def logout():  
    if 'email' in session:  
        session.pop('email',None)  
        return render_template('login.html');  
    else:  
        return '<p>user already logged out</p>' 

if __name__ == "__main__":
    app.run(debug=True)