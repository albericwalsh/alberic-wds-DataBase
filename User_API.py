import time

import flask
import flask_cors
import mysql.connector as mysql
from flask import request, jsonify

# Flask setup
app = flask.Flask(__name__)
app.config["PORT"] = 5001
app.config["DEBUG"] = True
flask_cors.CORS(app)

# Database connection
try:
    database = mysql.connect(host="localhost", user="root", passwd="T(N23P.1[Gz.dpo%", database="alberic_wds_db_user")
    cursor = database.cursor()
except Exception as e:
    print("Error: Unable to connect to the database")
    print(e)


# Exemple: http://127.0.0.1:5001/api/v1/user/login?username=alberic&password=123
@app.route('/api/v1/user/login', methods=['GET'])
def login():
    if 'username' in request.args:
        username = request.args['username']
    else:
        return jsonify({'Statut': 1, 'Message': 'No username field provided. Please specify a username.'})

    if 'password' in request.args:
        password = request.args['password']
    else:
        return jsonify({'Statut': 1, 'Message': 'No password field provided. Please specify a password.'})

    # check if the user exists and return UID
    cursor.execute("SELECT UID FROM Users WHERE UserName=%s AND Password=%s", (username, password))
    user = cursor.fetchone()
    if user:
        # set the user as connected
        cursor.execute("UPDATE Users SET IsConnected=TRUE WHERE UID=%s", (user[0],))
        return jsonify({'Statut': 0, 'Message': 'User connected successfully', 'UID': user[0]})
    else:
        return jsonify({'Statut': 1, 'Message': 'Username or password is incorrect'})

# Exemple: http://127.0.0.1:5001/api/v1/user/register?username=alberic&password=123&name=Alberic
@app.route('/api/v1/user/register', methods=['GET'])
def register():
    if 'username' in request.args:
        username = request.args['username']
    else:
        return jsonify({'Statut': 1, 'Message': 'Username not provided, please specify a username'})

    if 'password' in request.args:
        password = request.args['password']
    else:
        return jsonify({'Statut': 1, 'Message': 'Password not provided, please specify a password'})

    if 'name' in request.args:
        name = request.args['name']
    else:
        return jsonify({'Statut': 1, 'Message': 'Name not provided, please specify a name'})

    cursor.execute("INSERT INTO Users (UserName, Password, Name) VALUES (%s, %s, %s)", (username, password, name))
    database.commit()
    return jsonify({'Statut': 0, 'Message': 'User registered successfully'})

# Exemple: http://127.0.0.1:5001/api/v1/user/logout?user=1
@app.route('/api/v1/user/logout', methods=['GET'])
def logout():
    if 'user' in request.args:
        user = request.args['user']
    else:
        return jsonify({'Statut': 1, 'Message': 'User not provided'})

    cursor.execute("UPDATE Users SET IsConnected=FALSE WHERE UID=%s", (user,))
    database.commit()
    return jsonify({'Statut': 0, 'Message': 'User disconnected successfully'})

# Exemple: http://127.0.0.1:5001/api/v1/user/update_user?user=1&password=123&name=Alberic
@app.route('/api/v1/user/update_user', methods=['GET'])
def update_user():
    if 'user' in request.args:
        user = request.args['user']
    else:
        return jsonify({'Statut': 1, 'Message': 'User not provided'})

    if 'password' in request.args:
        password = request.args['password']
    else:
        return jsonify({'Statut': 1, 'Message': 'Password not provided'})

    if 'name' in request.args:
        name = request.args['name']
    else:
        return jsonify({'Statut': 1, 'Message': 'Name not provided'})

    cursor.execute("UPDATE Users SET Password=%s, Name=%s WHERE UID=%s", (password, name, user))
    database.commit()
    return jsonify({'Statut': 0, 'Message': 'User updated successfully'})

# Exemple: http://127.0.0.1:5001/api/v1/user/set_user_admin?user=2&approbator=1
@app.route('/api/v1/user/set_user_admin', methods=['GET'])
def set_user_admin():
    if 'user' in request.args:
        user = request.args['user']
    else:
        return jsonify({'Statut': 1, 'Message': 'User not provided'})

    if 'approbator' in request.args:
        approbator = request.args['approbator']
    else:
        return jsonify({'Statut': 1, 'Message': 'Approbator not provided'})

    #     get approbator approbation
    cursor.execute("SELECT Approbator FROM Users WHERE UID=%s", (approbator,))
    approbator = cursor.fetchone()
    if approbator >= 1:
        cursor.execute("UPDATE Users SET Approbator=1 WHERE UID=%s", (user,))
        database.commit()
        return jsonify({'Statut': 0, 'Message': 'User is now an admin'})
    else:
        return jsonify({'Statut': 1, 'Message': 'User is not an approbator'})

# Exemple: http://127.0.0.1:5001/api/v1/user/delete_user?user=2&password=123
@app.route('/api/v1/user/delete_user', methods=['GET'])
def delete_user():
    if 'user' in request.args:
        user = request.args['user']
    else:
        return jsonify({'Statut': 1, 'Message': 'User not provided'})

    if 'password' in request.args:
        password = request.args['password']
    else:
        return jsonify({'Statut': 1, 'Message': 'Password not provided'})

    cursor.execute("DELETE FROM Users WHERE UID=%s AND Password=%s", (user, password))
    database.commit()
    return jsonify({'Statut': 0, 'Message': 'User deleted successfully'})

# Exemple: http://127.0.0.1:5001/api/v1/user/get_users
@app.route('/api/v1/user/get_users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    user_list = []
    for user in users:
        user_list.append({'UID': user[0], 'Username': user[1], 'Name': user[3]})

    return jsonify({'Statut': 0, 'Users': user_list})

# Exemple: http://127.0.0.1:5001/api/v1/services/check_service?service=1&user=1
@app.route('/api/v1/services/check_service', methods=['GET'])
def check_service():
    if 'service' in request.args:
        service = request.args['service']
    else:
        return jsonify({'Statut': 1, 'Message': 'Service not provided'})

    if 'user' in request.args:
        user = request.args['user']
    else:
        return jsonify({'Statut': 1, 'Message': 'User not provided'})

    cursor.execute("SELECT * FROM Services_List WHERE UID=%s AND SID=%s", (user, service))
    service = cursor.fetchone()
    if service:
        return jsonify({'Statut': 0, 'Message': 'Service available for UID=' + str(user)})
    else:
        return jsonify({'Statut': 1, 'Message': 'Service not available'})

# Exemple: http://127.0.0.1:5001/api/v1/services/add_service?service=1&user=1
@app.route('/api/v1/services/add_service', methods=['GET'])
def add_service():
    if 'service' in request.args:
        service = request.args['service']
    else:
        return jsonify({'Statut': 1, 'Message': 'Service not provided'})

    if 'user' in request.args:
        user = request.args['user']
    else:
        return jsonify({'Statut': 1, 'Message': 'User not provided'})

    # check if the user is an approbator
    cursor.execute("SELECT Role FROM Users WHERE UID=%s", (user,))
    user = cursor.fetchone()

    cursor.execute("SELECT Approbation FROM Services WHERE SID=%s", (service,))
    approbation = cursor.fetchone()
    if user >= 1 or approbation == 0:
        cursor.execute("INSERT INTO Services_List (UID, SID, ReceiveDate) VALUES (%s, %s, %s)",
                       (user, service, time.strftime('%Y-%m-%d %H:%M:%S')))
        database.commit()
        return jsonify({'Statut': 0, 'Message': 'Service added successfully for UID=' + str(user)})
    elif approbation == 1:
        cursor.execute("INSERT INTO Services_Approbation_List (UID, SID, ClaimDate) VALUES (%s, %s, %s)",
                       (user, service, time.strftime('%Y-%m-%d %H:%M:%S')))
        database.commit()
        return jsonify({'Statut': 0, 'Message': 'Service added to approbation list for UID=' + str(user)})
    else:
        return jsonify({'Statut': 1, 'Message': 'User is not an approbator'})

# Exemple: http://127.0.0.1:5001/api/v1/services/remove_service?service=1&user=1
@app.route('/api/v1/services/remove_service', methods=['GET'])
def remove_service():
    if 'service' in request.args:
        service = request.args['service']
    else:
        return jsonify({'Statut': 1, 'Message': 'Service not provided'})

    if 'user' in request.args:
        user = request.args['user']
    else:
        return jsonify({'Statut': 1, 'Message': 'User not provided'})

    cursor.execute("DELETE FROM Services_List WHERE UID=%s AND SID=%s", (user, service))
    database.commit()
    return jsonify({'Statut': 0, 'Message': 'Service removed successfully for UID=' + str(user)})

# Exemple: http://127.0.0.1:5001/api/v1/services/create_services?name=Service1&link=www.service1.com&description=Service1Description&approbator=1
@app.route('/api/v1/services/create_services', methods=['GET'])
def create_services():
    if 'name' in request.args:
        name = request.args['name']
    else:
        return jsonify({'Statut': 1, 'Message': 'Name not provided'})

    if 'link' in request.args:
        link = request.args['link']
    else:
        return jsonify({'Statut': 1, 'Message': 'Link not provided'})

    if 'description' in request.args:
        description = request.args['description']
    else:
        return jsonify({'Statut': 1, 'Message': 'Description not provided'})

    if 'user' in request.args:
        approbator = request.args['approbator']
    else:
        return jsonify({'Statut': 1, 'Message': 'Approbator not provided'})

    cursor.execute("SELECT Role FROM Users WHERE UID=%s", (approbator,))
    approbator = cursor.fetchone()
    if approbator >= 1:
        cursor.execute("INSERT INTO Services (Name, Link, Description) VALUES (%s, %s, %s)", (name, link, description))
        database.commit()
        return jsonify({'Statut': 0, 'Message': 'Service created successfully'})
    else:
        return jsonify({'Statut': 1, 'Message': 'User is not an approbator'})

# Exemple: http://127.0.0.1:5001/api/v1/services/delete_service?service=1&approbator=1
@app.route('/api/v1/services/delete_service', methods=['GET'])
def delete_services():
    if 'service' in request.args:
        service = request.args['service']
    else:
        return jsonify({'Statut': 1, 'Message': 'Service not provided'})

    if 'approbator' in request.args:
        approbator = request.args['approbator']
    else:
        return jsonify({'Statut': 1, 'Message': 'Approbator not provided'})

    cursor.execute("SELECT Role FROM Users WHERE UID=%s", (approbator,))
    approbator = cursor.fetchone()
    if approbator >= 1:
        cursor.execute("DELETE FROM Services WHERE SID=%s", (service,))
        database.commit()
        return jsonify({'Statut': 0, 'Message': 'Service deleted successfully'})
    else:
        return jsonify({'Statut': 1, 'Message': 'User is not an approbator'})

# Exemple: http://127.0.0.1:5001/api/v1/services/get_services
@app.route('/api/v1/services/get_services', methods=['GET'])
def get_services():
    cursor.execute("SELECT * FROM Services")
    services = cursor.fetchall()
    services_list = []
    for service in services:
        services_list.append({'SID': service[0], 'Name': service[1], 'Link': service[2], 'Description': service[3]})
    return jsonify({'Statut': 0, 'Services': services_list})

# Exemple: http://127.0.0.1:5001/api/v1/services/approve_service?service=1&user=1&approbator=1
@app.route('/api/v1/services/approve_service', methods=['GET'])
def approve_service():
    if 'service' in request.args:
        service = request.args['service']
    else:
        return jsonify({'Statut': 1, 'Message': 'Service not provided'})

    if 'user' in request.args:
        user = request.args['user']
    else:
        return jsonify({'Statut': 1, 'Message': 'User not provided'})

    if 'approbator' in request.args:
        approbator = request.args['approbator']
    else:
        return jsonify({'Statut': 1, 'Message': 'Approbator not provided'})

    cursor.execute("SELECT Role FROM Users WHERE UID=%s", (approbator,))
    approbator = cursor.fetchone()
    if approbator >= 1:
        cursor.execute("SELECT * FROM Services_Approbation_List WHERE UID=%s AND SID=%s", (user, service))
        service = cursor.fetchone()
        if service:
            cursor.execute("INSERT INTO Services_List (UID, SID, ReceiveDate) VALUES (%s, %s, %s)",
                           (user, service[1], time.strftime('%Y-%m-%d %H:%M:%S')))
            cursor.execute("DELETE FROM Services_Approbation_List WHERE UID=%s AND SID=%s", (user, service[1]))
            database.commit()
            return jsonify({'Statut': 0, 'Message': 'Service approved successfully for UID=' + str(user)})
        else:
            return jsonify({'Statut': 1, 'Message': 'Service not found in approbation list'})
    else:
        return jsonify({'Statut': 1, 'Message': 'User is not an approbator'})

# Exemple: http://127.0.0.1:5001/api/v1/services/get_services_list
@app.route('/api/v1/services/get_services_list', methods=['GET'])
def get_services_list():
    cursor.execute("SELECT * FROM Services_List")
    services_list = cursor.fetchall()
    services_list_list = []
    for service_list in services_list:
        services_list_list.append({'UID': service_list[0], 'SID': service_list[1]})
    return jsonify({'Statut': 0, 'Services_List': services_list_list})

# Exemple: http://127.0.0.1:5001/api/v1/services/get_services_approbation_list
@app.route('/api/v1/services/get_services_approbation_list', methods=['GET'])
def get_services_approbation_list():
    cursor.execute("SELECT * FROM Services_Approbation_List")
    services_list = cursor.fetchall()
    services_list_list = []
    for service_list in services_list:
        services_list_list.append({'UID': service_list[0], 'SID': service_list[1]})
    return jsonify({'Statut': 0, 'Services_Approbation_List': services_list_list})

# Exemple: http://127.0.0.1:5001/api/v1/services/get_user_services?user=1
@app.route('/api/v1/services/get_user_services', methods=['GET'])
def get_user_services():
    if 'user' in request.args:
        user = request.args['user']
    else:
        return jsonify({'Statut': 1, 'Message': 'User not provided'})

    cursor.execute("SELECT * FROM Services_List WHERE UID=%s", (user,))
    services_list = cursor.fetchall()
    services_list_list = []
    for service_list in services_list:
        services_list_list.append({'SID': service_list[1]})
    return jsonify({'Statut': 0, 'Services_List': services_list_list})

if __name__ == '__main__':
    app.run(port=5001)
