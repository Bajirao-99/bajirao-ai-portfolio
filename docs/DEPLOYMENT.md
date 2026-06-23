# Deployment Guide

## Production Platforms

- Frontend: Vercel
- Backend: Render
- Database: Render PostgreSQL
- Repository: GitHub

## Backend Deployment

Render configuration:

```text
Root Directory: backend
Runtime: Docker
Dockerfile: ./Dockerfile
Health Check: /api/v1/health