from flask import Flask, request, render_template, send_from_directory, url_for
import os
import qrcode
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return "No file uploaded", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Generate public URL
    file_url = url_for('uploaded_file', filename=filename, _external=True)

    # Generate QR code
    qr = qrcode.make(file_url)
    qr_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}_qr.png')
    qr.save(qr_path)

    return f'''
        <p>File uploaded: <a href="{file_url}" target="_blank">{file_url}</a></p>
        <p>Scan this QR code to access the file:</p>
        <img src="/static/uploads/{filename}_qr.png" alt="QR Code" />
        <p><a href="/">Upload another file</a></p>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
