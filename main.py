from flask import Flask, render_template
import requests

blog_data = requests.get('https://api.npoint.io/1e6d051c36377d107b50').json()

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def home():
    blog_data = requests.get('https://api.npoint.io/1e6d051c36377d107b50').json()
    return render_template("index.html", blog_posts=blog_data)

@app.route('/contact')
def contact():
    return render_template("contact.html")

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

if __name__ == "__main__":
    app.run(debug=True, port=8000)