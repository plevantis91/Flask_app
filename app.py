from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, choice, sample

app = Flask(__name__, template_folder='template')

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

MOVIES = {'Amadues', 'Chicken Run', 'Dances With Wolves'}

@app.route('/')
def home_page():
    html= """
    <html>
        <body>
            <h1>Home Page!</h1>
            <p>Welcome to my simple app!</p>
            <a href='/hello'>Go to hello page</a>
        </body>
    </html>
    """
    return html

@app.route('/old-home-page')
def redirect_to_home():
    """Redirects to new home page"""
    flash('That page has moved! This is our new home page')
    return redirect("/")

@app.route('/movies')
def show_all_movies():
    """show list of all movies in fake """
    return render_template('./templates/movies.html', movies=MOVIES)

@app.route('/movies/new',methods=["POST"])
def add_movies():
    title = request.form['title']
    if title in MOVIES:
        flash('Movie Already Exists!', 'error')
    else:
        MOVIES.add(title)
        flash("Create Your Movie!", 'success')
    return redirect('/movies')

@app.route('/form')
def show_form():
    return render_template("./templates/form.html")

@app.route('/form-2')
def show_form_2():
    return render_template("./templates/form_2.html")

COMPLIMENTS = ['cool', 'clever', 'tenacious', 'awesome', 'Pythonic']

@app.route('/spell/<word>')
def spell_word(word):
    return render_template('./templates/spell_word.html', word=word)


@app.route('/greet')
def get_greet():
    username = request.args["username"]
    nice_thing = choice(COMPLIMENTS)
    return render_template("./templates/greet.html", username=username, compliment=nice_thing)

@app.route('/greet-2')
def get_greeting_2():
    username = request.args["username"]
    wants = request.args.get("wants_compliments")
    nice_things = sample(COMPLIMENTS,3)
    return render_template("./templates/greet_2.html", username=username,wants_compliments= wants, compliments= nice_things)

@app.route('/lucky')
def lucky_number():
    num = randint(1,10)
    return render_template("./templates/lucky.html", lucky_num=num, msg="You are so lucky!")

@app.route('/hello/<name>')
def say_hello(name):
    return render_template("./templates/hello.html")

@app.route('/goodbye')
def say_goodbye():
    return "GOOD BYE!!!"

@app.route('/search')
def search():
    term = request.args["term"]
    sort = request.args["sort"]
    return f"<h1>Search Results For: {term}</h1>"

# @app.route("/post", methods=["POST"])
# def handle_post_to_my_route():
#     return "YOU Made a Post request"

@app.route('/add-comment')
def add_comment_form():
    return """
    <h1>Add Comment</h1>
        <form method="POST">
            <input type='text' placeholder='comment' name='comment'/>
            <input type='text' placeholder='username' name='username'/>
            <button>Submit</button>
        </form>
        """

@app.route('/add-comment', methods=["POST"])
def save_comment():
    comment= request.form["comment"]
    username= request.form["username"]
    return f"""
    <h1> Saved comments</h1>
    <ul>
        <li>Username: {username}</li>
        <li>Comment: {comment}</li>
    </ul>
"""

@app.route('/r/<subreddit>')
def show_subreddit(subreddit):
    return f"<h1>Browsing The {subreddit} Subreddit</h1>"

@app.route("/r/<subreddit>/comments/<int:post_id>")
def show_commetns(subreddit, post_id):
    return f"<h1>Viewing comments for post with id: {post_id} from the {subreddit} Subreddit</h1>"

POSTS = {
    1:"I like chicken tenders",
    2: "I hate mayo!",
    3: "Double rainbow all the way",
    4: "YOLO OMG (kill me)"
}

@app.route('/posts/<int:id>')
def find_post(id):
    post = POSTS.get(id, "Post Not Found")
    return f"<p>{post}</p>"

app.run(debug=True)
