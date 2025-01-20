from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from prediction import predict_result
from metadata import extract_metadata

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Predict result using ELA and metadata
        prediction, confidence, ela_filename = predict_result(file_path)
        metadata = extract_metadata(file_path)
        
        # Build the URLs for original and ELA images
        original_image_url = url_for('static', filename=f'uploads/{filename}')
        ela_image_url = url_for('static', filename=f'uploads/{ela_filename}')

        return render_template('result.html', 
                               original_image_url=original_image_url, 
                               ela_image_url=ela_image_url, 
                               prediction=prediction, 
                               confidence=confidence, 
                               metadata=metadata)

if __name__ == '__main__':
    app.run(debug=True)
