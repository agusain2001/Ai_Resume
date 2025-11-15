import PyPDF2
from docx import Document
import re
import json

class ResumeParser:
    """Parse resumes from PDF and DOCX files"""
    
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        self.url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    
    def parse_file(self, uploaded_file):
        """Main method to parse uploaded file"""
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        if file_type == 'pdf':
            text = self._extract_pdf_text(uploaded_file)
        elif file_type in ['docx', 'doc']:
            text = self._extract_docx_text(uploaded_file)
        else:
            raise ValueError("Unsupported file format")
        
        return self._parse_text(text)
    
    def _extract_pdf_text(self, file):
        """Extract text from PDF"""
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def _extract_docx_text(self, file):
        """Extract text from DOCX"""
        doc = Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    
    def _parse_text(self, text):
        """Parse text and extract structured information"""
        
        # Extract personal information
        personal_info = self._extract_personal_info(text)
        
        # Extract sections
        sections = self._split_into_sections(text)
        
        # Extract education
        education = self._extract_education(sections.get('education', ''))
        
        # Extract experience
        experience = self._extract_experience(sections.get('experience', ''))
        
        # Extract skills
        skills = self._extract_skills(sections.get('skills', ''))
        
        # Extract projects
        projects = self._extract_projects(sections.get('projects', ''))
        
        # Extract summary
        summary = self._extract_summary(sections.get('summary', ''))
        
        return {
            "personal_info": personal_info,
            "summary": summary,
            "education": education,
            "experience": experience,
            "skills": skills,
            "projects": projects,
            "raw_text": text
        }
    
    def _extract_personal_info(self, text):
        """Extract personal information"""
        info = {}
        
        # Extract email
        emails = re.findall(self.email_pattern, text)
        info['email'] = emails[0] if emails else ""
        
        # Extract phone
        phones = re.findall(self.phone_pattern, text)
        info['phone'] = phones[0] if phones else ""
        
        # Extract name (usually first line)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        info['name'] = lines[0] if lines else ""
        
        # Extract URLs (LinkedIn, GitHub, etc.)
        urls = re.findall(self.url_pattern, text)
        info['linkedin'] = next((url for url in urls if 'linkedin' in url.lower()), "")
        info['github'] = next((url for url in urls if 'github' in url.lower()), "")
        info['portfolio'] = next((url for url in urls if url not in [info['linkedin'], info['github']]), "")
        
        return info
    
    def _split_into_sections(self, text):
        """Split text into sections based on headers"""
        sections = {}
        
        # Common section headers
        section_keywords = {
            'summary': ['summary', 'profile', 'objective', 'about'],
            'education': ['education', 'academic', 'qualification'],
            'experience': ['experience', 'employment', 'work history', 'professional experience'],
            'skills': ['skills', 'technical skills', 'competencies'],
            'projects': ['projects', 'portfolio'],
            'certifications': ['certifications', 'certificates', 'licenses']
        }
        
        lines = text.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line is a section header
            is_header = False
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    # Save previous section
                    if current_section and section_content:
                        sections[current_section] = '\n'.join(section_content)
                    
                    current_section = section
                    section_content = []
                    is_header = True
                    break
            
            if not is_header and current_section:
                section_content.append(line)
        
        # Save last section
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content)
        
        return sections
    
    def _extract_summary(self, text):
        """Extract professional summary"""
        if not text:
            return ""
        
        # Clean and return first few sentences
        sentences = text.strip().split('.')
        return '. '.join(sentences[:3]).strip() + '.'
    
    def _extract_education(self, text):
        """Extract education details"""
        education = []
        
        if not text:
            return education
        
        # Common degree patterns
        degree_patterns = [
            r'(Bachelor|Master|Ph\.?D|B\.?S\.?|M\.?S\.?|B\.?A\.?|M\.?A\.?).*',
            r'(B\.Tech|M\.Tech|B\.E\.|M\.E\.)',
        ]
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        current_entry = {}
        for line in lines:
            # Check for degree
            for pattern in degree_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    if current_entry:
                        education.append(current_entry)
                    current_entry = {'degree': line, 'institution': '', 'graduation_date': '', 'gpa': ''}
                    break
            
            # Check for year (graduation date)
            year_match = re.search(r'(19|20)\d{2}', line)
            if year_match and current_entry:
                current_entry['graduation_date'] = year_match.group()
            
            # Check for GPA
            gpa_match = re.search(r'(\d\.\d+)\s*/?(\d\.\d+)?', line)
            if gpa_match and current_entry and not current_entry.get('gpa'):
                current_entry['gpa'] = gpa_match.group()
            
            # Institution name (if not degree and no year)
            if current_entry and not re.search(r'(19|20)\d{2}', line) and line not in current_entry.get('degree', ''):
                if not current_entry.get('institution'):
                    current_entry['institution'] = line
        
        if current_entry:
            education.append(current_entry)
        
        return education if education else [{'degree': '', 'institution': '', 'graduation_date': '', 'gpa': ''}]
    
    def _extract_experience(self, text):
        """Extract work experience"""
        experience = []
        
        if not text:
            return experience
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        current_entry = {}
        for line in lines:
            # Check for dates (indicates new entry)
            date_pattern = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}'
            
            if re.search(date_pattern, line, re.IGNORECASE):
                if current_entry:
                    experience.append(current_entry)
                
                # Parse dates
                dates = re.findall(date_pattern, line, re.IGNORECASE)
                current_entry = {
                    'title': '',
                    'company': '',
                    'start_date': dates[0] if dates else '',
                    'end_date': dates[1] if len(dates) > 1 else 'Present',
                    'responsibilities': []
                }
            elif current_entry:
                # Check if it's a bullet point or responsibility
                if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                    current_entry['responsibilities'].append(line)
                elif not current_entry.get('title'):
                    current_entry['title'] = line
                elif not current_entry.get('company'):
                    current_entry['company'] = line
                else:
                    current_entry['responsibilities'].append(line)
        
        if current_entry:
            experience.append(current_entry)
        
        # Format responsibilities as text
        for exp in experience:
            exp['responsibilities'] = '\n'.join(exp['responsibilities'])
        
        return experience if experience else [{'title': '', 'company': '', 'start_date': '', 'end_date': '', 'responsibilities': ''}]
    
    def _extract_skills(self, text):
        """Extract skills"""
        if not text:
            return {'technical': '', 'soft': ''}
        
        # Simple extraction - separate by common delimiters
        skills_list = []
        for line in text.split('\n'):
            line = line.strip()
            if line and not any(header in line.lower() for header in ['skills', 'technical', 'soft']):
                # Remove bullet points
                line = re.sub(r'^[•\-\*]\s*', '', line)
                skills_list.append(line)
        
        all_skills = ', '.join(skills_list)
        
        # Try to categorize (simple heuristic)
        technical_keywords = ['python', 'java', 'javascript', 'react', 'sql', 'aws', 'docker', 'git']
        technical = []
        soft = []
        
        for skill in skills_list:
            if any(keyword in skill.lower() for keyword in technical_keywords):
                technical.append(skill)
            else:
                soft.append(skill)
        
        return {
            'technical': ', '.join(technical) if technical else all_skills,
            'soft': ', '.join(soft) if soft else ''
        }
    
    def _extract_projects(self, text):
        """Extract projects"""
        projects = []
        
        if not text:
            return projects
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        current_project = {}
        for line in lines:
            # New project indicator (usually bold or title-cased)
            if line.isupper() or (line[0].isupper() and not line.startswith(('•', '-', '*'))):
                if current_project:
                    projects.append(current_project)
                current_project = {'name': line, 'description': '', 'technologies': ''}
            elif current_project:
                if 'technologies' in line.lower() or 'tech stack' in line.lower():
                    current_project['technologies'] = line.split(':', 1)[-1].strip()
                else:
                    current_project['description'] += line + ' '
        
        if current_project:
            projects.append(current_project)
        
        return projects if projects else [{'name': '', 'description': '', 'technologies': ''}]