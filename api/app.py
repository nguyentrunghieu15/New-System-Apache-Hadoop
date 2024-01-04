import os
from subprocess import PIPE, Popen
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = './temp'
HDFS_PATH_NEWS  = '/news'
HDFS_PATH_STOCKS  = '/stocks'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'the random string'

@app.route('/')
def ping():
    return "OK"

@app.route('/fsputnew', methods=['POST',"GET"])
def put_news():
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
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            put = Popen(["hadoop", "fs", "-put", f"{os.path.join(app.config['UPLOAD_FOLDER'], filename)}", HDFS_PATH_NEWS], stdin=PIPE, bufsize=-1)
            put.communicate()
    return "OK"

@app.route('/fsputstock', methods=['POST',"GET"])
def put_stocks():
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
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            put = Popen(["hadoop", "fs", "-put", f"{os.path.join(app.config['UPLOAD_FOLDER'], filename)}", HDFS_PATH_STOCKS], stdin=PIPE, bufsize=-1)
            put.communicate()
    return "OK"
@app.route('/fsls/<path>', methods=['GET'])
def get_list_file(path):
    if request.method == 'GET':
        hdfs_path = path
        process = Popen(f'hdfs dfs -ls -h {hdfs_path}', shell=True, stdout=PIPE, stderr=PIPE)
        std_out, std_err = process.communicate()
        list_of_file_names = [fn.split(' ')[-1].split('/')[-1] for fn in std_out.decode().split('\n')[1:]][:-1]
        return list_of_file_names        