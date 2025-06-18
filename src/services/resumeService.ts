import fetch from 'node-fetch';

export interface ResumeData {
  basics?: {
    name?: string;
    label?: string;
    image?: string;
    email?: string;
    phone?: string;
    url?: string;
    summary?: string;
    location?: {
      city?: string;
      countryCode?: string;
    };
  };
  work?: Array<{
    company?: string;
    position?: string;
    startDate?: string;
    endDate?: string;
    summary?: string;
    highlights?: string[];
  }>;
  education?: Array<{
    institution?: string;
    area?: string;
    studyType?: string;
    startDate?: string;
    endDate?: string;
  }>;
  skills?: Array<{
    name?: string;
    level?: string;
    keywords?: string[];
  }>;
  languages?: Array<{
    language?: string;
    fluency?: string;
  }>;
  interests?: Array<{
    name?: string;
    keywords?: string[];
  }>;
  references?: Array<{
    name?: string;
    reference?: string;
  }>;
}

export class ResumeService {
  private cache: ResumeData | null = null;
  private cacheTimestamp: number = 0;
  private readonly cacheTimeout: number = 300000; // 5 minutes

  constructor(
    private readonly gistId: string,
    private readonly githubToken?: string
  ) {}

  async getResume(): Promise<ResumeData> {
    // Check cache
    const now = Date.now();
    if (this.cache && (now - this.cacheTimestamp) < this.cacheTimeout) {
      return this.cache;
    }

    try {
      const headers: Record<string, string> = {
        'User-Agent': 'mcp-resume-server',
        'Accept': 'application/vnd.github.v3+json',
      };

      if (this.githubToken) {
        headers['Authorization'] = `token ${this.githubToken}`;
      }

      const response = await fetch(`https://api.github.com/gists/${this.gistId}`, {
        headers,
      });

      if (!response.ok) {
        throw new Error(`GitHub API error: ${response.status} ${response.statusText}`);
      }

      const gistData = await response.json() as any;
      
      // Find the resume.json file in the gist
      const files = gistData.files;
      const resumeFile = files['resume.json'];
      
      if (!resumeFile) {
        throw new Error('resume.json file not found in gist');
      }

      const resumeData = JSON.parse(resumeFile.content) as ResumeData;
      
      // Update cache
      this.cache = resumeData;
      this.cacheTimestamp = now;
      
      return resumeData;
    } catch (error) {
      throw new Error(`Failed to fetch resume from gist: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  formatAsText(resumeData: ResumeData): string {
    const sections: string[] = [];

    // Basic info
    if (resumeData.basics) {
      const basics = resumeData.basics;
      sections.push(`${basics.name || 'Name not available'}`);
      if (basics.label) sections.push(`${basics.label}`);
      if (basics.email) sections.push(`Email: ${basics.email}`);
      if (basics.phone) sections.push(`Phone: ${basics.phone}`);
      if (basics.url) sections.push(`Website: ${basics.url}`);
      if (basics.summary) sections.push(`\nSUMMARY:\n${basics.summary}`);
    }

    // Work experience
    if (resumeData.work && resumeData.work.length > 0) {
      sections.push('\nWORK EXPERIENCE:');
      resumeData.work.forEach(job => {
        sections.push(`\n${job.company || 'Company'} - ${job.position || 'Position'}`);
        if (job.startDate || job.endDate) {
          sections.push(`${job.startDate || ''} - ${job.endDate || 'Present'}`);
        }
        if (job.summary) sections.push(job.summary);
        if (job.highlights && job.highlights.length > 0) {
          job.highlights.forEach(highlight => sections.push(`• ${highlight}`));
        }
      });
    }

    // Education
    if (resumeData.education && resumeData.education.length > 0) {
      sections.push('\nEDUCATION:');
      resumeData.education.forEach(edu => {
        sections.push(`\n${edu.institution || 'Institution'}`);
        if (edu.area) sections.push(`${edu.studyType || 'Degree'} in ${edu.area}`);
        if (edu.startDate || edu.endDate) {
          sections.push(`${edu.startDate || ''} - ${edu.endDate || 'Present'}`);
        }
      });
    }

    // Skills
    if (resumeData.skills && resumeData.skills.length > 0) {
      sections.push('\nSKILLS:');
      resumeData.skills.forEach(skill => {
        let skillText = skill.name || 'Skill';
        if (skill.level) skillText += ` (${skill.level})`;
        if (skill.keywords && skill.keywords.length > 0) {
          skillText += `: ${skill.keywords.join(', ')}`;
        }
        sections.push(skillText);
      });
    }

    // Languages
    if (resumeData.languages && resumeData.languages.length > 0) {
      sections.push('\nLANGUAGES:');
      resumeData.languages.forEach(lang => {
        sections.push(`${lang.language || 'Language'}: ${lang.fluency || 'Level not specified'}`);
      });
    }

    return sections.join('\n');
  }

  searchResume(resumeData: ResumeData, query: string): any[] {
    const results: any[] = [];
    const searchTerm = query.toLowerCase();

    // Search in basics
    if (resumeData.basics) {
      const basics = resumeData.basics;
      if (basics.summary?.toLowerCase().includes(searchTerm)) {
        results.push({
          section: 'summary',
          content: basics.summary,
          match: 'Summary contains search term'
        });
      }
    }

    // Search in work experience
    if (resumeData.work) {
      resumeData.work.forEach((job, index) => {
        if (job.company?.toLowerCase().includes(searchTerm) ||
            job.position?.toLowerCase().includes(searchTerm) ||
            job.summary?.toLowerCase().includes(searchTerm)) {
          results.push({
            section: 'work',
            index,
            content: job,
            match: 'Work experience contains search term'
          });
        }
      });
    }

    // Search in skills
    if (resumeData.skills) {
      resumeData.skills.forEach((skill, index) => {
        if (skill.name?.toLowerCase().includes(searchTerm) ||
            skill.keywords?.some(keyword => keyword.toLowerCase().includes(searchTerm))) {
          results.push({
            section: 'skills',
            index,
            content: skill,
            match: 'Skill contains search term'
          });
        }
      });
    }

    return results;
  }
} 