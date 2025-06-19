"""
Fallback Resume Service

Provides sample resume data when MCP server is not available (e.g., on Streamlit Cloud).
This allows the app to demonstrate functionality even without the full MCP setup.
"""

import json
from typing import Dict, Any

# Michael Wybraniec's REAL CV data from gist (hardcoded for deployment reliability)
SAMPLE_RESUME_DATA = {
    "personal": {
        "name": "Michael Wybraniec",
        "title": "10 Years' Experience · Software Engineer · Architecture · MCP Servers & Coding Agents",
        "location": "Paris & Lyon, FR 🇫🇷 • London, UK 🇬🇧",
        "email": "michael@one-front.com",
        "phone": "(+33) 0 XXX XXX XXX",
        "website": "https://one-front.com",
        "image": "https://media.licdn.com/dms/image/v2/D4D03AQFfMCJNe-bGQA/profile-displayphoto-shrink_800_800/B4DZdAFfIzH4Ac-/0/1749126870070?e=1754524800&v=beta&t=9o7NFNiNcgzPEpll8Xj372MxELNuzo6wloIq9tTqz3U",
        "summary": "With a decade of professional experience spanning the UK 🇬🇧, Spain 🇪🇸, Netherlands 🇳🇱, France 🇫🇷 and Poland 🇵🇱. I bring a unique blend of hands-on full-stack development and strategic software architecture. Over the past seven years, I have delivered scalable, high-performance applications, and for three years, I have architected complex systems that align technical solutions with business goals. As a tech lead, I have driven cross-functional projects in finance, public safety, healthcare, and Web3, leading developer teams and shaping company policies for sustainable growth. I am also a passionate community builder — founding ONE-FRONT and the santeJS JavaScript community — and have shared my expertise at industry conferences. Currently, my focus is on AI-driven development projects, integrating LLMs, Agentic workflows, IDEs, and MCP Servers to drive innovation and build next-generation solutions. To contribute to open-source, I have begun publishing content and code on my website's blog and R&D sections, one-front.com."
    },
    "experience": [
        {
            "company": "ONE-FRONT (Freelance · AI-Driven Agentic Development)",
            "position": "Full-Stack Developer · Architect",
            "duration": "March 2021 - Present",
            "location": "Paris & Lyon, FR 🇫🇷 • London, UK 🇬🇧 • Sicuani, PE 🇵🇪",
            "description": "Delivered high-impact solutions across finance, insurance, public safety, non-profit, and Web3 sectors. Led international teams and end-to-end projects focused on building reliable, scalable, and maintainable systems using modern web technologies and cloud platforms. Built and maintained MCP Server for project documentation, using TypeScript and open-source language models. Created multilingual blog portfolio with error monitoring. Led development of platforms for Eco Village in France, insurance web applications for SanteVet (France/Spain/Italy), secure graph analysis tool for Interpol, Web3 NFT marketplace for Aventus (UK), and finance platforms with QuickBooks integration. Tech Stack: TS · Vue · React · Node · GraphQL · Sentry · Nuxt · CMS · MCP"
        },
        {
            "company": "SanteVet (Freelance · Micro-services, Domain-Driven Design)",
            "position": "Software Architect & Frontend Strategy Lead",
            "duration": "July 2022 - March 2024",
            "location": "Lyon, FR 🇫🇷",
            "description": "Drove pivotal multinational transformation of frontend architecture, establishing foundation for scalable product development across France 🇫🇷, Spain 🇪🇸, and Italy 🇮🇹. Planned and executed company-wide ONE-FRONT Engineering Strategy (2022–2024). Unified frontend architecture across regions with shared components and Contentful CMS integration. Founded and led 'santeJS' internal JavaScript community. Defined Frontend Security Policy v1 (2023). Led technical interviews and code reviews. Tech Stack: TypeScript, Vue 2 & 3, Nuxt 2 Bridge & Nuxt 3, Pinia, Contentful, AWS."
        },
        {
            "company": "Interpol (Freelance via Accenture & Asenium · Ripjar Solutions)",
            "position": "Full-Stack Developer · Security & Intelligence Systems",
            "duration": "July 2021 - June 2022",
            "location": "Lyon, FR 🇫🇷",
            "description": "Maintained secure architecture in scalable intelligence platform supporting European law enforcement agencies. Engineered modular full-stack system for large-scale graph analytics, entity resolution, and real-time visualization. Integrated heterogeneous data sources across cloud, on-premise, and data lake architectures. Developed secure orchestration pipelines and implemented NLP techniques for multilingual unstructured data. Built hardened, high-security features for sensitive deployments. Tech Stack: TypeScript, React, Elasticsearch, GraphQL, SQL, NLP."
        },
        {
            "company": "Inpart (Biopharmacy Lead Discovery)",
            "position": "Frontend Developer · Cross-Platform Web & Mobile",
            "duration": "March 2020 - March 2021",
            "location": "Lyon, FR 🇫🇷",
            "description": "Contributed to design and development of 'Lead Space' — cross-platform partnering platform for pharma and innovation industry. Built responsive, mobile-ready UIs using Vue.js, Quasar Framework, and TypeScript. Improved performance and accessibility, ensuring consistent UX across devices. Integrated real-time user feedback and analytics to rapidly iterate on product features. Tech Stack: Vue.js, Quasar, TypeScript, JavaScript, Responsive Design."
        },
        {
            "company": "Uplab · eCommerce SaaS",
            "position": "Full-Stack Developer · Financial SaaS & API Integrations",
            "duration": "August 2019 - March 2020",
            "location": "Lyon, FR 🇫🇷",
            "description": "Designed and delivered full-stack SaaS platform to automate financial reporting, tax declaration, and forecasting for Labelium. Integrated QuickBooks API for real-time financial data sync. Developed backend logic using Node.js and MongoDB. Built interactive dashboards with Vue.js and jQuery. Tech Stack: TypeScript, Node.js, MongoDB, Vue.js, jQuery, QuickBooks API."
        },
        {
            "company": "PVH Corp.",
            "position": "Senior Data Analyst · Calvin Klein & Tommy Hilfiger Division",
            "duration": "August 2017 - April 2018",
            "location": "Amsterdam, NL 🇳🇱",
            "description": "Supported data analysis and production planning for Calvin Klein and Tommy Hilfiger operations across Europe. Delivered insights for customer service optimization and B2B application reliability through analytics and software testing. Performed data analysis for production planning, provided 3rd-line support for customer service, and tested internal B2B sales applications."
        }
    ],
    "skills": {
        "core_expertise": [
            "Full-Stack", "JavaScript", "TypeScript", "Vue 3", "Nuxt 3", "React", 
            "Next.js", "Node.js", "Migration", "Architecture", "Agile", "API", 
            "REST", "GraphQL", "Swagger", "Postman", "OpenAPI"
        ],
        "ai_mcp": [
            "AI Software Engineering", "LLM-Integrated Platforms", "Model Context Protocol (MCP)", 
            "MCP Server Management", "Autonomous Agents", "Agent Scheduling", "Prompt Engineering", 
            "RAG (Retrieval-Augmented Generation)", "Vector Databases", "System Architecture for AI", 
            "OpenAI API", "Anthropic Claude", "Function Calling", "Tool Use", "Multi-Agent Coordination"
        ],
        "backend_devops": [
            "Node.js", "Express", "Fastify", "NestJS", "TypeORM", "Prisma", 
            "MySQL", "PostgreSQL", "MongoDB", "MariaDB", "Firebase", "Redis", 
            "ElasticSearch", "DynamoDB", "WebSockets", "Socket.IO", "RabbitMQ", 
            "Jenkins", "Docker", "GitHub Actions", "GitLab CI", "Bitbucket Pipelines"
        ],
        "cloud_serverless": [
            "AWS Lambda", "API Gateway", "AppSync", "Cognito", "Step Functions", 
            "Lambda@Edge", "S3", "AWS Amplify", "Heroku"
        ],
        "frontend": [
            "Vue 3", "Nuxt 3", "Pinia", "Vuex", "Vuetify", "Quasar", "ReactJS", 
            "Redux", "NextJS", "Tailwind CSS", "SASS", "LESS", "Bootstrap", 
            "Vite", "Webpack", "Responsive Web Design", "Web Components", "PWA"
        ],
        "languages": ["🇬🇧 English (Native speaker)", "🇫🇷 French (Advanced)", "🇵🇱 Polish (Native speaker)", "🇪🇸 Spanish (Beginner)"],
        "certifications": [
            "Advanced React Development", "Node.js Security", "Vue.js Fundamentals", 
            "TypeScript for Node.js Developers", "Scrum Master Prep", "AWS Deep Learning"
        ]
    },
    "education": [
        {
            "degree": "Ongoing - Continuous Professional Development",
            "institution": "Various Platforms (LinkedIn Learning, Pluralsight)",
            "year": "2019-2024",
            "location": "Online",
            "specialization": "AI/ML, Cloud Architecture, Advanced JavaScript"
        }
    ],
    "projects": [
        {
            "name": "MCP Resume System",
            "description": "Revolutionary AI-powered resume screening system using Model Context Protocol. Features real-time GitHub gist integration, multiple LLM provider support, and ChatGPT-style interface. Deployed on Streamlit Cloud with automatic Node.js fallback.",
            "technologies": ["TypeScript", "Python", "Streamlit", "OpenAI", "MCP", "GitHub API", "Docker"],
            "url": "https://github.com/michaelwybraniec/mcp-resume",
            "status": "Production",
            "year": "2024"
        },
        {
            "name": "SanteVet Frontend Architecture",
            "description": "Led multinational transformation of frontend architecture across France, Spain, and Italy. Unified components with Contentful CMS integration and established scalable development practices.",
            "technologies": ["Vue 3", "Nuxt 3", "TypeScript", "Contentful", "AWS", "Pinia"],
            "url": "https://www.santevet.com",
            "status": "Production", 
            "year": "2022-2024"
        },
        {
            "name": "Interpol Intelligence Platform",
            "description": "Secure graph analysis tool for European law enforcement. Large-scale analytics, entity resolution, and real-time visualization with multilingual NLP integration.",
            "technologies": ["React", "TypeScript", "Elasticsearch", "GraphQL", "SQL", "NLP"],
            "url": "https://ripjar.com",
            "status": "Production",
            "year": "2021-2022"
        },
        {
            "name": "Lead Space - Pharma Platform",
            "description": "Cross-platform partnering platform for pharma and innovation industry. Responsive UIs with seamless web-to-mobile experiences.",
            "technologies": ["Vue.js", "Quasar", "TypeScript", "Responsive Design"],
            "url": "https://www.inpart.io",
            "status": "Production",
            "year": "2020-2021"
        }
    ],
    "achievements": [
        "Founded ONE-FRONT, serving international clients across France, UK, Spain, Netherlands, and Peru",
        "Architected and led multinational frontend transformation at SanteVet (France/Spain/Italy)",
        "Developed secure intelligence systems for Interpol supporting European law enforcement",
        "Founded and directed 'santeJS' JavaScript community for knowledge sharing and innovation",
        "Pioneered MCP Resume System - first-of-its-kind AI recruitment tool with Model Context Protocol",
        "Led cross-functional teams across finance, public safety, healthcare, and Web3 sectors",
        "Delivered scalable solutions for pharma, insurance, and fintech industries",
        "Established Frontend Security Policy v1 and engineering best practices",
        "Expert in multilingual platform development with full i18n support"
    ],
    "industries": [
        "Artificial Intelligence & MCP Servers",
        "Insurance Technology (InsurTech)",
        "Public Safety & Law Enforcement",
        "Pharmaceutical & Healthcare Technology", 
        "Financial Technology (FinTech)",
        "Web3 & Blockchain",
        "Non-Profit & Social Impact",
        "Fashion & Retail (Calvin Klein, Tommy Hilfiger)"
    ]
}

class FallbackResumeService:
    """Provides resume data when MCP server is not available"""
    
    def __init__(self):
        self.data = SAMPLE_RESUME_DATA
    
    def get_full_resume(self) -> Dict[str, Any]:
        """Get complete resume data"""
        return self.data
    
    def get_experience(self) -> Dict[str, Any]:
        """Get work experience"""
        return {"experience": self.data["experience"]}
    
    def get_skills(self) -> Dict[str, Any]:
        """Get skills and technologies"""
        return {"skills": self.data["skills"]}
    
    def get_education(self) -> Dict[str, Any]:
        """Get education information"""
        return {"education": self.data["education"]}
    
    def get_projects(self) -> Dict[str, Any]:
        """Get project information"""
        return {"projects": self.data["projects"]}
    
    def get_summary(self) -> Dict[str, Any]:
        """Get professional summary"""
        return {"summary": self.data["personal"]["summary"]}
    
    def get_achievements(self) -> Dict[str, Any]:
        """Get achievements and accomplishments"""
        return {"achievements": self.data["achievements"]}
    
    def get_industries(self) -> Dict[str, Any]:
        """Get industry experience"""
        return {"industries": self.data["industries"]}
    
    def search_resume(self, query: str) -> Dict[str, Any]:
        """Search resume content"""
        # Simple search implementation
        results = []
        query_lower = query.lower()
        
        # Search in experience
        for exp in self.data["experience"]:
            if (query_lower in exp["description"].lower() or 
                query_lower in exp["position"].lower() or
                query_lower in exp["company"].lower()):
                results.append({"type": "experience", "data": exp})
        
        # Search in skills
        for skill in self.data["skills"]["technical"]:
            if query_lower in skill.lower():
                results.append({"type": "technical_skill", "name": skill})
        
        # Search in frameworks
        for framework in self.data["skills"]["frameworks"]:
            if query_lower in framework.lower():
                results.append({"type": "framework", "name": framework})
        
        # Search in AI/ML skills
        for ai_skill in self.data["skills"]["ai_ml"]:
            if query_lower in ai_skill.lower():
                results.append({"type": "ai_ml_skill", "name": ai_skill})
        
        # Search in projects
        for project in self.data["projects"]:
            if (query_lower in project["name"].lower() or 
                query_lower in project["description"].lower() or
                any(query_lower in tech.lower() for tech in project["technologies"])):
                results.append({"type": "project", "data": project})
        
        # Search in achievements
        for achievement in self.data["achievements"]:
            if query_lower in achievement.lower():
                results.append({"type": "achievement", "description": achievement})
        
        return {"search_results": results, "query": query, "total_results": len(results)}
    
    def analyze_job_match(self, job_description: str) -> Dict[str, Any]:
        """Analyze how well the resume matches a job description"""
        # Comprehensive keyword matching
        job_lower = job_description.lower()
        matched_technical_skills = []
        matched_frameworks = []
        matched_ai_skills = []
        matched_industries = []
        relevant_projects = []
        relevant_experience = []
        
        # Match technical skills
        for skill in self.data["skills"]["technical"]:
            if skill.lower() in job_lower:
                matched_technical_skills.append(skill)
        
        # Match frameworks
        for framework in self.data["skills"]["frameworks"]:
            if framework.lower() in job_lower:
                matched_frameworks.append(framework)
        
        # Match AI/ML skills
        for ai_skill in self.data["skills"]["ai_ml"]:
            if ai_skill.lower() in job_lower:
                matched_ai_skills.append(ai_skill)
        
        # Match industries
        for industry in self.data["industries"]:
            if any(word in job_lower for word in industry.lower().split()):
                matched_industries.append(industry)
        
        # Find relevant projects
        for project in self.data["projects"]:
            if any(tech.lower() in job_lower for tech in project["technologies"]):
                relevant_projects.append(project["name"])
        
        # Find relevant experience
        for exp in self.data["experience"]:
            if any(word in job_lower for word in exp["description"].lower().split() if len(word) > 4):
                relevant_experience.append(f"{exp['position']} at {exp['company']}")
        
        # Calculate match score
        total_matches = (len(matched_technical_skills) + len(matched_frameworks) + 
                        len(matched_ai_skills) + len(relevant_projects) * 2 + 
                        len(relevant_experience) * 2)
        match_score = min(total_matches * 8, 100)  # Cap at 100%
        
        # Generate recommendations
        recommendations = []
        if matched_technical_skills:
            recommendations.append(f"Highlight these matching technical skills: {', '.join(matched_technical_skills[:3])}")
        if matched_frameworks:
            recommendations.append(f"Emphasize experience with: {', '.join(matched_frameworks[:2])}")
        if matched_ai_skills:
            recommendations.append(f"Showcase AI/ML expertise in: {', '.join(matched_ai_skills[:2])}")
        if relevant_projects:
            recommendations.append(f"Mention relevant projects like: {', '.join(relevant_projects[:2])}")
        if relevant_experience:
            recommendations.append(f"Draw from experience: {relevant_experience[0] if relevant_experience else 'Focus on leadership roles'}")
        
        if not recommendations:
            recommendations = [
                "Emphasize transferable skills and quick learning ability",
                "Highlight problem-solving and analytical skills",
                "Show enthusiasm for learning new technologies"
            ]
        
        return {
            "match_score": match_score,
            "matched_skills": {
                "technical": matched_technical_skills,
                "frameworks": matched_frameworks,
                "ai_ml": matched_ai_skills
            },
            "matched_industries": matched_industries,
            "relevant_projects": relevant_projects,
            "relevant_experience": relevant_experience,
            "recommendations": recommendations,
            "summary": f"Strong candidate with {match_score}% compatibility. {len(matched_technical_skills + matched_frameworks + matched_ai_skills)} matching technical skills found."
        }

# Global instance
fallback_service = FallbackResumeService() 