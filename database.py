import sqlite3
from datetime import datetime
import os

class DenTechDatabase:
    def __init__(self, db_name='dentech.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                visit_date DATE NOT NULL,
                notes TEXT,
                condition_type TEXT,
                prediction_result TEXT,
                confidence_score REAL,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_patient(self, patient_data):
        """Add a new patient to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patients 
            (patient_id, name, age, gender, visit_date, notes, condition_type, 
             prediction_result, confidence_score, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', patient_data)
        
        conn.commit()
        conn.close()
    
    def get_all_patients(self):
        """Get all patients from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT patient_id, name, age, gender, visit_date, condition_type, 
                   prediction_result, confidence_score, created_at
            FROM patients 
            ORDER BY created_at DESC
        ''')
        
        patients = cursor.fetchall()
        conn.close()
        return patients
    
    def get_patient_by_id(self, patient_id):
        """Get a specific patient by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patients WHERE patient_id = ?
        ''', (patient_id,))
        
        patient = cursor.fetchone()
        conn.close()
        return patient
    
    def search_patients(self, search_term):
        """Search patients by name or patient ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT patient_id, name, age, gender, visit_date, condition_type, 
                   prediction_result, confidence_score, created_at
            FROM patients 
            WHERE name LIKE ? OR patient_id LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{search_term}%', f'%{search_term}%'))
        
        patients = cursor.fetchall()
        conn.close()
        return patients

# Initialize database when module is imported
db = DenTechDatabase()