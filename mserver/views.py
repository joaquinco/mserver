from flask import render_template

from mserver.mserver import app


@app.route('/')
def index():
    try:
        return render_template('index.html')
    except:
        return 'Sorry men! Parece que no compilaste el frontend'
