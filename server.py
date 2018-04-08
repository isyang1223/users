from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import MySQLConnector
import re 
import md5
app = Flask(__name__)
app.secret_key = 'key'
mysql = MySQLConnector(app,'usersdb')

@app.route('/users')
def index():
    show_all_users_query = "SELECT id, name, email, CONCAT(MONTHNAME(created_at), ' ', DAY(created_at),' ', YEAR(created_at)) AS 'Created At' FROM users;"
    all_users = mysql.query_db(show_all_users_query)
    return render_template("users_index.html", all_users = all_users)

@app.route('/users/<id>')
def show_user(id):
    show_this_user_query = 'SELECT * FROM users WHERE id = :id;'
    show_this_user_data = {'id': id}
    this_user = mysql.query_db(show_this_user_query, show_this_user_data)
    
    return render_template("users_show.html", this_user = this_user)

# @app.route('/click_user')
# def click_user():
#     return redirect("/users/<id>")

@app.route('/users/new')
def click_add_new_user():
    return render_template("users_new.html")

@app.route('/users/create', methods=['POST'])
def create_new_user():
    create_new_user_query = "INSERT INTO users (name, email) VALUES (:name, :email);"
    new_user_data = {
        'name': request.form['name'],
        'email': request.form['email']
    }
    mysql.query_db(create_new_user_query, new_user_data)
    return redirect("/users")

@app.route('/goback')
def go_back():
    return redirect("/users")

    
@app.route('/users/<id>/edit')
def click_edit_user(id):
    show_this_user_query = 'SELECT * FROM users WHERE id = :id;'
    show_this_user_data = {'id': id}
    this_user = mysql.query_db(show_this_user_query, show_this_user_data)
    
    return render_template("edit_users.html", this_user = this_user)

@app.route('/users/<id>/update', methods=['POST'])
def update_user(id):
    update_user_query = "UPDATE users SET name = :name, email = :email WHERE id = :id;"
    update_user_data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'id': id
    }
    
    mysql.query_db(update_user_query, update_user_data)
    
    return redirect("/users")

@app.route('/users/<id>/destory')
def delete(id):
    delete_user_query = "DELETE FROM users where id = :id;"
    delete_data = {'id':id}


    mysql.query_db(delete_user_query, delete_data)
    return redirect("/users")



app.run(debug=True)