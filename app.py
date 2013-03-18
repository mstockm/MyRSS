import os
import sys
from flask import (
    Flask,
    request,
    redirect,
    flash,
    render_template,
    session,
    url_for,
    make_response,
    json
)

sys.path.append(os.path.abspath(os.pardir))

from rss.models.user import User


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
    user = User.get(user_id)
    if not user:
        return redirect(url_for('login'))

    stream = user.get_stream()

    return render_template('stream.html',
        stream=stream,
        feed_names=user.feed_names
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.get(user_id)
        if user:
            return redirect(url_for('stream'))
        return render_template('login.html')

    email = request.form.get('email')
    if not email:
        flash('No email provided')
        return redirect(url_for('login'))

    user = User.get_by_email(email)
    if not user:
        user = User.create(email)
    session['user_id'] = user._id
    return redirect(url_for('stream'))


@app.route('/add', methods=['GET', 'POST'])
def add_feed():
    user_id = session.get('user_id')
    user = User.get(user_id)
    if not user:
        flash('Invalid User ID')
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('add_feed.html', feed_names=user.feed_names)

    feed_link = request.form.get('feed_link')
    user.add_feed(feed_link)
    flash('Feed added successfully')
    return redirect(url_for('stream'))


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    user_id = session.get('user_id')
    user = User.get(user_id)
    if not user:
        return make_response(json.dumps({'message': "Invalid User ID"}), 400)

    feed_link = request.form.get('feed')
    user.remove_feed(feed_link)
    return json.dumps({'message': "Success"})


if __name__ == '__main__':
    app.run(debug=True)
