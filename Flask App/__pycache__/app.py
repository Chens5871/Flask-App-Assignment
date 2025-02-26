
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from models import mongo, bcrypt, init_db
from config import Config
import random
import string

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and mail
init_db(app)
mail = Mail(app)

# Route: User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

        # Check if user exists
        user = mongo.db.users.find_one({"email": email})
        if user:
            flash("Email already registered!", "danger")
            return redirect(url_for("register"))

        mongo.db.users.insert_one({"email": email, "password": password})
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# Route: User Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = mongo.db.users.find_one({"email": email})
        if user and bcrypt.check_password_hash(user["password"], password):
            session["user"] = email
            return redirect(url_for("dashboard"))

        flash("Invalid credentials!", "danger")

    return render_template("login.html")


# Route: Forgot Password
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = mongo.db.users.find_one({"email": email})

        if user:
            try:
                # Generate a temporary password and send it to the user's email
                temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                hashed_temp_password = bcrypt.generate_password_hash(temp_password).decode("utf-8")

                mongo.db.users.update_one({"email": email}, {"$set": {"password": hashed_temp_password}})

                msg = Message("Password Reset", sender="your_email@gmail.com", recipients=[email])
                msg.body = f"Your new temporary password is: {temp_password}"
                mail.send(msg)

                flash("A new password has been sent to your email.", "success")
                return redirect(url_for("login"))
            except Exception as e:
                flash(f"An error occurred while sending the email: {str(e)}", "danger")
        else:
            flash("Email not found!", "danger")

    return render_template("forgot_password.html")


# Route: Password Reset
@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("reset_password"))

        hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        mongo.db.users.update_one({"email": session["user"]}, {"$set": {"password": hashed_password}})
        
        flash("Password updated successfully!", "success")
        return redirect(url_for("login"))

    return render_template("reset_password.html")


# Route: Dashboard (User enters contact details)
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        contact = {
            "email": session["user"],
            "mobile": request.form["mobile"],
            "address": request.form["address"],
            "registration_number": request.form["registration_number"]
        }
        mongo.db.contacts.insert_one(contact)
        flash("Contact details saved!", "success")

    return render_template("dashboard.html")

# Route: Search Contacts by Registration Number
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        reg_number = request.form["registration_number"]
        contact = mongo.db.contacts.find_one({"registration_number": reg_number})

        if contact:
            return render_template("dashboard.html", contact=contact)
        else:
            flash("No contact found!", "danger")

    return render_template("dashboard.html")

# Route: Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

