from flask import Flask, render_template, request, redirect
import cv2
import os
from datetime import datetime

app = Flask(__name__)

# Create folders automatically
os.makedirs("users", exist_ok=True)
os.makedirs("attendance", exist_ok=True)

# Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Signup Page
@app.route("/signup")
def signup():
    return render_template("signup.html")

# Login Page
@app.route("/login")
def login():
    return render_template("login.html")

# Register User
@app.route("/register", methods=["POST"])
def register():

    username = request.form["username"]
    password = request.form["password"]

    cam = cv2.VideoCapture(0)

    ret, frame = cam.read()

    if ret:
        image_path = f"users/{username}.jpg"
        cv2.imwrite(image_path, frame)

    cam.release()

    with open(f"users/{username}.txt", "w") as file:
        file.write(password)

    return redirect("/login")

# Face Login
@app.route("/face_login", methods=["POST"])
def face_login():

    username = request.form["username"]

    saved_image = f"users/{username}.jpg"

    if not os.path.exists(saved_image):
        return "User Not Found"

    cam = cv2.VideoCapture(0)

    ret, frame = cam.read()

    cam.release()

    login_image = "temp.jpg"

    cv2.imwrite(login_image, frame)

    saved = cv2.imread(saved_image)
    current = cv2.imread(login_image)

    saved_gray = cv2.cvtColor(saved, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)

    difference = cv2.absdiff(saved_gray, current_gray)

    score = difference.mean()

    if score < 50:

        now = datetime.now()

        with open("attendance/attendance.txt", "a") as file:
            file.write(f"{username} - {now}\n")

        return render_template("dashboard.html", username=username)

    else:
        return "Face Not Matched"

# Run App
if __name__ == "__main__":
    app.run(debug=True)