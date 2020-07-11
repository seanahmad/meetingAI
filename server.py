import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from app.translation import get_full_translation

#UPLOAD_FOLDER = '/Users/shreyjain/Desktop/meetingTranscriber/MeetingTranscriber/audio_files'
UPLOAD_FOLDER = '/Users/shreyjain/Desktop/meetingTranscriber/MeetingTranscriber/audio_files'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}

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
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(full_name)
            return get_full_translation(f'{full_name}')
    return render_template('home.html')

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(port=4000,debug=True)
