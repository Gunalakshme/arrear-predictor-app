# Deploying a React (Vite) App to GitHub Pages
## Complete Step-by-Step Guide

**Project:** Arrear Predictor App  
**Author:** Gunalakshme  
**Date:** June 1, 2026  
**Live URL:** https://gunalakshme.github.io/arrear-predictor-app/

---

## Table of Contents

1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
3. [Step 1: Configure Vite for GitHub Pages](#step-1-configure-vite-for-github-pages)
4. [Step 2: Create GitHub Actions Workflow](#step-2-create-github-actions-workflow)
5. [Step 3: Update .gitignore](#step-3-update-gitignore)
6. [Step 4: Create a GitHub Repository](#step-4-create-a-github-repository)
7. [Step 5: Install and Authenticate GitHub CLI](#step-5-install-and-authenticate-github-cli)
8. [Step 6: Initialize Git and Push Code](#step-6-initialize-git-and-push-code)
9. [Step 7: Enable GitHub Pages](#step-7-enable-github-pages)
10. [Step 8: Verify Deployment](#step-8-verify-deployment)
11. [Updating Your App](#updating-your-app)
12. [Troubleshooting](#troubleshooting)

---

## 1. Overview

This guide walks through the complete process of deploying a **React application** (built with **Vite**) to **GitHub Pages** — a free static site hosting service provided by GitHub. Once deployed, your app will be accessible to anyone on the internet via a public URL.

### How It Works

```
Your Code → Push to GitHub → GitHub Actions (auto-build) → GitHub Pages (hosting) → Live URL
```

**GitHub Actions** automatically builds your app every time you push code, and **GitHub Pages** serves the built files as a static website.

---

## 2. Prerequisites

Before starting, ensure you have:

- **Node.js** (v18 or later) installed — check with `node --version`
- **npm** installed — check with `npm --version`
- **Git** installed — check with `git --version`
- A **GitHub account** at [github.com](https://github.com)
- A working **Vite + React** project that runs locally with `npm run dev`
- **Homebrew** (macOS) — check with `brew --version`

---

## Step 1: Configure Vite for GitHub Pages

### Why This Is Needed

GitHub Pages serves your app from a subpath (e.g., `https://username.github.io/repo-name/`), not from the root (`/`). By default, Vite assumes your app is served from `/`, which would cause all asset paths (CSS, JS, images) to break. Setting the `base` option fixes this.

### What To Do

Open the file `vite.config.js` in your project root and add the `base` property:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/arrear-predictor-app/',
})
```

### Key Details

| Property | Value | Purpose |
|----------|-------|---------|
| `base` | `'/arrear-predictor-app/'` | Must match your GitHub repository name exactly, wrapped in `/` slashes |

> **Important:** The `base` value MUST match your GitHub repository name. If your repo is named `my-cool-app`, then set `base: '/my-cool-app/'`.

---

## Step 2: Create GitHub Actions Workflow

### Why This Is Needed

GitHub Actions is a CI/CD (Continuous Integration/Continuous Deployment) service built into GitHub. We create a **workflow file** that tells GitHub to automatically build and deploy your app whenever you push code to the `main` branch.

### What To Do

Create the following directory and file in your project:

```
.github/
  workflows/
    deploy.yml
```

Create the file `.github/workflows/deploy.yml` with this content:

```yaml
# Deploy to GitHub Pages
name: Deploy to GitHub Pages

on:
  push:
    branches: ['main']
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: 'pages'
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './dist'

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Workflow Breakdown

| Section | Purpose |
|---------|---------|
| `on: push: branches: ['main']` | Triggers the workflow on every push to the `main` branch |
| `workflow_dispatch` | Allows you to manually trigger the workflow from GitHub's UI |
| `permissions` | Grants the workflow permission to read code and write to GitHub Pages |
| `concurrency` | Prevents multiple deployments from running simultaneously |
| **Build Job** | Checks out code, installs Node.js, runs `npm ci` and `npm run build` |
| **Deploy Job** | Takes the built `./dist` folder and deploys it to GitHub Pages |

---

## Step 3: Update .gitignore

### Why This Is Needed

The `.gitignore` file tells Git which files and folders to exclude from the repository. We don't want to push unnecessary files like `node_modules`, build outputs, or local-only files.

### What To Do

Ensure your `.gitignore` file includes at minimum:

```
# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
dist
dist-ssr
*.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

# Python / local files (if applicable)
venv-pdf
*.pdf
*.bat
generate_doc.py
```

### Key Exclusions

| Excluded | Reason |
|----------|--------|
| `node_modules` | Dependencies are installed from `package.json` during build — no need to upload them (they can be 100s of MBs) |
| `dist` | Build output is generated by GitHub Actions — we don't commit it |
| `.DS_Store` | macOS system files that are not needed |
| `venv-pdf` | Python virtual environment not needed for the web app |

---

## Step 4: Create a GitHub Repository

### What To Do

1. Go to **[github.com/new](https://github.com/new)** in your browser
2. Fill in the details:
   - **Repository name:** `arrear-predictor-app` (must match the `base` in `vite.config.js`)
   - **Description:** (optional) "Arrear Predictor App"
   - **Visibility:** Select **Public** (required for free GitHub Pages)
3. **DO NOT** check any of these boxes:
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license
4. Click **Create repository**

> **Why Public?** GitHub Pages is free only for public repositories on the free plan. Private repos require GitHub Pro.

> **Why no README/gitignore?** We already have these files in our local project. Adding them on GitHub would create conflicts when pushing.

---

## Step 5: Install and Authenticate GitHub CLI

### Why This Is Needed

To push code from your computer to GitHub, Git needs to authenticate with your GitHub account. The **GitHub CLI (`gh`)** is the easiest way to set this up on macOS.

### 5a. Install GitHub CLI

Open your terminal and run:

```bash
brew install gh
```

Expected output:
```
==> Pouring gh--2.93.0.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/gh/2.93.0: 229 files, 37.9MB
```

### 5b. Authenticate with GitHub

Run:

```bash
gh auth login
```

When prompted, select:
1. **Where do you use GitHub?** → `GitHub.com`
2. **Preferred protocol?** → `HTTPS`
3. **Authenticate Git with your GitHub credentials?** → `Yes`
4. **How would you like to authenticate?** → `Login with a web browser`

The CLI will display a **one-time code** (e.g., `0D44-A547`). Press Enter to open your browser, paste the code, and click **Authorize**.

Expected success message:
```
✓ Authentication complete.
✓ Configured git protocol
✓ Logged in as Gunalakshme
```

---

## Step 6: Initialize Git and Push Code

### What To Do

Run the following commands in your terminal, **one by one**:

```bash
# Navigate to your project directory
cd /path/to/your/arrear-predictor-app

# Initialize a new Git repository
git init

# Add all files to staging
git add .

# Create the first commit
git commit -m "Initial commit: Arrear Predictor App"

# Rename the branch to 'main' (GitHub's default)
git branch -M main

# Connect your local repo to the GitHub repo
git remote add origin https://github.com/Gunalakshme/arrear-predictor-app.git

# Push the code to GitHub
git push -u origin main
```

### Command Breakdown

| Command | What It Does |
|---------|--------------|
| `git init` | Creates a new `.git` folder, turning your project into a Git repository |
| `git add .` | Stages all files (respecting `.gitignore`) for the next commit |
| `git commit -m "..."` | Saves a snapshot of your staged files with a descriptive message |
| `git branch -M main` | Renames the default branch from `master` to `main` |
| `git remote add origin <URL>` | Links your local repo to the GitHub repo (replace URL with yours) |
| `git push -u origin main` | Uploads your code to GitHub and sets `main` as the default push target |

Expected output for `git push`:
```
To https://github.com/Gunalakshme/arrear-predictor-app.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

---

## Step 7: Enable GitHub Pages

### What To Do

#### Option A: Using GitHub CLI (Faster)

Run this command:

```bash
gh api repos/Gunalakshme/arrear-predictor-app/pages -X POST -f build_type=workflow
```

This enables GitHub Pages with **GitHub Actions** as the build source.

#### Option B: Using GitHub Website (Manual)

1. Go to your repository on GitHub: `https://github.com/Gunalakshme/arrear-predictor-app`
2. Click the **Settings** tab (gear icon)
3. In the left sidebar, click **Pages**
4. Under **Build and deployment → Source**, select **GitHub Actions**
5. Click **Save**

---

## Step 8: Verify Deployment

### Check the Workflow Status

Once you push code and enable Pages, the GitHub Actions workflow runs automatically.

#### Using CLI:

```bash
gh run list --repo Gunalakshme/arrear-predictor-app --limit 3
```

#### Using GitHub Website:

1. Go to your repo → click the **Actions** tab
2. You should see a workflow run named "Deploy to GitHub Pages"
3. Click on it to see the progress

### Expected Results

The workflow has two jobs:

```
✓ build  (23s) — Installs dependencies and builds the app
✓ deploy (20s) — Deploys the built files to GitHub Pages
```

### Access Your Live App

Once both jobs show ✓, your app is live at:

```
https://gunalakshme.github.io/arrear-predictor-app/
```

> **Note:** It may take 1-2 minutes after deployment for the URL to become active for the first time.

---

## Updating Your App

Whenever you make changes to your app, deploy the update with just 3 commands:

```bash
# Stage all changes
git add .

# Commit with a descriptive message
git commit -m "Describe what you changed"

# Push to GitHub (auto-deploys in ~1 minute)
git push
```

The GitHub Actions workflow will automatically rebuild and redeploy your app.

---

## Troubleshooting

### Common Issues and Solutions

| Problem | Solution |
|---------|----------|
| **404 error on the live URL** | Check that `base` in `vite.config.js` matches your repo name exactly |
| **Blank page loads** | Open browser DevTools (F12) → Console tab. Look for asset loading errors. Usually a `base` path issue |
| **Workflow fails at "Install dependencies"** | Make sure `package-lock.json` is committed (not in `.gitignore`) |
| **Workflow fails at "Build"** | Run `npm run build` locally first to check for build errors |
| **"Permission denied" on push** | Re-run `gh auth login` to re-authenticate |
| **"Repository not found" on push** | Verify the repo exists at `github.com/YOUR_USERNAME/REPO_NAME` and the remote URL is correct |

### Useful Commands

```bash
# Check your Git remote URL
git remote -v

# Check GitHub authentication status
gh auth status

# Manually trigger a deployment
gh workflow run deploy.yml --repo Gunalakshme/arrear-predictor-app

# View recent workflow runs
gh run list --repo Gunalakshme/arrear-predictor-app
```

---

## Architecture Summary

```
┌──────────────────────────────────────────────────────────┐
│                    Your Computer                         │
│                                                          │
│  arrear-predictor-app/                                   │
│  ├── src/                  ← React source code           │
│  ├── public/               ← Static assets               │
│  ├── vite.config.js        ← Build config (base path)    │
│  ├── package.json          ← Dependencies & scripts      │
│  └── .github/workflows/                                  │
│      └── deploy.yml        ← CI/CD pipeline              │
│                                                          │
│         │  git push                                      │
│         ▼                                                │
│  ┌──────────────────────────────────────────────────┐    │
│  │              GitHub Repository                    │    │
│  │     github.com/Gunalakshme/arrear-predictor-app   │    │
│  │                                                    │    │
│  │  ┌──────────────────────────────────────────┐     │    │
│  │  │         GitHub Actions                    │     │    │
│  │  │  1. Checkout code                         │     │    │
│  │  │  2. Install Node.js                       │     │    │
│  │  │  3. npm ci (install deps)                 │     │    │
│  │  │  4. npm run build (creates dist/)         │     │    │
│  │  │  5. Upload dist/ to Pages                 │     │    │
│  │  └──────────────────────────────────────────┘     │    │
│  │                     │                              │    │
│  │                     ▼                              │    │
│  │  ┌──────────────────────────────────────────┐     │    │
│  │  │         GitHub Pages                      │     │    │
│  │  │  Serves static files from dist/           │     │    │
│  │  │                                           │     │    │
│  │  │  URL: gunalakshme.github.io/              │     │    │
│  │  │       arrear-predictor-app/               │     │    │
│  │  └──────────────────────────────────────────┘     │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

---

*Guide generated on June 1, 2026*
