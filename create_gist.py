#!/usr/bin/env python3
"""
Script to create or update a GitHub gist with Michael's resume data.
This script will upload the resume.json file to a GitHub gist.

Usage:
    python create_gist.py [github_token]
    
    If no token is provided, you'll be prompted to enter one.
"""

import json
import requests
import sys
import os
from pathlib import Path

def create_or_update_gist(github_token: str, gist_id: str = None):
    """Create a new gist or update an existing one with resume data"""
    
    # Read the resume JSON file
    resume_file = Path("michael_wybraniec_resume.json")
    if not resume_file.exists():
        print("❌ Resume file not found: michael_wybraniec_resume.json")
        return None
    
    with open(resume_file, 'r') as f:
        resume_data = f.read()
    
    # Validate JSON
    try:
        json.loads(resume_data)
        print("✅ Resume JSON is valid")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return None
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "MCP-Resume-Upload"
    }
    
    gist_data = {
        "description": "Michael Wybraniec - Professional Resume (JSON Resume Format)",
        "public": True,
        "files": {
            "resume.json": {
                "content": resume_data
            }
        }
    }
    
    if gist_id:
        # Update existing gist
        url = f"https://api.github.com/gists/{gist_id}"
        response = requests.patch(url, headers=headers, json=gist_data)
        action = "updated"
    else:
        # Create new gist
        url = "https://api.github.com/gists"
        response = requests.post(url, headers=headers, json=gist_data)
        action = "created"
    
    if response.status_code in [200, 201]:
        result = response.json()
        print(f"✅ Gist {action} successfully!")
        print(f"📄 Gist URL: {result['html_url']}")
        print(f"🔗 Gist ID: {result['id']}")
        print(f"📋 Raw URL: {result['files']['resume.json']['raw_url']}")
        
        # Save gist info for future use
        gist_info = {
            "gist_id": result['id'],
            "html_url": result['html_url'],
            "raw_url": result['files']['resume.json']['raw_url'],
            "created_at": result['created_at'],
            "updated_at": result['updated_at']
        }
        
        with open("gist_info.json", "w") as f:
            json.dump(gist_info, f, indent=2)
        
        print("💾 Gist info saved to gist_info.json")
        return result
    else:
        print(f"❌ Failed to {action[:-1]} gist: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def main():
    print("🚀 GitHub Gist Creator for MCP Resume")
    print("=" * 50)
    
    # Get GitHub token
    github_token = None
    if len(sys.argv) > 1:
        github_token = sys.argv[1]
    else:
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            github_token = input("Enter your GitHub Personal Access Token: ").strip()
    
    if not github_token:
        print("❌ GitHub token is required")
        print("💡 Get one at: https://github.com/settings/tokens")
        print("   Required scopes: 'gist'")
        sys.exit(1)
    
    # Check if gist_info.json exists (for updating)
    gist_info_file = Path("gist_info.json")
    existing_gist_id = None
    
    if gist_info_file.exists():
        try:
            with open(gist_info_file, 'r') as f:
                gist_info = json.load(f)
                existing_gist_id = gist_info.get('gist_id')
                print(f"📄 Found existing gist: {existing_gist_id}")
                
                update = input("Update existing gist? (y/n): ").strip().lower()
                if update != 'y':
                    existing_gist_id = None
        except:
            print("⚠️ Could not read existing gist info")
    
    # Create or update gist
    result = create_or_update_gist(github_token, existing_gist_id)
    
    if result:
        print("\n🎉 Success! Your resume is now available as a GitHub gist.")
        print("\n📋 To use in your MCP Resume app:")
        print(f"   1. Copy the Gist ID: {result['id']}")
        print("   2. Add it in the Streamlit app sidebar under 'Resume Source'")
        print("   3. Restart the MCP server with the new gist ID")
        
        print("\n🔗 Quick links:")
        print(f"   • View gist: {result['html_url']}")
        print(f"   • Raw JSON: {result['files']['resume.json']['raw_url']}")

if __name__ == "__main__":
    main() 