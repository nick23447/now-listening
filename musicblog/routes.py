from musicblog import app


@app.route('/')
@app.route('/home')
def home():
    return "<h2>Hello World</h2>"