# Bajirao AI Portfolio

An advanced full-stack AI-powered professional portfolio built with React, FastAPI, PostgreSQL, Docker, Gemini, semantic embeddings, and Retrieval-Augmented Generation.

The platform presents professional experience, projects, research, skills, coding profiles, resumes, and achievements while also providing AI-powered job-description matching and a portfolio chatbot grounded in verified portfolio data.

## Live Application

- Frontend: `https://YOUR-VERCEL-URL`
- Backend API: `https://api.bajiraosalunke.com`
- Health Check: `https://api.bajiraosalunke.com/api/v1/health`

Replace `YOUR-VERCEL-URL` with the exact deployed Vercel production URL.

---

## Overview

Bajirao AI Portfolio is more than a static personal website. It is a complete full-stack application that allows recruiters and visitors to:

- Explore professional experience, education, skills, projects, research, achievements, and certifications.
- Download role-specific resume versions.
- Compare a job description against the portfolio.
- View matched skills, missing skills, relevant projects, research, and experience.
- Receive an explainable portfolio-fit score.
- Ask questions through a RAG-based AI portfolio chatbot.
- Submit contact and interview requests.
- View GitHub repositories and coding-profile achievements.

The platform also includes a secure administration dashboard for managing all public content, recruiter messages, AI activity, resume files, project screenshots, and analytics.

---

## Main Features

### Public Portfolio

- Professional profile
- Education history
- Work experience
- Technical skills
- Achievements
- Certifications
- Featured projects
- Research and publications
- GitHub integration
- Coding-profile integration
- Multiple resume downloads
- Contact form
- Interview request form

### AI Job Description Matcher

The visitor can paste a job description and receive:

- Overall portfolio match score
- Skill-match score
- Semantic similarity score
- Experience relevance
- Project relevance
- Research relevance
- Matched skills
- Missing skills
- Relevant professional experience
- Relevant projects
- Relevant research
- Strengths and improvement areas
- Recommended resume version

### AI Portfolio Chatbot

The chatbot uses portfolio-grounded Retrieval-Augmented Generation to answer questions such as:

- What are Bajirao's strongest technical skills?
- Explain the RecruitAI Pro project.
- What was the result of the Hindi event-extraction research?
- Is he suitable for a Python backend role?
- What teaching experience does he have?

The chatbot retrieves relevant portfolio records before generating an answer and displays supporting sources.

### Admin Dashboard

- JWT-based administrator authentication
- Protected routes
- Dashboard analytics
- Profile management
- Education CRUD
- Experience CRUD
- Skills CRUD
- Achievement CRUD
- Certification CRUD
- Project CRUD
- Research CRUD
- Coding-profile CRUD
- Project screenshot management
- Resume PDF management
- Contact-message management
- Interview-request management
- AI job-match history
- Chat-interaction history

### Analytics

- Unique visitors
- Total page views
- Project views
- Resume downloads
- Contact-message counts
- Interview-request counts
- JD-match activity
- AI-chat usage
- Top pages
- Top projects
- Daily page-view statistics

---

## Application Screenshots

### Public Portfolio

![Public portfolio home page](docs/screenshots/01-home-page.png)

### AI Job Description Matcher

![AI job matching result](docs/screenshots/05-job-match-result.png)

### AI Portfolio Chatbot

![Portfolio chatbot](docs/screenshots/06-ai-chatbot.png)

### Admin Analytics Dashboard

![Admin dashboard](docs/screenshots/08-admin-dashboard.png)

### Content Manager

![Admin content manager](docs/screenshots/09-content-manager.png)

## Technology Stack

### Frontend

- React
- TypeScript
- Vite
- React Router
- Lucide React
- CSS
- Vercel Analytics
- Vercel Speed Insights

### Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic Settings
- Psycopg 3
- JWT authentication
- Gemini API
- Sentence Transformers
- REST APIs

### Database

- PostgreSQL
- Render PostgreSQL
- Alembic migrations

### AI and NLP

- Gemini generative AI
- Sentence-transformer embeddings
- Semantic similarity
- Skill extraction
- Hybrid scoring
- Retrieval-Augmented Generation
- Grounded source attribution

### DevOps and Deployment

- Docker
- Docker Compose
- Nginx
- GitHub Actions
- Render
- Vercel
- Health checks
- Automated migrations
- CI testing

---

## System Architecture

```mermaid
flowchart LR
    U[Portfolio Visitor] --> VF[Vercel React Frontend]
    A[Administrator] --> VF

    VF --> API[Render FastAPI Backend]

    API --> DB[(Render PostgreSQL)]
    API --> GEMINI[Gemini API]
    API --> EMB[Sentence Transformer Embeddings]
    API --> GH[GitHub API]
    API --> FS[Persistent Upload Storage]

    DB --> PROFILE[Portfolio Content]
    DB --> ANALYTICS[Analytics]
    DB --> AIHISTORY[AI Activity]
    DB --> MESSAGES[Contact and Interview Requests]

    API --> AUTH[JWT Authentication]
    AUTH --> ADMIN[Protected Admin Dashboard]