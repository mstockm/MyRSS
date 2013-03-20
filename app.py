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
from rss.models.item import Item

from rss.templates.helpers import format_timestamp


app = Flask(__name__)
app.secret_key = os.environ.get('secret_key', 'bad_secret_key')
app.jinja_env.globals.update(format_timestamp=format_timestamp)


@app.route('/')
def index():
    if session.get('user_id'):
        return redirect(url_for('stream'))
    else:
        return redirect(url_for('login'))


@app.route('/starred', methods=['GET'])
def starred_stream():
    user_id = session.get('user_id')
    user = User.get(user_id)
    if not user:
        return redirect(url_for('login'))

    stream, unread_count = user.get_starred_stream_with_count()
    before = None
    if stream:
        before = stream[-1]['date']

    return render_template('stream.html',
        stream=stream,
        feed_names=user.feed_names,
        email=user.email,
        before=before,
        unread_count=unread_count,
        unread=True,
        starred=True
    )


@app.route('/stream', methods=['GET'])
def stream():
    user_id = session.get('user_id')
    user = User.get(user_id)
    if not user:
        return redirect(url_for('login'))

    unread = False if request.args.get('items') == 'all' else True

    stream, unread_count = user.get_stream_with_count(unread)
    before = None
    if stream:
        before = stream[-1]['date']

    return render_template('stream.html',
        stream=stream,
        feed_names=user.feed_names,
        email=user.email,
        before=before,
        unread_count=unread_count,
        unread=unread,
        starred=False
    )


@app.route('/stream_ajax', methods=['GET'])
def stream_ajax():
    user_id = session.get('user_id')
    user = User.get(user_id)
    if not user:
        return redirect(url_for('login'))

    before_time = request.args.get('before')
    unread = False if request.args.get('items') == 'all' else True
    stream = user.get_stream(before_time=before_time, unread_only=unread)
    before = ""
    if stream:
        before = stream[-1]['date']

    content = render_template('stream_ajax.html', stream=stream)
    length = len(stream)

    return json.dumps({
        'content': content,
        'length': length,
        'before': before
    })


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


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))


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


@app.route('/item/read', methods=['POST'])
def mark_as_read():
    user_id = session.get('user_id')
    user = User.get(user_id)
    if not user:
        return make_response(json.dumps({'message': "Invalid User ID"}), 400)

    item_id = request.form.get('item_id')
    item = Item.get_for_user(item_id, user)
    item.mark_as_read()
    item.save()

    return json.dumps({'message': "Success"})


@app.route('/item/star', methods=['POST'])
def star():
    user_id = session.get('user_id')
    user = User.get(user_id)
    if not user:
        return make_response(json.dumps({'message': "Invalid User ID"}), 400)

    item_id = request.form.get('item_id')
    item = Item.get_for_user(item_id, user)
    item.star()
    item.save()

    return json.dumps({'message': "Success"})


@app.route('/item/unstar', methods=['POST'])
def unstar():
    user_id = session.get('user_id')
    user = User.get(user_id)
    if not user:
        return make_response(json.dumps({'message': "Invalid User ID"}), 400)

    item_id = request.form.get('item_id')
    item = Item.get_for_user(item_id, user)
    item.unstar()
    item.save()

    return json.dumps({'message': "Success"})


if __name__ == '__main__':
    app.run(debug=True)
