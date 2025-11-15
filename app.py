import streamlit as st
import os
from dotenv import load_dotenv
import json
from utils.parser import ResumeParser
from utils.ats_scorer import ATSScorer
from utils.ai_enhancer import AIEnhancer
from utils.template_manager import TemplateManager
from utils.resume_generator import ResumeGenerator
import plotly.graph_objects as go

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Resume Builder & ATS Optimizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'original_score' not in st.session_state:
    st.session_state.original_score = None
if 'enhanced_data' not in st.session_state:
    st.session_state.enhanced_data = None
if 'enhanced_score' not in st.session_state:
    st.session_state.enhanced_score = None
if 'score_calculated' not in st.session_state:
    st.session_state.score_calculated = False
if 'data_saved' not in st.session_state:
    st.session_state.data_saved = False
if 'enhancing' not in st.session_state:
    st.session_state.enhancing = False

def main():
    st.markdown('<h1 class="main-header">🤖 AI Resume Builder & ATS Optimizer</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/resume.png", width=100)
        st.title("Navigation")
        page = st.radio("Go to", ["Home", "Create Resume", "Dashboard", "Help"])
        
        st.markdown("---")
        st.info("💡 **Tip**: Upload your resume or enter details manually to get started!")
    
    if page == "Home":
        show_home()
    elif page == "Create Resume":
        show_create_resume()
    elif page == "Dashboard":
        show_dashboard()
    else:
        show_help()

def show_home():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Welcome to AI Resume Builder!")
        st.markdown("""
        Create ATS-optimized resumes with AI-powered enhancements in minutes.
        
        **Features:**
        - 📊 Real-time ATS Scoring
        - 🤖 AI-Enhanced Content (Google Gemini)
        - 📝 Professional LaTeX Templates
        - 📥 Export to Word & PDF
        - 📈 Score Improvement Tracking
        - 💬 AI Feedback Chat
        """)
        
        st.markdown("### How It Works")
        st.markdown("""
        1. **Upload** your existing resume or **Enter** details manually
        2. **Get** your initial ATS score
        3. **Enhance** with AI-powered optimization
        4. **Choose** from professional templates
        5. **Download** your optimized resume
        """)
        
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state.page = "Create Resume"
            st.rerun()

def show_create_resume():
    st.markdown("### 📝 Create Your Resume")
    
    # Input method selection
    input_method = st.radio(
        "Choose Input Method:",
        ["Upload Existing Resume", "Enter Details Manually"],
        horizontal=True
    )
    
    if input_method == "Upload Existing Resume":
        handle_file_upload()
    else:
        handle_manual_entry()

def handle_file_upload():
    st.markdown("#### Upload Your Resume")
    
    uploaded_file = st.file_uploader(
        "Choose a file (PDF or Word)",
        type=['pdf', 'docx'],
        help="Upload your existing resume for analysis and enhancement"
    )
    
    if uploaded_file:
        with st.spinner("🔍 Parsing your resume..."):
            try:
                parser = ResumeParser()
                resume_data = parser.parse_file(uploaded_file)
                st.session_state.resume_data = resume_data
                
                st.success("✅ Resume parsed successfully!")
                
                # Display parsed data
                with st.expander("📋 View Extracted Information"):
                    st.json(resume_data)
                
                # Calculate initial ATS score
                if st.button("📊 Calculate ATS Score", key="calc_score_upload"):
                    calculate_ats_score(resume_data)
                
                # Show enhancement button if score is calculated
                if st.session_state.get('score_calculated'):
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button("🚀 Enhance with AI", use_container_width=True, key="enhance_upload"):
                            st.session_state.enhancing = True
                            st.rerun()
                
                # Show enhancement results if available
                if st.session_state.get('enhancing') or st.session_state.get('enhanced_data'):
                    if not st.session_state.get('enhanced_data'):
                        enhance_resume(resume_data)
                    else:
                        show_comparison()
                    
            except Exception as e:
                st.error(f"❌ Error parsing resume: {str(e)}")

def handle_manual_entry():
    st.markdown("#### Enter Your Details")
    
    with st.form("manual_entry_form"):
        st.markdown("##### Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name*", placeholder="John Doe")
            email = st.text_input("Email*", placeholder="john.doe@email.com")
            phone = st.text_input("Phone*", placeholder="+1 234 567 8900")
        with col2:
            linkedin = st.text_input("LinkedIn", placeholder="linkedin.com/in/johndoe")
            github = st.text_input("GitHub", placeholder="github.com/johndoe")
            portfolio = st.text_input("Portfolio/Website", placeholder="johndoe.com")
        
        st.markdown("##### Professional Summary")
        summary = st.text_area(
            "Summary*",
            placeholder="Write a brief professional summary (2-3 sentences)",
            height=100
        )
        
        st.markdown("##### Education")
        num_education = st.number_input("Number of Education Entries", min_value=1, max_value=5, value=1)
        education = []
        for i in range(num_education):
            with st.expander(f"Education {i+1}"):
                col1, col2 = st.columns(2)
                with col1:
                    degree = st.text_input(f"Degree*", key=f"degree_{i}", placeholder="B.S. Computer Science")
                    institution = st.text_input(f"Institution*", key=f"inst_{i}", placeholder="University Name")
                with col2:
                    graduation = st.text_input(f"Graduation Date*", key=f"grad_{i}", placeholder="May 2023")
                    gpa = st.text_input(f"GPA", key=f"gpa_{i}", placeholder="3.8/4.0")
                education.append({
                    "degree": degree,
                    "institution": institution,
                    "graduation_date": graduation,
                    "gpa": gpa
                })
        
        st.markdown("##### Work Experience")
        num_experience = st.number_input("Number of Work Experiences", min_value=0, max_value=10, value=2)
        experience = []
        for i in range(num_experience):
            with st.expander(f"Experience {i+1}"):
                col1, col2 = st.columns(2)
                with col1:
                    job_title = st.text_input(f"Job Title*", key=f"job_{i}", placeholder="Software Engineer")
                    company = st.text_input(f"Company*", key=f"company_{i}", placeholder="Tech Corp")
                with col2:
                    start_date = st.text_input(f"Start Date*", key=f"start_{i}", placeholder="Jan 2022")
                    end_date = st.text_input(f"End Date*", key=f"end_{i}", placeholder="Present")
                
                responsibilities = st.text_area(
                    f"Responsibilities & Achievements*",
                    key=f"resp_{i}",
                    placeholder="• Developed web applications using React\n• Improved system performance by 30%",
                    height=100
                )
                experience.append({
                    "title": job_title,
                    "company": company,
                    "start_date": start_date,
                    "end_date": end_date,
                    "responsibilities": responsibilities
                })
        
        st.markdown("##### Skills")
        col1, col2 = st.columns(2)
        with col1:
            technical_skills = st.text_area(
                "Technical Skills*",
                placeholder="Python, Java, React, SQL, AWS",
                height=80
            )
        with col2:
            soft_skills = st.text_area(
                "Soft Skills",
                placeholder="Leadership, Communication, Problem-solving",
                height=80
            )
        
        st.markdown("##### Projects")
        num_projects = st.number_input("Number of Projects", min_value=0, max_value=10, value=2)
        projects = []
        for i in range(num_projects):
            with st.expander(f"Project {i+1}"):
                project_name = st.text_input(f"Project Name*", key=f"proj_name_{i}")
                project_desc = st.text_area(
                    f"Description*",
                    key=f"proj_desc_{i}",
                    placeholder="Brief description of the project and your role",
                    height=80
                )
                project_tech = st.text_input(f"Technologies Used", key=f"proj_tech_{i}")
                projects.append({
                    "name": project_name,
                    "description": project_desc,
                    "technologies": project_tech
                })
        
        submitted = st.form_submit_button("💾 Save & Continue", use_container_width=True)
        
        if submitted:
            resume_data = {
                "personal_info": {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "linkedin": linkedin,
                    "github": github,
                    "portfolio": portfolio
                },
                "summary": summary,
                "education": education,
                "experience": experience,
                "skills": {
                    "technical": technical_skills,
                    "soft": soft_skills
                },
                "projects": projects
            }
            
            if name and email and phone and summary:
                st.session_state.resume_data = resume_data
                st.session_state.data_saved = True
                st.success("✅ Resume data saved successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill all required fields marked with *")
    
    # Show score calculation button if data is saved
    if st.session_state.get('data_saved') and st.session_state.get('resume_data'):
        st.markdown("---")
        if st.button("📊 Calculate ATS Score", key="calc_score_manual"):
            calculate_ats_score(st.session_state.resume_data)
        
        # Show enhancement button if score is calculated
        if st.session_state.get('score_calculated'):
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Enhance with AI", use_container_width=True, key="enhance_manual"):
                    st.session_state.enhancing = True
                    st.rerun()
        
        # Show enhancement results if available
        if st.session_state.get('enhancing') or st.session_state.get('enhanced_data'):
            if not st.session_state.get('enhanced_data'):
                enhance_resume(st.session_state.resume_data)
            else:
                show_comparison()

def calculate_ats_score(resume_data):
    with st.spinner("🔍 Calculating ATS Score..."):
        try:
            scorer = ATSScorer()
            score, feedback = scorer.calculate_score(resume_data)
            st.session_state.original_score = score
            st.session_state.score_calculated = True
            
            # Display score
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f"""
                <div class="score-card">
                    <h2>Original ATS Score</h2>
                    <h1 style="font-size: 4rem; margin: 0;">{score}%</h1>
                    <p>{'Excellent' if score >= 80 else 'Good' if score >= 60 else 'Needs Improvement'}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Display feedback
            with st.expander("📝 Detailed Feedback"):
                for item in feedback:
                    st.markdown(f"- {item}")
                    
        except Exception as e:
            st.error(f"❌ Error calculating score: {str(e)}")

def enhance_resume(resume_data):
    with st.spinner("🤖 Enhancing your resume with AI... This may take 10-15 seconds..."):
        try:
            enhancer = AIEnhancer()
            enhanced_data = enhancer.enhance_resume(resume_data)
            st.session_state.enhanced_data = enhanced_data
            st.session_state.enhancing = False
            
            # Calculate enhanced score
            scorer = ATSScorer()
            enhanced_score, _ = scorer.calculate_score(enhanced_data)
            st.session_state.enhanced_score = enhanced_score
            
            st.success("✅ Resume enhanced successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error enhancing resume: {str(e)}")
            st.error("Please check your API key and internet connection.")
            st.session_state.enhancing = False

def show_comparison():
    st.markdown("### 📊 Before & After Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Original")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; color: white; text-align: center;">
            <h1 style="font-size: 3rem; margin: 0;">{st.session_state.original_score}%</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Enhanced")
        improvement = st.session_state.enhanced_score - st.session_state.original_score
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                    padding: 2rem; border-radius: 10px; color: white; text-align: center;">
            <h1 style="font-size: 3rem; margin: 0;">{st.session_state.enhanced_score}%</h1>
            <p style="font-size: 1.2rem;">+{improvement}% Improvement</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Side by side content comparison
    st.markdown("### 📝 Content Comparison")
    
    tab1, tab2 = st.tabs(["Original Resume", "Enhanced Resume"])
    
    with tab1:
        st.json(st.session_state.resume_data)
    
    with tab2:
        st.json(st.session_state.enhanced_data)
    
    # Template selection
    st.markdown("---")
    st.markdown("### 🎨 Choose a Template")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://img.icons8.com/color/96/resume.png", width=80)
        st.markdown("**Professional**")
        if st.button("Select Template 1", key="template1"):
            generate_final_resume("template1")
    
    with col2:
        st.image("https://img.icons8.com/color/96/cv.png", width=80)
        st.markdown("**Modern**")
        if st.button("Select Template 2", key="template2"):
            generate_final_resume("template2")
    
    with col3:
        st.image("https://img.icons8.com/color/96/document.png", width=80)
        st.markdown("**Classic**")
        if st.button("Select Template 3", key="template3"):
            generate_final_resume("template3")

def generate_final_resume(template_name):
    with st.spinner("📄 Generating your resume..."):
        try:
            generator = ResumeGenerator()
            docx_file, pdf_file = generator.generate(
                st.session_state.enhanced_data,
                template_name
            )
            
            st.success("✅ Resume generated successfully!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                with open(docx_file, 'rb') as f:
                    st.download_button(
                        label="📥 Download Word (.docx)",
                        data=f,
                        file_name="resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
            
            with col2:
                with open(pdf_file, 'rb') as f:
                    st.download_button(
                        label="📥 Download PDF",
                        data=f,
                        file_name="resume.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Error generating resume: {str(e)}")

def show_dashboard():
    st.markdown("### 📊 Dashboard")
    
    if st.session_state.original_score and st.session_state.enhanced_score:
        # Score improvement chart
        fig = go.Figure(data=[
            go.Bar(name='Original', x=['ATS Score'], y=[st.session_state.original_score], marker_color='#667eea'),
            go.Bar(name='Enhanced', x=['ATS Score'], y=[st.session_state.enhanced_score], marker_color='#38ef7d')
        ])
        
        fig.update_layout(
            title='ATS Score Improvement',
            yaxis_title='Score (%)',
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Original Score", f"{st.session_state.original_score}%")
        with col2:
            st.metric("Enhanced Score", f"{st.session_state.enhanced_score}%")
        with col3:
            improvement = st.session_state.enhanced_score - st.session_state.original_score
            st.metric("Improvement", f"+{improvement}%", delta=f"{improvement}%")
    else:
        st.info("📝 Create a resume first to see your dashboard statistics!")

def show_help():
    st.markdown("### ❓ Help & FAQ")
    
    with st.expander("What is ATS?"):
        st.markdown("""
        **Applicant Tracking System (ATS)** is software used by companies to filter resumes.
        An ATS-optimized resume increases your chances of getting past the initial screening.
        """)
    
    with st.expander("How does AI enhancement work?"):
        st.markdown("""
        Our AI (powered by Google Gemini) analyzes your resume and:
        - Improves grammar and phrasing
        - Optimizes keywords for ATS
        - Enhances professional tone
        - Suggests better ways to present achievements
        """)
    
    with st.expander("What file formats are supported?"):
        st.markdown("""
        - **Input**: PDF, DOCX
        - **Output**: PDF, DOCX
        """)
    
    with st.expander("How is the ATS score calculated?"):
        st.markdown("""
        The score is based on multiple factors:
        - Keyword density and relevance
        - Format and structure
        - Content completeness
        - Professional language
        - Quantifiable achievements
        """)

if __name__ == "__main__":
    main()