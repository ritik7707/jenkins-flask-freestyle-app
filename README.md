# Jenkins Freestyle + Docker Demo

A small Flask web application for practicing Git checkout, Jenkins Freestyle builds, Docker image tagging, container replacement, and deployment verification.

## Files

- `app.py` — Flask application with `/` and `/health` endpoints
- `requirements.txt` — Python dependency
- `Dockerfile` — instructions to build the image
- `.dockerignore` — files excluded from the Docker build context

## Run locally with Docker

From this directory:

```bash
docker build -t jenkins-flask-app:local .
docker run -d --name jenkins-flask-app -p 5000:5000 jenkins-flask-app:local
```

Open `http://localhost:5000` and `http://localhost:5000/health`.

To stop/remove the test container:

```bash
docker rm -f jenkins-flask-app
```

## Jenkins Freestyle job (Windows agent)

Create a Freestyle project and configure:

1. **Source Code Management → Git**
   - Repository URL: your GitHub repository URL
   - Branch Specifier: `*/main` (or your actual default branch)
   - Credentials: select credentials only if the repository requires authentication
2. **Build Steps → Execute Windows batch command**
3. Paste this script:

```bat
@echo off
setlocal

echo === Environment check ===
git --version
docker --version
docker info
if errorlevel 1 exit /b 1

echo === Build image ===
docker build -t jenkins-flask-app:%BUILD_NUMBER% .
if errorlevel 1 exit /b 1

echo === Replace previous container if present ===
docker rm -f jenkins-flask-app >NUL 2>&1

echo === Run new container ===
docker run -d --name jenkins-flask-app -p 5000:5000 -e APP_VERSION=%BUILD_NUMBER% jenkins-flask-app:%BUILD_NUMBER%
if errorlevel 1 exit /b 1

echo === Verify container ===
docker ps --filter "name=jenkins-flask-app"
docker logs --tail 50 jenkins-flask-app
curl.exe -fsS http://localhost:5000/health
if errorlevel 1 exit /b 1

echo === Deployment verification complete ===
endlocal
```

## Important notes

- The Jenkins service account must be able to run Git and Docker. If Docker Desktop is used, it must be running and the service account must have appropriate access.
- Make sure port `5000` is free. If it is already in use, change the host-side port in `-p 5000:5000`, for example `-p 5001:5000`, and browse to that host port.
- This is a learning demo. The script replaces the named container after the image builds successfully. For production deployment, use health checks and a rollback strategy.
- For a public GitHub repository, credentials may not be needed to clone. Do not put passwords or access tokens directly in the build script.
