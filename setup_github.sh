#!/bin/bash

# GitHub Repository Setup Script
# Run this after creating a new repository on GitHub

echo "🚀 Setting up GitHub repository for ElevenLabs Batch Processor"
echo "=================================================="

# Get GitHub username
GITHUB_USERNAME="ieiskyler"

# Repository name
REPO_NAME="elevenlabs-batch-processor"

# Set up remote
echo "Setting up remote origin..."
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git

# Set main branch
git branch -M main

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo "✅ Repository uploaded successfully!"
echo "🔗 Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "Next steps:"
echo "1. The script will now update all URLs in the project files"
echo "2. A new commit will be made with the updated URLs"
echo "3. Changes will be pushed to GitHub"
