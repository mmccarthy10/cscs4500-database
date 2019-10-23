from flask import Flask,request,render_template
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_USER'] = 'csc4500'
app.config['MYSQL_PASSWORD'] = 'charitydb'
app.config['MYSQL_DB'] = 'Charity'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

@app.route("/")
def hello():
    return render_template('login.html')

@app.route("/Donation", methods=['GET', 'POST'])
def Authenticate():
    if request.method == "POST":
        details = request.form

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if "delete" in details:
            cursor.execute('DELETE FROM donation WHERE donationId="' + details['delete'] + '";')
            mysql.connection.commit()
        if "name" in details:
            cursor.execute('INSERT INTO donation (donationName, quantity, donator, date) VALUES("' + details['name'] + '", "' + details['qty'] + '", "' + details['donator'] + '", "2019-10-22");')
            mysql.connection.commit()
    donationName = 'T-Shirt'
    #cursor = mysql.connect().cursor()
    #cursor.execute("SELECT * from donation where donationName='" + donationName + "'")
    #data = cursor.fetchone()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM donation;')
    data = cursor.fetchall()
    print("Routed here")
    #entry1 = cursor.fetchone()

    #cursor.execute('SELECT * FROM donation WHERE donationId=2')
    #entry2 = cursor.fetchone()
    #cursor.execute('SELECT * FROM donation WHERE donationId=3')
    #entry3 = cursor.fetchone()
    #if entry3 is None:
    #    entry2['donationName'] = 'NULLED!'
    
    table = [
        {
           'name': 'T-Shirt',
           'quantity': '4',
           'donator': 'Sarah Hawkins',
           'date': '2019-10-14',
           'id': '1'
        }
    ]
        #if data is None:
     #return "Definitely not a thing."
    #else:
     #return "That's a thing!"
    return render_template('donations.html', data=data)

if __name__ == "__main__":
    app.run(host = "0.0.0.0",debug = True)
