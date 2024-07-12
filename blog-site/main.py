'''
======================================================================================

In an era where programming knowledge is widespread, starting another blog might seem 
mundane to some. However, this blog was developed as part of the creator’s journey 
through the myriad of technologies encountered in the web development landscape. The 
creator is a tenacious and self-driven individual, aware of his shortcomings, and 
constantly seeks to improve his knowledge in any field he chooses to explore.

Technologies Employed:
    - Python: Main language for implementation
    - HTML: Structure of the website
    - CSS: Styling the website
    - JavaScript: Navbar functionality
    - Bootstrap: CSS framework for reusable code
    - Flask: Web framework
    - Jinja: Template engine
    - SMTPLib: Sending contact emails

Course Utilized:
    - Python Professional Bootcamp by App Brewery

======================================================================================
'''
from flask import Flask, render_template, request
import smtplib
import requests

EMAIL = None 
PASSWORD = None

response = requests.get("https://api.npoint.io/31babe0a95af13f1f33a")
posts = response.json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    '''
    This function sets up the main page using the index 
    HTML file and passes all posts to be displayed on the page.
    '''
    return render_template("index.html", all_posts=posts)

@app.route('/contact', methods=["GET", "POST"])
def contact():
    '''
    This function handles the contact page route. It renders the HTML file.
    If a POST request is made, it sends an email using the smtplib library.
    It checks if data was submitted, then extracts the data and updates the page.
    '''
    if request.method == "POST":
        data = request.form
        send_message_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", front_message="Message Sent")

    return render_template("contact.html", front_message="Contact Me")

@app.route('/about')
def about():
    '''
    This function handles the about page route and renders the HTML file.
    '''
    return render_template("about.html")

@app.route('/post/<post_id>')
def get_post(post_id):
    '''
    This function retrieves a specific post by its ID. It searches through the 
    posts from the API response and passes the found post to the post HTML file.
    If the post is not found, it returns a 404 error.
    '''
    current_post = None
    for post in posts:
        if int(post_id) == int(post['id']):
            current_post = post
            break

    if current_post is None:
        return "Post not found", 404
    
    return render_template("post.html", post=current_post)

def send_message_email(name, email, phone, message):
    '''
    Generates an email message using string formatting and sends it
    using the smtplib library.
    '''
    email_message = f"Subject: New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(EMAIL, email, email_message)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
