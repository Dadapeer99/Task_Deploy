from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = 'Dadapeer' 

# Dummy login credentials
dummy_credentials = {
    "email": "test@example.com",
    "password": "password123"
}

# Load tasks from a file
def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to a file
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)

# Home route to display login page
@app.route('/')
def login():
    # if 'email' in session:
    #     return redirect(url_for('index'))
    return render_template('login.html')

# Handle login form submission
@app.route('/login', methods=['POST'])
def handle_login():
    email = request.form['email']
    password = request.form['password']

    if email == dummy_credentials['email'] and password == dummy_credentials['password']:
        # session['email'] = email
        # return redirect(url_for('index'))
        return render_template("index.html")
    else:
        return "Invalid credentials. Please try again."

# Logout route
@app.route('/logout')
def logout():
    # session.pop('email', None)
    return redirect(url_for('login'))

# Dashboard route (after login)
@app.route('/dashboard')
def index():
    # if 'email' not in session:
    #     return redirect(url_for('login'))
    return render_template('index.html')

# API routes for managing tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    tasks = load_tasks()
    new_task = request.json
    new_task['id'] = len(tasks) + 1
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return jsonify({'success': True})

@app.route('/tasks/<int:task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            break
    save_tasks(tasks)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
