# Security Documentation

## Secret Management

Secrets are stored in environment variables and are excluded from Git.

Protected values include:

- Database URLs
- Database passwords
- JWT secret
- Gemini API key
- GitHub token
- Administrator credentials

## Authentication

Administrator routes use JWT bearer authentication.

Passwords are never stored in plain text.

The frontend stores the access token in session storage for the active browser tab.

## API Security

The backend includes:

- Trusted-host validation
- Environment-based CORS
- Security response headers
- Production-safe error responses
- Request IDs
- File type validation
- Upload size validation
- Input validation using Pydantic
- SQLAlchemy parameterized database operations

## Production Headers

The application sends:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy
Strict-Transport-Security