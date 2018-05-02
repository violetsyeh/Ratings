"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from model import User, Rating, Movie, connect_to_db, db



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    for user in users:
        # print user
        # break
        return render_template("user_list.html", users=users)

@app.route("/show-registration")
def show_registration():
    """Shows registration form"""

    return render_template("register-form.html")

@app.route('/register', methods=['POST'])
def register_form():

    email = request.form["user-email"]
    password = request.form["user-password"]

    find_email = User.query.filter(User.email == email).first()
    # print find_email
    # print "============"

    if find_email:
        return redirect('/login')
    else:
        user = User(email=email, password=password)
        # print user
        # print "============"
        db.session.add(user)
        db.session.commit()
        return redirect('/')

@app.route("/show-login")
def show_login():
    """Shows login page"""

    return render_template("login-form.html")

@app.route("/login", methods=['POST'])
def verify_login():
    email = request.form["user-email"]
    password = request.form["user-password"]
    print email
    find_user_id = User.query.filter(User.email== email).first()
    print find_user_id

    if find_user_id and find_user_id.email == email:
        find_login = User.query.filter(User.password == password).first()
        if find_login == password:
            user_id = find_user_id.user_id
            session['user_id'] = user_id
            flash("You were successfully logged in")
            return redirect('/')
        if not find_user_id:
            flash('Please enter a valid password')
            return redirect('/show-registration')
    else:
        flash('Please register')
        return redirect('/show-registration')

@app.route("/logout")
def process_logout():
    """Log user out."""

    del session['user_id']
    flash("You were successfully logged out.")
    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(port=5000, host='0.0.0.0')
