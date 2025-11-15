import os
from typing import Dict, Any

class TemplateManager:
    """Manage LaTeX resume templates"""
    
    def __init__(self):
        self.templates_dir = "templates"
        self.templates = {
            "template1": self._get_professional_template(),
            "template2": self._get_modern_template(),
            "template3": self._get_classic_template()
        }
    
    def get_template(self, template_name: str) -> str:
        """Get a specific template"""
        return self.templates.get(template_name, self.templates["template1"])
    
    def fill_template(self, template_name: str, resume_data: Dict[str, Any]) -> str:
        """Fill template with resume data"""
        template = self.get_template(template_name)
        
        # Replace placeholders with actual data
        filled_template = template
        
        # Personal Info
        personal = resume_data.get('personal_info', {})
        filled_template = filled_template.replace('{{NAME}}', personal.get('name', ''))
        filled_template = filled_template.replace('{{EMAIL}}', personal.get('email', ''))
        filled_template = filled_template.replace('{{PHONE}}', personal.get('phone', ''))
        filled_template = filled_template.replace('{{LINKEDIN}}', personal.get('linkedin', ''))
        filled_template = filled_template.replace('{{GITHUB}}', personal.get('github', ''))
        
        # Summary
        filled_template = filled_template.replace('{{SUMMARY}}', resume_data.get('summary', ''))
        
        # Education
        education_latex = self._format_education(resume_data.get('education', []))
        filled_template = filled_template.replace('{{EDUCATION}}', education_latex)
        
        # Experience
        experience_latex = self._format_experience(resume_data.get('experience', []))
        filled_template = filled_template.replace('{{EXPERIENCE}}', experience_latex)
        
        # Skills
        skills_latex = self._format_skills(resume_data.get('skills', {}))
        filled_template = filled_template.replace('{{SKILLS}}', skills_latex)
        
        # Projects
        projects_latex = self._format_projects(resume_data.get('projects', []))
        filled_template = filled_template.replace('{{PROJECTS}}', projects_latex)
        
        return filled_template
    
    def _format_education(self, education: list) -> str:
        """Format education section for LaTeX"""
        latex = ""
        for edu in education:
            latex += f"""
\\resumeSubheading
  {{{edu.get('degree', '')}}}{{}}
  {{{edu.get('institution', '')}}}{{}}
  {{{edu.get('graduation_date', '')}}}{{}}
  {{GPA: {edu.get('gpa', 'N/A')}}}{{}}
"""
        return latex
    
    def _format_experience(self, experience: list) -> str:
        """Format experience section for LaTeX"""
        latex = ""
        for exp in experience:
            latex += f"""
\\resumeSubheading
  {{{exp.get('title', '')}}}{{}}
  {{{exp.get('company', '')}}}{{}}
  {{{exp.get('start_date', '')} - {exp.get('end_date', '')}}}{{}}
  {{}}{{}}
\\resumeItemListStart
"""
            # Format responsibilities
            responsibilities = exp.get('responsibilities', '')
            if responsibilities:
                for line in responsibilities.split('\n'):
                    line = line.strip()
                    if line and line not in ['', ' ']:
                        # Remove bullet points as LaTeX will add them
                        line = line.replace('•', '').replace('-', '').replace('*', '').strip()
                        if line:
                            latex += f"  \\resumeItem{{{line}}}\n"
            
            latex += "\\resumeItemListEnd\n"
        
        return latex
    
    def _format_skills(self, skills: Dict[str, str]) -> str:
        """Format skills section for LaTeX"""
        if isinstance(skills, dict):
            technical = skills.get('technical', '')
            soft = skills.get('soft', '')
            
            latex = ""
            if technical:
                latex += f"\\textbf{{Technical Skills:}} {technical} \\\\\n"
            if soft:
                latex += f"\\textbf{{Soft Skills:}} {soft}\n"
            return latex
        else:
            return str(skills)
    
    def _format_projects(self, projects: list) -> str:
        """Format projects section for LaTeX"""
        latex = ""
        for proj in projects:
            latex += f"""
\\resumeProjectHeading
  {{\\textbf{{{proj.get('name', '')}}} $|$ \\emph{{{proj.get('technologies', '')}}}}}{{}}
\\resumeItemListStart
  \\resumeItem{{{proj.get('description', '')}}}
\\resumeItemListEnd
"""
        return latex
    
    def _get_professional_template(self) -> str:
        """Professional template (similar to Jake's Resume)"""
        return r"""
\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}

\begin{center}
    \textbf{\Huge \scshape {{NAME}}} \\ \vspace{1pt}
    \small {{PHONE}} $|$ \href{mailto:{{EMAIL}}}{\underline{{{EMAIL}}}} $|$ 
    \href{{{LINKEDIN}}}{\underline{LinkedIn}} $|$
    \href{{{GITHUB}}}{\underline{GitHub}}
\end{center}

\section{Professional Summary}
{{SUMMARY}}

\section{Education}
\resumeSubHeadingListStart
{{EDUCATION}}
\resumeSubHeadingListEnd

\section{Experience}
\resumeSubHeadingListStart
{{EXPERIENCE}}
\resumeSubHeadingListEnd

\section{Technical Skills}
\begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     {{SKILLS}}
    }}
\end{itemize}

\section{Projects}
\resumeSubHeadingListStart
{{PROJECTS}}
\resumeSubHeadingListEnd

\end{document}
"""
    
    def _get_modern_template(self) -> str:
        """Modern template with color accents"""
        return r"""
\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{xcolor}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\definecolor{primary}{RGB}{0,102,204}

\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large\color{primary}
}{}{0em}{}[\color{primary}\titlerule \vspace{-5pt}]

\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{\color{primary}#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}

\begin{center}
    {\Huge \scshape \color{primary} {{NAME}}} \\ \vspace{1pt}
    \small {{PHONE}} $|$ \href{mailto:{{EMAIL}}}{\underline{{{EMAIL}}}} $|$ 
    \href{{{LINKEDIN}}}{\underline{LinkedIn}} $|$
    \href{{{GITHUB}}}{\underline{GitHub}}
\end{center}

\section{Professional Summary}
{{SUMMARY}}

\section{Education}
\resumeSubHeadingListStart
{{EDUCATION}}
\resumeSubHeadingListEnd

\section{Experience}
\resumeSubHeadingListStart
{{EXPERIENCE}}
\resumeSubHeadingListEnd

\section{Technical Skills}
\begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     {{SKILLS}}
    }}
\end{itemize}

\section{Projects}
\resumeSubHeadingListStart
{{PROJECTS}}
\resumeSubHeadingListEnd

\end{document}
"""
    
    def _get_classic_template(self) -> str:
        """Classic template - simple and elegant"""
        # Similar to professional but with minimal styling
        return self._get_professional_template()