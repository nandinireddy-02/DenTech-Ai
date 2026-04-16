import sqlite3
from datetime import datetime
import os
import time

class DenTechDatabase:
    def __init__(self, db_name='dentech.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name, timeout=30)
        conn.execute('PRAGMA busy_timeout = 30000')
        return conn
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()

            # WAL mode reduces writer-reader contention for SQLite.
            cursor.execute('PRAGMA journal_mode = WAL')
            cursor.execute('PRAGMA synchronous = NORMAL')

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
        finally:
            conn.close()
    
    def add_patient(self, patient_data):
        """Add a new patient to the database"""
        for attempt in range(5):
            conn = self.get_connection()
            try:
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT INTO patients 
                    (patient_id, name, age, gender, visit_date, notes, condition_type, 
                     prediction_result, confidence_score, image_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', patient_data)

                conn.commit()
                return
            except sqlite3.OperationalError as exc:
                conn.rollback()
                is_locked = 'database is locked' in str(exc).lower()
                if not is_locked or attempt == 4:
                    raise
                time.sleep(0.2 * (attempt + 1))
            finally:
                conn.close()
    
    def get_all_patients(self):
        """Get all patients from the database"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT patient_id, name, age, gender, visit_date, condition_type, 
                       prediction_result, confidence_score, created_at
                FROM patients 
                ORDER BY created_at DESC
            ''')

            return cursor.fetchall()
        finally:
            conn.close()
    
    def get_patient_by_id(self, patient_id):
        """Get a specific patient by ID"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM patients WHERE patient_id = ?
            ''', (patient_id,))

            return cursor.fetchone()
        finally:
            conn.close()
    
    def get_next_patient_number(self):
        """Get the next patient serial number"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM patients')
            count = cursor.fetchone()[0]

            # Return next number (count + 1) with leading zeros
            return f"{count + 1:04d}"
        finally:
            conn.close()
    
    def search_patients(self, search_term):
        """Search patients by name or patient ID"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT patient_id, name, age, gender, visit_date, condition_type, 
                       prediction_result, confidence_score, created_at
                FROM patients 
                WHERE name LIKE ? OR patient_id LIKE ?
                ORDER BY created_at DESC
            ''', (f'%{search_term}%', f'%{search_term}%'))

            return cursor.fetchall()
        finally:
            conn.close()

# Initialize database when module is imported
db = DenTechDatabase()