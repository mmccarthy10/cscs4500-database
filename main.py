# Import files
from flask import Flask,request,render_template
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
<<<<<<< Updated upstream
=======
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
#
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

>>>>>>> Stashed changes
#Andres page
@app.route("/Accounts", methods=['GET', 'POST'])
def accounts_main():
    if request.method == "POST":
        details = request.form

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        if "name" in details:
            cursor.execute('INSERT INTO accounts (Name, Password,Email, Address, ID, Type) VALUES("' + details['name'] + '", "' + details['password'] + '","' + details['email'] + '", "' + details['address'] + '", "' + details['ID'] + '", "' + details['Type'] +'");')

        mysql.connection.commit()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts;')
    data = cursor.fetchall()

    return render_template('andres.html', data=data)
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

# Run server, visible online and refreshes with new code
if __name__ == "__main__":
    app.run(debug = True)
