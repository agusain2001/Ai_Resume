import re
from collections import Counter

class ATSScorer:
    """Calculate ATS (Applicant Tracking System) score for resumes"""
    
    def __init__(self):
        # Common ATS-friendly keywords by category
        self.technical_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
            'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'aws', 'azure',
            'docker', 'kubernetes', 'git', 'ci/cd', 'agile', 'scrum', 'devops',
            'machine learning', 'ai', 'data science', 'analytics', 'api', 'rest',
            'microservices', 'cloud', 'linux', 'windows', 'ios', 'android'
        ]
        
        self.action_verbs = [
            'achieved', 'improved', 'developed', 'created', 'designed', 'built',
            'implemented', 'managed', 'led', 'increased', 'decreased', 'reduced',
            'optimized', 'enhanced', 'streamlined', 'automated', 'delivered',
            'launched', 'established', 'collaborated', 'coordinated', 'facilitated'
        ]
        
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem-solving',
            'analytical', 'creative', 'adaptable', 'detail-oriented',
            'time management', 'critical thinking', 'collaboration'
        ]
    
    def calculate_score(self, resume_data):
        """Calculate overall ATS score and provide feedback"""
        
        scores = {
            'format_structure': self._score_format_structure(resume_data),
            'keyword_optimization': self._score_keywords(resume_data),
            'content_quality': self._score_content_quality(resume_data),
            'completeness': self._score_completeness(resume_data),
            'quantifiable_results': self._score_quantifiable_results(resume_data)
        }
        
        # Weighted average
        weights = {
            'format_structure': 0.20,
            'keyword_optimization': 0.25,
            'content_quality': 0.20,
            'completeness': 0.20,
            'quantifiable_results': 0.15
        }
        
        total_score = sum(scores[key] * weights[key] for key in scores)
        
        # Generate feedback
        feedback = self._generate_feedback(scores, resume_data)
        
        return round(total_score), feedback
    
    def _score_format_structure(self, resume_data):
        """Score based on format and structure (0-100)"""
        score = 0
        
        # Check if has personal info
        personal_info = resume_data.get('personal_info', {})
        if personal_info.get('name'):
            score += 20
        if personal_info.get('email'):
            score += 20
        if personal_info.get('phone'):
            score += 20
        
        # Check for professional links
        if personal_info.get('linkedin') or personal_info.get('github'):
            score += 20
        
        # Check section presence
        if resume_data.get('summary'):
            score += 10
        if resume_data.get('education'):
            score += 5
        if resume_data.get('experience'):
            score += 5
        
        return min(score, 100)
    
    def _score_keywords(self, resume_data):
        """Score based on keyword optimization (0-100)"""
        
        # Combine all text
        all_text = self._get_all_text(resume_data).lower()
        
        # Count technical keywords
        tech_count = sum(1 for keyword in self.technical_keywords if keyword in all_text)
        tech_score = min((tech_count / 10) * 100, 100)  # 10+ keywords = 100%
        
        # Count action verbs
        action_count = sum(1 for verb in self.action_verbs if verb in all_text)
        action_score = min((action_count / 8) * 100, 100)  # 8+ verbs = 100%
        
        # Count soft skills
        soft_count = sum(1 for skill in self.soft_skills if skill in all_text)
        soft_score = min((soft_count / 5) * 100, 100)  # 5+ skills = 100%
        
        # Average of all keyword scores
        return (tech_score * 0.5 + action_score * 0.3 + soft_score * 0.2)
    
    def _score_content_quality(self, resume_data):
        """Score based on content quality (0-100)"""
        score = 0
        
        # Check summary quality
        summary = resume_data.get('summary', '')
        if summary:
            words = len(summary.split())
            if 30 <= words <= 100:  # Ideal summary length
                score += 25
            elif words > 0:
                score += 15
        
        # Check experience descriptions
        experiences = resume_data.get('experience', [])
        if experiences:
            total_length = 0
            for exp in experiences:
                resp = exp.get('responsibilities', '')
                total_length += len(resp.split())
            
            if total_length > 100:  # Detailed experience
                score += 30
            elif total_length > 50:
                score += 20
            elif total_length > 0:
                score += 10
        
        # Check for projects
        projects = resume_data.get('projects', [])
        if projects and any(p.get('description') for p in projects):
            score += 25
        
        # Check skills organization
        skills = resume_data.get('skills', {})
        if isinstance(skills, dict):
            if skills.get('technical') and skills.get('soft'):
                score += 20
            elif skills.get('technical') or skills.get('soft'):
                score += 10
        
        return min(score, 100)
    
    def _score_completeness(self, resume_data):
        """Score based on completeness (0-100)"""
        score = 0
        
        # Required sections
        if resume_data.get('personal_info', {}).get('name'):
            score += 20
        
        if resume_data.get('summary'):
            score += 15
        
        if resume_data.get('education') and len(resume_data['education']) > 0:
            score += 20
        
        if resume_data.get('experience') and len(resume_data['experience']) > 0:
            score += 25
        
        if resume_data.get('skills'):
            score += 20
        
        return min(score, 100)
    
    def _score_quantifiable_results(self, resume_data):
        """Score based on quantifiable achievements (0-100)"""
        
        all_text = self._get_all_text(resume_data)
        
        # Look for numbers and percentages
        numbers = re.findall(r'\d+%', all_text)
        numbers += re.findall(r'\$\d+', all_text)
        numbers += re.findall(r'\d+\+', all_text)
        
        # Look for quantifiable achievements
        achievement_patterns = [
            r'increased.*\d+',
            r'decreased.*\d+',
            r'improved.*\d+',
            r'reduced.*\d+',
            r'saved.*\d+',
            r'generated.*\d+',
            r'\d+.*users',
            r'\d+.*customers',
            r'\d+.*projects'
        ]
        
        achievements = 0
        for pattern in achievement_patterns:
            achievements += len(re.findall(pattern, all_text.lower()))
        
        # Score based on quantifiable metrics
        total_metrics = len(numbers) + achievements
        
        if total_metrics >= 10:
            return 100
        elif total_metrics >= 7:
            return 85
        elif total_metrics >= 5:
            return 70
        elif total_metrics >= 3:
            return 50
        elif total_metrics >= 1:
            return 30
        else:
            return 0
    
    def _get_all_text(self, resume_data):
        """Get all text from resume data"""
        text_parts = []
        
        # Personal info
        personal = resume_data.get('personal_info', {})
        text_parts.extend([str(v) for v in personal.values() if v])
        
        # Summary
        if resume_data.get('summary'):
            text_parts.append(resume_data['summary'])
        
        # Education
        for edu in resume_data.get('education', []):
            text_parts.extend([str(v) for v in edu.values() if v])
        
        # Experience
        for exp in resume_data.get('experience', []):
            text_parts.extend([str(v) for v in exp.values() if v])
        
        # Skills
        skills = resume_data.get('skills', {})
        if isinstance(skills, dict):
            text_parts.extend([str(v) for v in skills.values() if v])
        elif isinstance(skills, str):
            text_parts.append(skills)
        
        # Projects
        for proj in resume_data.get('projects', []):
            text_parts.extend([str(v) for v in proj.values() if v])
        
        return ' '.join(text_parts)
    
    def _generate_feedback(self, scores, resume_data):
        """Generate detailed feedback based on scores"""
        feedback = []
        
        # Format & Structure feedback
        if scores['format_structure'] < 70:
            feedback.append("⚠️ Consider adding more contact information (email, phone, LinkedIn)")
        
        # Keyword feedback
        if scores['keyword_optimization'] < 70:
            feedback.append("📝 Add more relevant technical keywords and action verbs to improve ATS visibility")
            feedback.append("💡 Use strong action verbs like 'achieved', 'implemented', 'led', 'optimized'")
        
        # Content quality feedback
        if scores['content_quality'] < 70:
            feedback.append("✍️ Expand your experience descriptions with more details and context")
            feedback.append("🎯 Consider adding a professional summary (30-100 words)")
        
        # Completeness feedback
        if scores['completeness'] < 80:
            missing_sections = []
            if not resume_data.get('summary'):
                missing_sections.append("Professional Summary")
            if not resume_data.get('projects'):
                missing_sections.append("Projects")
            if missing_sections:
                feedback.append(f"📋 Consider adding: {', '.join(missing_sections)}")
        
        # Quantifiable results feedback
        if scores['quantifiable_results'] < 60:
            feedback.append("📊 Add more quantifiable achievements (e.g., 'Increased efficiency by 30%', 'Managed team of 5')")
            feedback.append("💯 Use numbers, percentages, and metrics to demonstrate impact")
        
        # Positive feedback
        if all(score >= 70 for score in scores.values()):
            feedback.append("✨ Great job! Your resume is well-structured and ATS-friendly")
        
        if scores['quantifiable_results'] >= 80:
            feedback.append("🎉 Excellent use of quantifiable achievements!")
        
        return feedback if feedback else ["✅ Your resume looks great!"]