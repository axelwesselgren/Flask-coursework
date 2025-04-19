from server import app
from server.forms import RegisterForm
from flask import render_template, flash, redirect, url_for

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegisterForm()

    if form.validate_on_submit():
        flash('Success', 'success')
        return redirect(url_for('index'))

    return render_template('index.html', form=form)