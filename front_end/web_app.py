

from flask import Flask, request, render_template, redirect, url_for

import config
import api.api

app = Flask(__name__)

@app.route('/client')
def home_client():
    return render_template('client.html')

@app.route('/client/send', methods=['POST'])
def send_data():
    test = request.form.get('test')
    api.api.send_to_server({'test': test})
    return redirect(url_for('home'))

def run_web_app():
    app.run(port=config.WEB_APP_PORT, use_reloader=False, debug=False)

