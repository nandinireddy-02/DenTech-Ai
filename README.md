# DenTech AI 🦷 - Your Online Dental Friend

A modern AI-based web application designed to assist dental professionals with automated analysis of dental images. The system provides decision-support for two key dental conditions: Hypodontia (from X-ray images) and Tooth Discoloration (from photographs).

![DenTech AI](https://img.shields.io/badge/DenTech-AI-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHRleHQgeT0iMjAiIGZvbnQtc2l6ZT0iMjAiPvCfprc8L3RleHQ+PC9zdmc+)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green?style=flat&logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)](https://python.org)
[![SQLite](https://img.shields.io/badge/SQLite-Database-orange?style=flat&logo=sqlite)](https://sqlite.org)

## ✨ Features

### 🎨 Modern UI Design
- Premium medical SaaS interface with glassmorphism effects
- Dental-themed animations and professional color scheme
- Responsive design with smooth transitions
- 3D tooth animations and SVG drawing effects

### 🦷 AI Analysis Capabilities
- **Hypodontia Detection**: Analyze X-ray images for missing teeth
- **Tooth Discoloration Analysis**: Examine photographs for discoloration patterns
- Confidence scoring and professional explanations
- Clinical recommendations based on AI findings

### 👤 Patient Management
- Comprehensive patient information forms
- Secure database storage with SQLite
- Patient history tracking and search functionality
- Auto-generated patient IDs with timestamps

### 📊 Professional Features
- Detailed analysis results with visual confidence meters
- Medical-grade disclaimer and safety information
- Export capabilities for patient records
- Professional language suitable for dental practitioners

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git for version control

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nandinireddy-02/DenTech-Ai.git
   cd DenTech-Ai
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000` to access DenTech AI

## 📁 Project Structure

```
DenTech-AI/
├── app.py                 # Main Flask application
├── database.py           # Database models and operations
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── dentech.db           # SQLite database (created automatically)
├── uploads/             # Uploaded dental images
├── static/
│   ├── css/
│   │   └── style.css    # Dental-themed styling
│   ├── js/             # JavaScript files (future)
│   └── images/         # Static images
└── templates/
    ├── index.html      # Homepage with animations
    ├── patient_details.html  # Patient information form
    ├── upload.html     # Image upload and analysis
    ├── results.html    # AI analysis results
    └── history.html    # Patient history viewer
```

## 🎮 Usage Guide

### 1. Homepage
- Features dental-themed animations including 3D rotating tooth
- Start new patient analysis or view patient history
- Professional medical interface with glassmorphism design

### 2. Patient Registration
- Enter patient details (Name, Age, Gender, Visit Date)
- Auto-generated patient IDs for tracking
- Optional notes field for additional information

### 3. Image Analysis
- Choose analysis type:
  - **Hypodontia Detection** for X-ray images
  - **Tooth Discoloration** for tooth photographs
- Drag-and-drop or click to upload images
- Real-time image preview with validation

### 4. AI Results
- Comprehensive analysis results with confidence scoring
- Professional explanations and clinical recommendations
- Visual confidence meters and status indicators
- Save patient records automatically

### 5. Patient History
- View all previous analyses in an organized table
- Search and filter functionality
- Export options for patient records
- Click any row to view detailed results

## 🔧 Configuration

### Database Setup
The application automatically creates a SQLite database (`dentech.db`) on first run. No manual database setup required.

### Upload Configuration
- **Supported formats**: PNG, JPG, JPEG, GIF
- **Maximum file size**: 10MB
- **Upload directory**: `uploads/` (created automatically)

### Development Mode
For development with auto-reload:
```bash
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python app.py
```

## 🤖 AI Implementation Notes

The current version includes **simulated AI analysis** for demonstration purposes. The system:
- Provides realistic confidence scores (75-95%)
- Returns contextually appropriate results
- Simulates processing time for authentic feel
- Maintains consistent result quality

### Future AI Integration
To integrate actual AI models:

1. **Add AI dependencies** (uncomment in `requirements.txt`):
   ```
   tensorflow==2.13.0
   opencv-python==4.8.1.78
   pillow==10.0.1
   numpy==1.24.3
   ```

2. **Replace simulation function** in `app.py`:
   - Update `simulate_ai_analysis()` with actual model calls
   - Add image preprocessing and model inference
   - Implement proper error handling for AI failures

3. **Model files**:
   - Add trained models to `models/` directory
   - Update model loading in application startup

## 📊 Database Schema

### Patients Table
| Column | Type | Description |
|--------|------|-------------|
| patient_id | TEXT | Primary key, auto-generated |
| name | TEXT | Patient full name |
| age | INTEGER | Patient age |
| gender | TEXT | Patient gender |
| visit_date | DATE | Date of dental visit |
| notes | TEXT | Optional notes |
| condition_type | TEXT | Analysis type (hypodontia/discoloration) |
| prediction_result | TEXT | AI analysis result |
| confidence_score | REAL | AI confidence percentage |
| image_path | TEXT | Uploaded image filename |
| created_at | TIMESTAMP | Record creation time |

## 🎨 Styling Features

### Dental Color Palette
- **Primary Blue**: `#4A90E2` (Professional medical blue)
- **Dental Teal**: `#50C9C3` (Calming accent color)
- **Light Background**: `#E8F4FD` (Soft medical background)
- **Success Green**: `#28A745` (Positive results)
- **Warning Amber**: `#FFC107` (Caution indicators)

### Animation Effects
- Floating tooth background elements
- 3D rotating tooth models
- SVG drawing animations
- Smooth glassmorphism cards
- Professional hover effects

## ⚕️ Medical Compliance

### Disclaimer
DenTech AI is designed as a **decision-support tool** for dental professionals:
- Not a replacement for professional diagnosis
- Results should be interpreted by qualified dentists
- Does not provide medical advice or treatment recommendations
- Always consult licensed dental professionals for patient care

### Data Privacy
- Patient data stored locally in SQLite database
- No external data transmission
- Secure file handling for uploaded images
- GDPR-compliant data handling practices

## 🚀 Deployment

### Local Development
```bash
python app.py
```
Access at: `http://localhost:5000`

### Production Deployment
For production deployment, consider:
1. **WSGI Server**: Use Gunicorn or uWSGI
2. **Reverse Proxy**: Configure Nginx or Apache
3. **HTTPS**: Implement SSL/TLS certificates
4. **Database**: Consider PostgreSQL for production
5. **File Storage**: Use cloud storage for uploaded images

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔒 Security Considerations

- File upload validation and size limits
- Secure filename handling
- SQL injection protection via parameterized queries
- XSS prevention through template escaping
- CSRF protection for forms

## 🧪 Testing

### Manual Testing Workflow
1. **Homepage**: Verify animations and navigation
2. **Patient Form**: Test validation and ID generation
3. **Upload System**: Test drag-drop and file validation
4. **Analysis**: Verify simulated AI processing
5. **Results**: Check confidence meters and recommendations
6. **History**: Test search and filtering functionality

### Browser Compatibility
Tested on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🛠️ Development

### Adding New Features
1. **Frontend**: Update HTML templates and CSS
2. **Backend**: Modify Flask routes in `app.py`
3. **Database**: Update schema in `database.py`
4. **Styling**: Enhance CSS with dental theme

### Code Style
- Follow PEP 8 for Python code
- Use semantic HTML5 elements
- Maintain dental color palette consistency
- Add professional animations sparingly

## 📱 Mobile Responsiveness

The application is fully responsive with:
- Mobile-first CSS Grid layouts
- Touch-friendly interface elements
- Adaptive typography and spacing
- Optimized animations for mobile devices

## 🔮 Future Enhancements

### Planned Features
- [ ] Real AI model integration (TensorFlow/PyTorch)
- [ ] PDF report generation
- [ ] Advanced patient search filters
- [ ] Data export to CSV/Excel
- [ ] Multi-language support
- [ ] Dark theme option
- [ ] Advanced analytics dashboard
- [ ] Integration with dental practice management systems

### Technical Improvements
- [ ] Add comprehensive test suite
- [ ] Implement caching for better performance
- [ ] Add API endpoints for mobile app integration
- [ ] Enhanced security features
- [ ] Automated backup system

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines
- Follow existing code style and conventions
- Maintain dental professional theme
- Test thoroughly before submitting
- Update documentation as needed
- Ensure mobile responsiveness

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dental professionals for guidance on clinical requirements
- Flask community for excellent documentation
- CSS animation inspiration from medical interface designs
- SQLite for reliable local database capabilities

## 📞 Support

For questions, issues, or suggestions:

- **GitHub Issues**: Create an issue for bug reports or feature requests
- **Documentation**: Check this README for detailed information
- **Medical Questions**: Consult qualified dental professionals

---

**⚕️ Medical Disclaimer**: DenTech AI is intended for decision support only. Always consult qualified dental professionals for diagnosis and treatment decisions.

**Made with 🦷 for dental professionals worldwide**