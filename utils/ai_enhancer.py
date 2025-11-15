import google.generativeai as genai
import os
import json
from typing import Dict, Any

class AIEnhancer:
    """Enhance resume content using Google Gemini API"""
    
    def __init__(self):
        api_key = "AIzaSyCCyG8AKeJc_QMOs-8hJtv1_zJ_dM1N1wI"
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def enhance_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to enhance all resume sections"""
        
        enhanced_data = resume_data.copy()
        
        # Enhance summary
        if resume_data.get('summary'):
            enhanced_data['summary'] = self._enhance_summary(resume_data['summary'])
        
        # Enhance experience
        if resume_data.get('experience'):
            enhanced_data['experience'] = self._enhance_experience(resume_data['experience'])
        
        # Enhance projects
        if resume_data.get('projects'):
            enhanced_data['projects'] = self._enhance_projects(resume_data['projects'])
        
        # Enhance skills description (if needed)
        if resume_data.get('skills'):
            enhanced_data['skills'] = self._enhance_skills(resume_data['skills'])
        
        return enhanced_data
    
    def _enhance_summary(self, summary: str) -> str:
        """Enhance professional summary"""
        
        prompt = f"""
        You are an expert resume writer. Enhance the following professional summary to make it more impactful, 
        ATS-friendly, and compelling. Keep it concise (2-3 sentences, 50-80 words).
        
        Focus on:
        - Strong action words
        - Relevant keywords
        - Clear value proposition
        - Professional tone
        - Quantifiable achievements if mentioned
        
        Original summary:
        {summary}
        
        Return ONLY the enhanced summary text, nothing else.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error enhancing summary: {e}")
            return summary
    
    def _enhance_experience(self, experiences: list) -> list:
        """Enhance work experience descriptions"""
        
        enhanced_experiences = []
        
        for exp in experiences:
            responsibilities = exp.get('responsibilities', '')
            
            if not responsibilities:
                enhanced_experiences.append(exp)
                continue
            
            prompt = f"""
            You are an expert resume writer. Enhance the following job responsibilities to make them more impactful and ATS-friendly.
            
            Job Title: {exp.get('title', 'N/A')}
            Company: {exp.get('company', 'N/A')}
            
            Original responsibilities:
            {responsibilities}
            
            Requirements:
            - Start each point with a strong action verb (achieved, developed, led, implemented, etc.)
            - Make achievements quantifiable where possible
            - Use industry-relevant keywords
            - Keep it concise and impactful
            - Format as bullet points (use • symbol)
            - Aim for 3-5 bullet points
            
            Return ONLY the enhanced bullet points, nothing else.
            """
            
            try:
                response = self.model.generate_content(prompt)
                enhanced_resp = response.text.strip()
                
                enhanced_exp = exp.copy()
                enhanced_exp['responsibilities'] = enhanced_resp
                enhanced_experiences.append(enhanced_exp)
            except Exception as e:
                print(f"Error enhancing experience: {e}")
                enhanced_experiences.append(exp)
        
        return enhanced_experiences
    
    def _enhance_projects(self, projects: list) -> list:
        """Enhance project descriptions"""
        
        enhanced_projects = []
        
        for proj in projects:
            description = proj.get('description', '')
            
            if not description:
                enhanced_projects.append(proj)
                continue
            
            prompt = f"""
            You are an expert resume writer. Enhance the following project description to make it more impressive and ATS-friendly.
            
            Project Name: {proj.get('name', 'N/A')}
            Technologies: {proj.get('technologies', 'N/A')}
            
            Original description:
            {description}
            
            Requirements:
            - Highlight technical skills and technologies used
            - Emphasize impact and results
            - Use action-oriented language
            - Keep it concise (2-3 sentences)
            - Include quantifiable metrics if possible
            
            Return ONLY the enhanced description, nothing else.
            """
            
            try:
                response = self.model.generate_content(prompt)
                enhanced_desc = response.text.strip()
                
                enhanced_proj = proj.copy()
                enhanced_proj['description'] = enhanced_desc
                enhanced_projects.append(enhanced_proj)
            except Exception as e:
                print(f"Error enhancing project: {e}")
                enhanced_projects.append(proj)
        
        return enhanced_projects
    
    def _enhance_skills(self, skills: Dict[str, str]) -> Dict[str, str]:
        """Organize and potentially expand skills"""
        
        if isinstance(skills, str):
            # If skills is just a string, try to categorize
            prompt = f"""
            Organize the following skills into two categories: Technical Skills and Soft Skills.
            
            Skills: {skills}
            
            Return in this exact JSON format:
            {{
                "technical": "comma-separated list of technical skills",
                "soft": "comma-separated list of soft skills"
            }}
            
            Return ONLY the JSON, nothing else.
            """
            
            try:
                response = self.model.generate_content(prompt)
                result = json.loads(response.text.strip())
                return result
            except Exception as e:
                print(f"Error enhancing skills: {e}")
                return {"technical": skills, "soft": ""}
        
        return skills
    
    def get_improvement_suggestions(self, resume_data: Dict[str, Any]) -> list:
        """Get AI-powered improvement suggestions"""
        
        # Convert resume data to readable format
        resume_text = self._format_resume_for_analysis(resume_data)
        
        prompt = f"""
        You are an expert resume reviewer and career coach. Analyze the following resume and provide 
        5 specific, actionable suggestions for improvement.
        
        Resume:
        {resume_text}
        
        Focus on:
        - ATS optimization
        - Content improvements
        - Keyword optimization
        - Quantifiable achievements
        - Professional presentation
        
        Return suggestions as a numbered list. Be specific and actionable.
        """
        
        try:
            response = self.model.generate_content(prompt)
            suggestions = response.text.strip().split('\n')
            return [s.strip() for s in suggestions if s.strip()]
        except Exception as e:
            print(f"Error getting suggestions: {e}")
            return ["Unable to generate suggestions at this time."]
    
    def _format_resume_for_analysis(self, resume_data: Dict[str, Any]) -> str:
        """Format resume data into readable text for analysis"""
        
        parts = []
        
        # Personal Info
        personal = resume_data.get('personal_info', {})
        if personal:
            parts.append(f"Name: {personal.get('name', 'N/A')}")
            parts.append(f"Email: {personal.get('email', 'N/A')}")
            parts.append(f"Phone: {personal.get('phone', 'N/A')}")
        
        # Summary
        if resume_data.get('summary'):
            parts.append(f"\nProfessional Summary:\n{resume_data['summary']}")
        
        # Education
        if resume_data.get('education'):
            parts.append("\nEducation:")
            for edu in resume_data['education']:
                parts.append(f"- {edu.get('degree', '')} from {edu.get('institution', '')}")
        
        # Experience
        if resume_data.get('experience'):
            parts.append("\nWork Experience:")
            for exp in resume_data['experience']:
                parts.append(f"\n{exp.get('title', '')} at {exp.get('company', '')}")
                parts.append(exp.get('responsibilities', ''))
        
        # Skills
        if resume_data.get('skills'):
            parts.append("\nSkills:")
            skills = resume_data['skills']
            if isinstance(skills, dict):
                if skills.get('technical'):
                    parts.append(f"Technical: {skills['technical']}")
                if skills.get('soft'):
                    parts.append(f"Soft: {skills['soft']}")
            else:
                parts.append(str(skills))
        
        # Projects
        if resume_data.get('projects'):
            parts.append("\nProjects:")
            for proj in resume_data['projects']:
                parts.append(f"\n{proj.get('name', '')}: {proj.get('description', '')}")
        
        return '\n'.join(parts)
    
    def chat_feedback(self, question: str, resume_data: Dict[str, Any]) -> str:
        """Interactive chat for resume feedback"""
        
        resume_context = self._format_resume_for_analysis(resume_data)
        
        prompt = f"""
        You are a professional resume consultant. A user is asking for advice about their resume.
        
        Resume Context:
        {resume_context}
        
        User Question: {question}
        
        Provide helpful, specific, and actionable advice. Be encouraging but honest.
        Keep your response concise (2-3 paragraphs maximum).
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error in chat feedback: {e}")
            return "I apologize, but I'm having trouble processing your question right now. Please try again."