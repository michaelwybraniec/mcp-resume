import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

export const config = {
  gistId: process.env.GITHUB_GIST_ID || 'dabf368473d41748e9d6051afb67efcf',
  githubToken: process.env.GITHUB_TOKEN, // Optional - for private gists or higher rate limits
  cacheTimeout: parseInt(process.env.CACHE_TIMEOUT || '300000'), // 5 minutes default
}; 