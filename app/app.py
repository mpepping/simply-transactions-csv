import os
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory, render_template
from werkzeug.utils import secure_filename

import helpers

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = helpers.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 12 * 1000 * 1000
app.secret_key = helpers.random_string("secret_key")

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in helpers.ALLOWED_EXTENSIONS

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
            random_filename = helpers.random_string(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], random_filename))
            form_currency = request.form["currency"]
            form_broker = request.form["broker"]
            return redirect(url_for('process_file', name=random_filename, currency=form_currency, broker=form_broker))
        else:
            return render_template('error.html', error="Only CSV files are can be processed")
    return render_template('app.html')


@app.route('/process/<name>')
def process_file(name):

    # validate csv file
    try:
        test_file = os.path.join(app.config['UPLOAD_FOLDER'], name)
        helpers.test_csv_schema(test_file)
    except:
        return render_template('error.html', error="Invalid CSV file. Check the file format and try again")

    out_name = "simply_wallst_" + name
    currency = request.args.get('currency')
    helpers.etl_degiro(name, currency)
    return redirect(url_for('download_file', name=out_name, mimetype='text/csv'))


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name, as_attachment=True)


@app.route('/delete/<name>')
def delete_file(name):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], name))
    return redirect(url_for('upload_file'))


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)