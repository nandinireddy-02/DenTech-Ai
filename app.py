from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
import random
from database import db

app = Flask(__name__)
app.secret_key = 'dentech_ai_secret_key_2026'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_patient_id():
    """Generate a unique patient ID"""
    timestamp = datetime.now().strftime("%Y%m%d")
    random_digits = str(random.randint(1000, 9999))
    return f"DT{timestamp}{random_digits}"

def simulate_ai_analysis(image_path, condition_type):
    """
    Simulate AI analysis for dental conditions
    In production, this would call actual AI models
    """
    import time
    time.sleep(2)  # Simulate processing time
    
    # Simulate random but realistic results
    if condition_type == 'hypodontia':
        conditions = [
            ('No Hypodontia Detected', 92.5, 'Normal tooth development pattern observed. All expected tooth structures are present in the X-ray image.'),
            ('Mild Hypodontia', 78.3, 'Missing 1-2 teeth detected. This is a common developmental variation that may require orthodontic consultation.'),
            ('Moderate Hypodontia', 85.1, 'Missing 3-5 teeth identified. Comprehensive treatment planning recommended with prosthodontic evaluation.')
        ]
    else:  # tooth_discoloration
        conditions = [
            ('No Significant Discoloration', 89.7, 'Normal tooth coloration within healthy parameters. No immediate treatment required.'),
            ('Mild Surface Staining', 76.4, 'Surface-level discoloration detected. Professional cleaning and whitening may be beneficial.'),
            ('Moderate Discoloration', 82.1, 'Noticeable discoloration present. Consider professional whitening treatment or cosmetic consultation.'),
            ('Severe Discoloration', 91.3, 'Significant discoloration detected. Comprehensive evaluation recommended to determine underlying cause.')
        ]
    
    result, confidence, explanation = random.choice(conditions)
    return result, confidence, explanation

@app.route('/')
def index():
    """Homepage with dental animations"""
    return render_template('index.html')

@app.route('/patient-details')
def patient_details():
    """Patient details form page"""
    return render_template('patient_details.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    """Image upload and analysis page"""
    if request.method == 'GET':
        # Get patient data from session or query params
        patient_data = request.args.to_dict()
        return render_template('upload.html', patient_data=patient_data)
    
    if request.method == 'POST':
        # Handle form data
        patient_data = {
            'patient_id': request.form.get('patient_id'),
            'name': request.form.get('name'),
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'visit_date': request.form.get('visit_date'),
            'notes': request.form.get('notes', ''),
            'condition_type': request.form.get('condition_type')
        }
        
        # Handle file upload
        if 'dental_image' not in request.files:
            flash('No image file selected')
            return redirect(request.url)
        
        file = request.files['dental_image']
        if file.filename == '':
            flash('No image file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Create unique filename
            unique_filename = f"{patient_data['patient_id']}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Simulate AI analysis
            result, confidence, explanation = simulate_ai_analysis(
                file_path, patient_data['condition_type']
            )
            
            # Save to database
            db_data = (
                patient_data['patient_id'],
                patient_data['name'],
                int(patient_data['age']),
                patient_data['gender'],
                patient_data['visit_date'],
                patient_data['notes'],
                patient_data['condition_type'],
                result,
                confidence,
                unique_filename
            )
            
            db.add_patient(db_data)
            
            # Redirect to results page
            return redirect(url_for('results', patient_id=patient_data['patient_id']))
        
        flash('Invalid file type. Please upload PNG, JPG, or JPEG images only.')
        return redirect(request.url)

@app.route('/results/<patient_id>')
def results(patient_id):
    """Display analysis results"""
    patient = db.get_patient_by_id(patient_id)
    if not patient:
        flash('Patient not found')
        return redirect(url_for('index'))
    
    return render_template('results.html', patient=patient)

@app.route('/history')
def patient_history():
    """Patient history page"""
    search_term = request.args.get('search', '')
    
    if search_term:
        patients = db.search_patients(search_term)
    else:
        patients = db.get_all_patients()
    
    return render_template('history.html', patients=patients, search_term=search_term)

@app.route('/api/generate-patient-id')
def api_generate_patient_id():
    """API endpoint to generate new patient ID"""
    return jsonify({'patient_id': generate_patient_id()})

if __name__ == '__main__':
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)