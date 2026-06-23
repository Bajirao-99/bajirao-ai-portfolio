# System Architecture

## 1. Architecture Overview

Bajirao AI Portfolio follows a layered full-stack architecture.

```mermaid
flowchart TB
    CLIENT[Browser Client]

    subgraph FRONTEND[Vercel Frontend]
        REACT[React + TypeScript]
        ROUTER[React Router]
        UI[Public and Admin UI]
        TRACKER[Analytics Tracker]
    end

    subgraph BACKEND[Render Backend]
        FASTAPI[FastAPI Application]
        ROUTES[REST API Routes]
        AUTH[JWT Authentication]
        SERVICES[Business Services]
        RAG[RAG Chat Service]
        MATCHER[JD Matching Service]
        ANALYTICS[Analytics Service]
        FILES[File Management]
    end

    subgraph DATA[Data Layer]
        POSTGRES[(PostgreSQL)]
        STORAGE[(Persistent Upload Storage)]
    end

    subgraph EXTERNAL[External Services]
        GEMINI[Gemini API]
        EMBEDDINGS[Sentence Transformer Model]
        GITHUB[GitHub API]
        VERCEL_ANALYTICS[Vercel Analytics]
    end

    CLIENT --> REACT
    REACT --> ROUTER
    ROUTER --> UI
    UI --> FASTAPI
    TRACKER --> FASTAPI

    FASTAPI --> ROUTES
    ROUTES --> AUTH
    ROUTES --> SERVICES

    SERVICES --> RAG
    SERVICES --> MATCHER
    SERVICES --> ANALYTICS
    SERVICES --> FILES

    SERVICES --> POSTGRES
    FILES --> STORAGE

    RAG --> GEMINI
    RAG --> EMBEDDINGS
    MATCHER --> EMBEDDINGS
    SERVICES --> GITHUB

    REACT --> VERCEL_ANALYTICS