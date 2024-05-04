from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # replace with your secret key
app.config['UPLOAD_FOLDER'] = '../static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, 'PDFs only!')], render_kw={'multiple': True})
    submit = SubmitField("Upload File")

@app.route("/", methods=['GET', 'POST'])
def index():
    form = UploadFileForm()
    if form.validate_on_submit():
        for uploaded_file in request.files.getlist('file'):
            if uploaded_file.filename != '':
                filename = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))
    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)