from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.models.user import User

routes_bp = Blueprint('routes_bp', __name__)

# Use this helper to get the auth object from current app
def get_auth():
    return current_app.auth

@routes_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        auth = get_auth()
        if auth.verify_user(username, password):
            session['user'] = username
            return redirect(url_for('routes_bp.welcome'))
        else:
            flash('Invalid credentials')
    # Get static credentials from config
    config = current_app.config
    return render_template('login.html', 
                          static_user=config['STATIC_USER'], 
                          static_pass=config['STATIC_PASS'])

@routes_bp.route('/welcome')
def welcome():
    if 'user' not in session:
        return redirect(url_for('routes_bp.login'))
    return render_template('welcome.html', user=session['user'])

@routes_bp.route('/users')
def users():
    if 'user' not in session:
        return redirect(url_for('routes_bp.login'))
    auth = get_auth()
    user_rows = auth.get_users()
    users = [User(id=row[0], username=row[1]) for row in user_rows]
    return render_template('users.html', users=users)

@routes_bp.route('/add_user', methods=['POST'])
def add_user():
    if 'user' not in session:
        return redirect(url_for('routes_bp.login'))
    username = request.form['username']
    password = request.form['password']
    auth = get_auth()
    if not auth.add_user(username, password):
        flash('Username already exists')
    return redirect(url_for('routes_bp.users'))

@routes_bp.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'user' not in session:
        return redirect(url_for('routes_bp.login'))
    auth = get_auth()
    auth.delete_user(user_id)
    return redirect(url_for('routes_bp.users'))

@routes_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('routes_bp.login'))
