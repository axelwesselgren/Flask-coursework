from flask import render_template, request, flash, redirect, url_for
from server import app
from werkzeug.utils import secure_filename
import os

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('file')

        for file in files:
            if os.path.splitext(file.filename)[1] not in app.config['UPLOAD_EXTENSIONS']:
                flash('File not supported', 'danger')
                return redirect(url_for('upload'))
            
        for file in files:
            file.save(
                os.path.join(
                    app.root_path, 
                    'static', 
                    'uploads', 
                    secure_filename(file.filename)
                )
            )

        flash('Sucess uploaded files', 'success')
        return redirect(url_for('upload'))
    else:
        return render_template('upload.html')
    