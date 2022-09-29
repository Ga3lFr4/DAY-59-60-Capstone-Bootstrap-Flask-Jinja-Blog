from flask import Flask, render_template, request
import requests
from smtplib import SMTP
from dotenv import load_dotenv
import os

load_dotenv("variables.env")
FROM_EMAIL = os.getenv('FROM_EMAIL')
TO_EMAIL = os.getenv('TO_EMAIL')
PW = os.getenv('MAIL_PW')


blog_data = requests.get('https://api.npoint.io/1e6d051c36377d107b50').json()

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def home():
    blog_data = requests.get('https://api.npoint.io/1e6d051c36377d107b50').json()
    return render_template("index.html", blog_posts=blog_data)


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/post/<int:id>')
def show_post(id):
    blog_data = requests.get('https://api.npoint.io/1e6d051c36377d107b50').json()
    blog_index = id - 1
    blog_post = blog_data[blog_index]
    post_title = blog_post["title"]
    post_subtitle = blog_post["subtitle"]
    post_body = blog_post["body"]
    return render_template("post.html", title=post_title, body=post_body, subtitle=post_subtitle)

@app.route("/contact", methods=['POST', 'GET'])
def receive_data():
    if request.method == 'GET':
        return render_template('contact.html', h1="Contact me")
    else:
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        with SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=FROM_EMAIL, password=PW)
            connection.sendmail(from_addr=FROM_EMAIL, to_addrs=TO_EMAIL, msg=f"Subject:New form\n\n"
                                                                             f"Name: {name}\nEmail: {email}\n"
                                                                             f"Phone: {phone}\nMessage: {message}")
        return render_template('contact.html', h1="Message received !")

if __name__ == "__main__":
    app.run(debug=True, port=8000)