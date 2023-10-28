from flask import Flask, render_template, request
import json
from supabase import create_client, Client
from flask_mail import Mail

# Initializing of flask app
app = Flask(__name__)

# Configuring the flask_mail API
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'priyamsarkar10a.sgips@gmail.com',
    MAIL_PASSWORD = 'xhwdiybgdhlpxzdl',
)

# Initializing the flask_mail feature in the app
mail = Mail(app)

# Reading of params for connecting to the backend
with open('config.json', 'r') as file:
    params = json.load(file)["params"]
    file.close()
# Connection to the backend
url = params["url"]
api_key = params["api_key"]
supabase = create_client(url, api_key)

# Reading the index properties from the json file
with open('config.json', 'r') as file:
    index_prop = json.load(file)["index_properties"]
    file.close()

# Reading the about properties from the json file
with open('config.json', 'r') as file:
    about_prop = json.load(file)["about_properties"]
    file.close()

# Reading the post properties from the json file
with open('config.json', 'r') as file:
    post_prop = json.load(file)["post_properties"]
    file.close()


# Home Route
@app.route('/')
def index():
    data = supabase.table('posts').select('title', 'about', 'email').execute()
    return render_template('index.html', index_prop=index_prop, data=data)

# About Route
@app.route('/about')
def about():
    return render_template('about.html', about_prop=about_prop, index_prop=index_prop)

# Post Route
@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form.get('title')
        about = request.form.get('about')
        email = request.form.get('email')
        supabase.table('posts').insert({"title":title, "about":about, "email": email}).execute()
        mail.send_message('Message from Tech Bar', sender=email, recipients=['priyamsarkar10a.sgips@gmail.com'], body= "Email: " + email + "\n" + "Title: " + title + "\n" + "About: " + about)

        return render_template('post.html',post_prop=post_prop, index_prop=index_prop)
    else:
        return render_template('post.html',post_prop=post_prop, index_prop=index_prop)



if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')