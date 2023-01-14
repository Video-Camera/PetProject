from flask import Flask, request, redirect, url_for, render_template
import sqlite3
from DBcontroller import connect_to_db
app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/create-new-pet/", methods=['GET', 'POST'])
def create_pet_profile():
    if request.method == 'POST':
        pet_name = request.form.get('petname')
        pet_species = request.form.get('petspecies')
        conn = connect_to_db()
        curr = conn.cursor()
        sql = """INSERT INTO pet (petname, species) VALUES (?, ?)"""
        curr.execute(sql, (pet_name, pet_species))
        conn.commit()
        conn.close()
        return render_template('homepage.html')
    else:
        return render_template('create-pet-page.html')


@app.route('/showallpets/', methods=['GET'])
def show_all_pets():
    if request.method == 'GET':
        conn = connect_to_db()
        curr = conn.cursor()
        sql = """SELECT * FROM pet"""
        curr.execute(sql)
        list_of_pets = curr.fetchall()
        return render_template('show-all-pets.html', content=list_of_pets)


@app.route('/show-only-unadopted', methods=['GET'])
def show_unadopted_pets():

    if request.method == 'GET':
        conn = connect_to_db()
        curr = conn.cursor()
        sql = """SELECT * FROM pet WHERE ownerId = 0 """
        curr.execute(sql)
        list_of_pets = curr.fetchall()
        sql = """SELECT * FROM user WHERE petId = 0"""
        curr.execute(sql)
        list_of_users = curr.fetchall()
        return render_template('show-unadopted-pets.html', content=list_of_pets, list_of_users=list_of_users)


@app.route("/create-new-user/", methods=['POST', 'GET'])
def create_user_profile():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        conn = connect_to_db()
        curr = conn.cursor()
        sql = """INSERT INTO user (firstname, lastname) VALUES (?, ?)"""
        curr.execute(sql, (firstname, lastname))
        conn.commit()
        conn.close()
        return render_template('homepage.html')
    else:
        return render_template('create-user.html')


@app.route('/adoption', methods=['POST'])
def adoption_operation():
        select_user = request.form.get('user')
        print(select_user)


@app.route('/pet/<int:petId>', methods=['GET'])
def pet_profile_page(petId):
    conn = connect_to_db()
    curr = conn.cursor()
    sql = """SELECT * FROM pet WHERE petId = ?"""
    curr.execute(sql, (petId, ))
    pet_entity = curr.fetchall()
    return render_template('pet-profile.html', content=pet_entity)


@app.route('/pet/edit/<int:petId>', methods=['GET'])
def edit_pet_get(petId):
    conn = connect_to_db()
    curr = conn.cursor()
    sql = """SELECT * FROM pet WHERE petId = ?"""
    curr.execute(sql, (petId, ))
    selected_pet = curr.fetchall()
    sql_get_users = """SELECT * FROM user"""
    curr.execute(sql_get_users)
    list_of_users = curr.fetchall()
    return render_template('pet-edit.html', content=selected_pet[0], list_of_users=list_of_users)


@app.route('/pet/edit/<int:petId>', methods=['POST'])
def edit_pet_post(petId):
    conn = connect_to_db()
    curr = conn.cursor()
    edited_name = request.form.get('editName')
    edited_species = request.form.get('editSpecies')
    edited_owner = request.form.get('editOwner')
    sql = """UPDATE pet SET petname = ?, species = ?, ownerId = ? WHERE petId = ?"""
    curr.execute(sql, (edited_name, edited_species, edited_owner, petId))
    sql_user = """UPDATE user SET petId = ? WHERE userId = ? """
    curr.execute(sql_user, (petId, edited_owner))
    # selected_pet = curr.fetchall()
    conn.commit()
    return redirect(f"/pet/{petId}")


@app.route('/user/<int:userId>', methods=['GET'])
def user_page(userId):
    conn = connect_to_db()
    curr = conn.cursor()
    sql = """SELECT * FROM user WHERE userId = ?"""
    sql_2 = """SELECT * FROM pet WHERE ownerId = ?"""
    curr.execute(sql, (userId, ))
    user_content = curr.fetchone()
    curr.execute(sql_2, (userId, ))
    pet_content = curr.fetchone()
    return render_template('user-page.html', content=user_content, pet=pet_content)


@app.route('/user/showusers/', methods=['GET'])
def show_all_users():
    conn = connect_to_db()
    curr = conn.cursor()
    sql = """SELECT userId, firstname FROM user"""
    curr.execute(sql)
    list_of_all_users = curr.fetchall()
    return render_template('show-all-users.html', content=list_of_all_users)



if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
    # app.run()  # run app
