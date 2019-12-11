# Import files
from flask import Flask,request,render_template,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import datetime

# Create MySQL object
mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'your secret key'

app.config['MYSQL_USER'] = 'csc4500'
app.config['MYSQL_PASSWORD'] = 'charitydb'
app.config['MYSQL_DB'] = 'Charity'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

# Login page
@app.route("/", methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Email' in request.form and 'Password' in request.form:
        # Create variables for easy access
        Email = request.form['Email']
        Password = request.form['Password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE Email = %s AND Password = %s', (Email, Password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['ID'] = account['ID']
            session['Email'] = account['Email']
            # Redirect to home page
            return redirect(url_for('dashboard'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('ID', None)
   session.pop('Email', None)
   # Redirect to login page
   return redirect(url_for('login'))

#Recipients page
@app.route("/recipients", methods=['GET', 'POST'])
# edit function
# def edit(locationId):
#     qry = db_session.query(Album).filter(
#                 Album.id==id)
#     album = qry.first()
#
#     if album:
#         form = AlbumForm(formdata=request.form, obj=album)
#         if request.method == 'POST' and form.validate():
#             # save edits
#             save_changes(album, form)
#             flash('recipient updated!')
#             return redirect('/')
#         return render_template('andres.html', form=form)
#     else:
#         return 'Error loading #{locationId}'.format(locationId=locationId)
def recipients_main():
    if request.method == "POST":
        details = request.form

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if "delete" in details:
            cursor.execute('DELETE FROM recipients WHERE locationId="' + details['delete'] + '";')
        if "company" in details:
            cursor.execute('INSERT INTO recipients (locationId, company, address, description) VALUES("' + details['locationId'] + '", "' + details['company'] + '", "' + details['Address'] + '","' + details['description'] +'");')

        mysql.connection.commit()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM recipients;')
    data = cursor.fetchall()


    return render_template('Recipients.html',data=data)

#Andres page
@app.route("/accounts", methods=['GET', 'POST'])
def accounts_main():
    if request.method == "POST":
        details = request.form

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if "delete" in details:
            cursor.execute('DELETE FROM accounts WHERE ID ="' + details['delete'] + '";')
        if "Name" in details:
            cursor.execute('INSERT INTO accounts (Name, Password,Email, Address, ID, Type) VALUES("' + details['Name'] + '", "' + details['Password'] + '","' + details['Email'] + '", "' + details['Address'] + '", "' + details['ID'] + '", "' + details['Type'] +'");')

        mysql.connection.commit()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts;')
    data = cursor.fetchall()

    return render_template('accounts.html', data=data)
#Carlos page
@app.route("/carlos")
def carlos():
    example = "Hello"
    return render_template('carlos.html', example=example)

#Ben page
@app.route("/Ben")
def Ben():
    variable = "Hello World!"
    return render_template('ben.html', variable=variable)

#Outgoing Donation page by carlos
@app.route("/outgoing-donation", methods=['GET', 'POST'])
def outgoing_donation():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM donation;')
    data = cursor.fetchall()
    cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor2.execute('SELECT * FROM Recipients;')
    people = cursor2.fetchall()
    return render_template('outgoing.html', data=data, people=people)

@app.route("/outgoing-donation-matt", methods=['GET', 'POST'])
def outgoing_donation_matt():
    if request.method == "POST":
        details = request.form

        today = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
        print(today)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if "delete" in details:
            cursor.execute('DELETE FROM donation WHERE donationId="' + details['delete'] + '";')
        if "recipient" in details:
            cursor.execute('INSERT INTO outgoingOverview (outgoingDate, outgoingRecipient, outgoingSent) VALUES("' + today + '", "' + details['recipient'] + '", 0);')
        if "donation" in details:
            cursor.execute('INSERT INTO outgoingDonations VALUES("' + details['donation'] + '", "' + details['item'] + '", "' + details['qty'] + '");')

        mysql.connection.commit()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM outgoingOverview;')
    data = cursor.fetchall()

    return render_template('outgoing-matt.html', data=data)

# Main donation landing page, reads and writes data to donation table
@app.route("/Donation", methods=['GET', 'POST'])
def donation_main():
    if request.method == "POST":
        details = request.form

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if "delete" in details:
            cursor.execute('DELETE FROM donation WHERE donationId="' + details['delete'] + '";')
        if "name" in details:
            cursor.execute('INSERT INTO donation (donationName, quantity, donator, date) VALUES("' + details['name'] + '", "' + details['qty'] + '", "' + details['donator'] + '", "2019-12-11");')

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
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('dashboard.html', email=session['Email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# Run server, visible online and refreshes with new code
if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0")
