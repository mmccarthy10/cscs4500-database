# Import files
from flask import Flask,request,render_template,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

# Create MySQL object
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_USER'] = 'csc4500'
app.config['MYSQL_PASSWORD'] = 'charitydb'
app.config['MYSQL_DB'] = 'Charity'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

# Login page
@app.route("/")
def login():
    return render_template('login.html')

#Outgoing Donation page by carlos
@app.route("/outgoing-donation")
def outgoing_donation():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM donation;')
    data = cursor.fetchall()
    cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor2.execute('SELECT * FROM Recipients;')
    people = cursor2.fetchall()
    return render_template('outgoing.html', data=data, people=people)
#Incoming donation page by Carlos
@app.route("/incoming-donation")
def incoming_donation():
    example = "in"
    return render_template('incoming.html', example=example)
# Main donation landing page, reads and writes data to donation table
@app.route("/Donation", methods=['GET', 'POST'])
def donation_main():
    if request.method == "POST":
        details = request.form

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if "delete" in details:
            cursor.execute('DELETE FROM donation WHERE donationId="' + details['delete'] + '";')
        if "name" in details:
            cursor.execute('INSERT INTO donation (donationName, quantity, donator, date) VALUES("' + details['name'] + '", "' + details['qty'] + '", "' + details['donator'] + '", "2019-10-22");')

        mysql.connection.commit()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM donation;')
    data = cursor.fetchall()

    return render_template('donations.html', data=data)

# Page for editing incoming donation entries
@app.route("/EditInDonation", methods=['GET', 'POST'])
def edit_indonation():
    if request.method == "POST":
        details = request.form

        # Populate edit with details
        if "edit" in details:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            print ("Editing " + details ['edit'])
            cursor.execute('SELECT * FROM donation WHERE donationId=' + details['edit'] + ';')
            data = cursor.fetchall()
            return render_template('edit_indonation.html', data=data)

        # Submit edit to database
        if "name" in details:
            print ("Confirming " + details['id'])
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE donation SET donationName="' + details['name'] + '", quantity=' + details['qty'] + ', donator="' + details['donator'] + '", date="' + details['date'] + '" WHERE donationId=' + details['id'] + ';')
            mysql.connection.commit()
            return redirect(url_for("donation_main"))

        # Redirect to main page if no entry picked
        else:
            return redirect(url_for("donation_main"))

    return redirect(url_for("donation_main"))
#Enter Recipients info for outgoing Donations -- Carlos
@app.route("/Recipients", methods=['GET', 'POST'])
def recipients_info():
    if request.method == "POST":
        info = request.form

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if "delete" in info:
            cursor.execute('DELETE FROM Recipients WHERE RE_NUM="' + info['delete'] + '";')
            mysql.connection.commit()
        if "name" in info:
            cursor.execute('INSERT INTO Recipients (RE_NAME, RE_ADDRESS, RE_CITY, RE_STATE, RE_COUNTRY, RE_ZIP, RE_EMAIL, RE_PHONE) VALUES("' + info['name'] + '", "' + info['address'] + '", "' + info['city'] + '", "' + info['state'] + '", " USA", "' + info['zip'] +'", "' + info['email_address'] +'", "' + info['phone'] + '");')
            mysql.connection.commit()


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Recipients;')
    data = cursor.fetchall()

    return render_template('recipients.html')
#a landing page for incoming and outgoing donations
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title="Dashboard")
# Run server, visible online and refreshes with new code
if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0")
