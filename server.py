"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

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

@app.route("/register", methods=['GET'])
def show_registration():
    """Shows registration form"""

    return render_template("register-form.html")

@app.route('/register', methods=['POST'])
def register_form():

    email = request.form.get("user-email")
    password = request.form.get("user-password")

    find_email = User.query.filter(User.email == email).first()
    # print find_email
    # print "============"

    if find_email:
        flash("You alreday have an account, please log in.")
        return redirect('/login')
    else:
        user = User(email=email, password=password)
        # print user
        # print "============"
        db.session.add(user)
        db.session.commit()
        flash("You successfully made an account.")
        return redirect('/')

@app.route("/login", methods=['GET'])
def show_login():
    """Shows login page"""

    return render_template("login-form.html")

@app.route("/login", methods=['POST'])
def verify_login():
    email = request.form.get("user-email")
    password = request.form.get("user-password")
    print email
    find_user = User.query.filter(User.email== email).first()
    print find_user

    if find_user:
        if find_user.password == password:
            
            session['user'] = find_user.user_id
            print find_user
            flash("You were successfully logged in")
            return redirect("/users/" + str(find_user.user_id))

        else:
            flash('Please enter a valid email/password')
            return redirect('/login')
    else:
        flash('Please enter a valid email/password')
        return redirect('/login')

@app.route("/logout")
def process_logout():
    """Log user out."""

    del session['user']
    flash("You were successfully logged out.")
    return redirect("/")

@app.route("/users/<user_id>")
def show_page(user_id):
    """Shows users page"""
    user = User.query.filter(User.user_id == user_id).first()
    # ratings = Rating.query.filter(Rating.user_id == user_id).all()

    return render_template("users.html", user=user)



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
