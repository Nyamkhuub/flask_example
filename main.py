import os
import json
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename, send_file, send_from_directory
from werkzeug.wrappers.response import Response

UPLOAD_FOLDER = 'assets/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'jpg'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('get_pdf'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploaded')
def get_pdf(name=None):
    return Response(json.dumps(os.listdir(app.config['UPLOAD_FOLDER'])), mimetype='application/json')
if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=80)