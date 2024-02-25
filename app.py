from flask import Flask, render_template, request
from instagram_private_api import Client, ClientCompatPatch

app = Flask(__name__)

def get_followers(api):
    followers = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''
        followers_response = api.user_followers(api.authenticated_user_id, rank_token=api.generate_uuid(), max_id=next_max_id)
        followers.extend(followers_response.get('users', []))
        next_max_id = followers_response.get('next_max_id', '')
    return followers

def get_following(api):
    following = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''
        following_response = api.user_following(api.authenticated_user_id, rank_token=api.generate_uuid(), max_id=next_max_id)
        following.extend(following_response.get('users', []))
        next_max_id = following_response.get('next_max_id', '')
    return following

def check_followers(username, password):
    api = Client(username, password)
    api.login()
    followers = get_followers(api)
    following = get_following(api)
    followers_set = set([follower['username'] for follower in followers])
    following_set = set([follow['username'] for follow in following])

    not_following_back = following_set - followers_set
    return not_following_back

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        not_following_back = check_followers(username, password)
        return render_template('result.html', not_following_back=not_following_back)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
