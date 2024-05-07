import os
import warnings
import en_core_web_sm
import json
from flask import Flask, request, jsonify
from pyresparser import ResumeParser

warnings.filterwarnings('ignore')

#nlp = en_core_web_sm.load()

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/parse_resume', methods=['POST'])
def parse_resume():
    try:
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            # Save the uploaded file to the uploads folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Parse the uploaded resume file
            data = ResumeParser(file_path).get_extracted_data()

            # Extract specific fields
            name = data.get('name', '')
            mobile_number = data.get('mobile_number', '')
            email = data.get('email', '')
            skills = data.get('skills', [])

            # Create a dictionary with the extracted fields
            extracted_data = {
                "name": name,
                "mobile_number": mobile_number,
                "email": email,
                "skills": skills
            }

            # Return JSON response
            return jsonify(extracted_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

