# 🤖 AI-Powered Resume Builder & ATS Optimization Agent

A complete AI-powered resume builder application that helps users create ATS-optimized resumes with professional formatting and enhanced readability using Google Gemini API.

## 🌟 Features

- **📤 Dual Input Methods**: Upload existing resume (PDF/DOCX) or enter details manually
- **📊 ATS Scoring**: Real-time Applicant Tracking System score calculation
- **🤖 AI Enhancement**: Powered by Google Gemini for intelligent content optimization
- **🎨 Professional Templates**: 3 LaTeX-based templates (Professional, Modern, Classic)
- **📥 Multi-Format Export**: Download resumes in both Word (.docx) and PDF formats
- **📈 Score Tracking**: Visual comparison of before/after ATS scores
- **💬 AI Feedback Chat**: Interactive suggestions for resume improvement
- **🔄 Live Preview**: Real-time updates as content is enhanced

## 📁 Project Structure

```
resume-builder/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # Project documentation
│
├── utils/
│   ├── __init__.py
│   ├── parser.py                   # Resume parsing utilities
│   ├── ats_scorer.py               # ATS scoring logic
│   ├── ai_enhancer.py              # AI enhancement using Gemini
│   ├── template_manager.py         # LaTeX template handler
│   └── resume_generator.py         # Word/PDF generation
│
├── templates/
│   ├── template1.tex               # Professional template
│   ├── template2.tex               # Modern template
│   └── template3.tex               # Classic template
│
└── output/                         # Generated resumes
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- (Optional) LaTeX distribution for PDF generation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd resume-builder
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

### Step 5: Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

## 🎯 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Step-by-Step Guide

1. **Choose Input Method**
   - Upload an existing resume (PDF or DOCX)
   - OR Enter details manually

2. **Calculate ATS Score**
   - Click "Calculate ATS Score" to get your initial score
   - Review detailed feedback

3. **Enhance with AI**
   - Click "Enhance with AI" to improve your resume
   - View before/after comparison

4. **Select Template**
   - Choose from Professional, Modern, or Classic templates

5. **Download Resume**
   - Download in Word (.docx) format
   - Download in PDF format

## 📊 ATS Scoring Criteria

The ATS scorer evaluates resumes based on:

- **Format & Structure (20%)**: Contact information, section organization
- **Keyword Optimization (25%)**: Technical keywords, action verbs, soft skills
- **Content Quality (20%)**: Summary quality, experience descriptions, projects
- **Completeness (20%)**: All required sections present
- **Quantifiable Results (15%)**: Numbers, percentages, metrics

## 🤖 AI Enhancement Features

Google Gemini AI enhances:

1. **Professional Summary**: More impactful and keyword-rich
2. **Work Experience**: Action-oriented bullet points with quantifiable results
3. **Projects**: Technical focus with measurable impact
4. **Skills**: Organized categorization

## 🎨 Available Templates

### Template 1: Professional
- Clean and traditional design
- ATS-optimized format
- Suitable for corporate positions

### Template 2: Modern
- Contemporary design with color accents
- Eye-catching while ATS-friendly
- Great for tech and creative roles

### Template 3: Classic
- Timeless and elegant
- Minimalist approach
- Universal compatibility

## 📦 Dependencies

```txt
streamlit==1.31.0
google-generativeai==0.3.2
python-dotenv==1.0.0
PyPDF2==3.0.1
python-docx==1.1.0
pylatex==1.4.2
pandas==2.1.4
plotly==5.18.0
requests==2.31.0
beautifulsoup4==4.12.2
```

## 🔧 Configuration

### Environment Variables

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Optional: LaTeX Installation

For high-quality PDF generation:

**Windows:**
```bash
# Install MiKTeX from https://miktex.org/download
```

**macOS:**
```bash
brew install mactex
```

**Linux:**
```bash
sudo apt-get install texlive-full
```

## 📝 Manual Entry Fields

When entering details manually, include:

- **Personal Information**: Name, Email, Phone, LinkedIn, GitHub, Portfolio
- **Professional Summary**: 2-3 sentence overview
- **Education**: Degree, Institution, Graduation Date, GPA
- **Work Experience**: Title, Company, Dates, Responsibilities
- **Skills**: Technical and Soft Skills
- **Projects**: Name, Description, Technologies

## 🎯 Best Practices

1. **Use Action Verbs**: Start bullet points with strong verbs (achieved, developed, led)
2. **Quantify Achievements**: Include numbers and percentages
3. **Keywords**: Include relevant industry keywords
4. **Consistency**: Use consistent formatting throughout
5. **Conciseness**: Keep descriptions clear and concise
6. **Proofreading**: Always review for errors

## 🚀 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your repository
4. Add `GEMINI_API_KEY` in Secrets
5. Deploy!

### Render

1. Create `render.yaml`:
   ```yaml
   services:
     - type: web
       name: resume-builder
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run app.py
   ```

2. Deploy on [Render](https://render.com)

### Vercel

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Deploy:
   ```bash
   vercel
   ```

## 🐛 Troubleshooting

### Common Issues

**Issue**: "GEMINI_API_KEY not found"
- **Solution**: Ensure `.env` file exists with valid API key

**Issue**: PDF generation fails
- **Solution**: Install LaTeX distribution or use DOCX format

**Issue**: Parsing errors
- **Solution**: Ensure resume follows standard format

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Gemini AI for content enhancement
- Streamlit for the web framework
- LaTeX community for resume templates

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Email: support@example.com

## 🔄 Updates

### Version 1.0.0 (Current)
- Initial release
- Basic ATS scoring
- AI enhancement with Gemini
- 3 professional templates
- Word and PDF export

### Planned Features
- More templates
- Job description matching
- Multi-language support
- Cover letter generation
- LinkedIn profile optimization

---

Made with ❤️ using Streamlit and Google Gemini AI