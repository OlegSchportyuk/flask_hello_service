from flask import (Flask, request, jsonify, abort, 
redirect, url_for, render_template, send_file, flash)

import joblib
import numpy as np
import pandas as pd

knn = joblib.load('knn.pkl')

app = Flask(__name__)

@app.route("/")
def hello_world():
    #print('hi')
    return "<h1>Hello, my very best friend!</h1>"


@app.route("/user/<username>")
def show_user_profile(username):
    #show the user profile for that user
    return f'User {username}'


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


@app.route("/avg/<nums>")
def avg(nums):
    nums = nums.split(',')
    nums = [float(num) for num in nums]
    mean_nums = mean(nums)
    print(mean_nums)
    return f'Average - {mean_nums}'


@app.route("/iris/<params>")
def iris(params):
    try:
        flowers = ['setosa', 'versicolor', 'virginica']

        params = params.split(',')
        params = [float(param) for param in params]

        params = np.array(params).reshape(1, -1)

        predict = knn.predict(params)

        flower = flowers[predict[0]-1]
    except:
        return redirect(url_for('bad_request'))    

    #return f'{predict}'
    return f'<title>{flower}</title> \
             <h1>{flower}</h1> \
             <img src="/static/{flower}.jpg" alt="setosa">'


@app.route('/show_image')
def show_image(flower='setosa'):

    return f'<img src="/static/{flower}.jpg" alt="setosa">'


@app.route('/iris_post', methods=['POST'])
def add_message():

    try:
        content = request.get_json()

        params = content['flower'].split(',')
        params = [float(param) for param in params]

        params = np.array(params).reshape(1, -1)

        predict = knn.predict(params)

        predict = {'class':str(predict[0])}

        print(content) # Do your processing
    except:
        return redirect(url_for('bad_request'))


    return jsonify(predict)


@app.route('/badrequest400')
def bad_request():
    abort(400)


from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import os

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        f = form.file.data
        #filename = secure_filename(f.filename)

        #filename = f'{form.name.data}.txt'
        #f.save(os.path.join(
        #    filename
        #))

        filename = f'{form.name.data}.csv'

        df = pd.read_csv(f, header=None)

        predict = knn.predict(df)
        result = pd.DataFrame(predict)
        result.to_csv(filename, index=False)



        #return(str(form.name))
        return send_file(
            filename,
            mimetype='text/csv',
            download_name=filename,
            as_attachment=True
        )
    return render_template('submit.html', form=form)



UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print('1')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            print('2')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('3')
            #return redirect(url_for('download_file', name=filename))
            return 'file uploaded'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''