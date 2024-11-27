from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from caption_model import generate_caption

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploaded_images'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('generate_caption', filename=filename))

@app.route('/caption/<filename>')
def generate_caption_route(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    caption = generate_caption(image_path)
    return render_template('caption.html', image_url=url_for('static', filename=f'uploaded_images/{filename}'), caption=caption)


if __name__ == '__main__':
    app.run(debug=True)
