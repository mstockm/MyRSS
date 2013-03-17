import os
from flask import (
    Flask,
    request,
    redirect,
    flash,
    render_template,
    session,
    url_for
)
from rss.user import User


app = Flask(__name__)
app.secret_key = os.environ.get('secret_key', 'bad_secret_key')


@app.route('/')
def index():
    if session.get('user_id'):
        return redirect(url_for('stream'))
    else:
        return redirect(url_for('login'))


@app.route('/stream', methods=['GET'])
def stream():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User(user_id)

    user.add_feed('http://feeds2.feedburner.com/PitchforkLatestNews')
    user.add_feed('http://feeds.feedburner.com/seriouseatsfeaturesvideos?format=xml')
    user.add_feed('http://pandodaily.com.feedsportal.com/c/35141/f/650422/index.rss')

    user.update_stream()

    return render_template('stream.html', stream=user.stream)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('user_id'):
            return redirect(url_for('stream'))
        return render_template('login.html')

    user_id = request.form.get('user_id')
    if not user_id:
        flash('No User ID provided')
        return redirect(url_for('login'))

    session['user_id'] = user_id
    return redirect(url_for('stream'))


if __name__ == '__main__':
    app.run(debug=True)
