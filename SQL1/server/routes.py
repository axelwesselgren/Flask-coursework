from flask import render_template, flash, redirect, url_for
from server import app
from server.dbhandler import create_connection
from server.forms import WormForm, SortForm

@app.route('/', methods=['POST', 'GET'])
def index():
    sort_form = SortForm()
    worm_form = WormForm()
    sort_order = "ASC"

    conn = create_connection()
    cur = conn.cursor()

    if sort_form.validate_on_submit():
        sort_order = sort_form.sort.data

    if worm_form.validate_on_submit():
        name = worm_form.name.data
        length = worm_form.length.data

        cur.execute(f"INSERT INTO worms(name, length) VALUES ('{name}', {length})")
        conn.commit()
        flash(f'Created worm', 'success')

    try:
        cur.execute(f'SELECT * FROM worms ORDER BY length {sort_order}')
        worms = cur.fetchall()

        return render_template('index.html', worms=worms, worm_form=worm_form, sort_form=sort_form)
    finally:
        cur.close()
        conn.close()

@app.route("/delete/<mask_id>")
def delete_worm(mask_id):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute(f'DELETE FROM worms WHERE id = {mask_id}')
    conn.commit()
    flash('Deleted worm', 'success')

    return redirect(url_for('index'))