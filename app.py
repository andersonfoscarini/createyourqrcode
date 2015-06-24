#!flask/bin/python
from flask import Flask, jsonify, request, render_template
import requests
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import qrgenerator

UPLOAD_FOLDER = '/home/anderson/Templates'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png','JPG', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = Flask(__name__)
port=2000

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        text = request.form['url']
        print text
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/static/', filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename, text=text))
    return render_template("index.html", text='http://www.coronelbicaco.rs.gov.br')

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    thum = qrgenerator.create_qrcode(request.args.get('text'), os.path.dirname(os.path.abspath(__file__)) + '/static/'+filename)
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)) + '/static/',
                               filename+'qr.jpg')



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=port)
