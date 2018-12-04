from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Mohsin'}
	posts = [
		{
			'author': {'username': 'Moss'},
			'body': 'Hopefully nothing breaks'
		},
		{
			'author': {'username': 'Moose'},
			'body': 'It will probably break'
		}
	]
	#hand the 'index.html' page these bits of data
	return render_template('index.html', title='Home', user=user, posts=posts)