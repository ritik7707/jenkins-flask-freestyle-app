
pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        DOCKER = 'C:\\Users\\ritik.mer\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        IMAGE_NAME = 'jenkins-flask-app'
        CONTAINER_NAME = 'jenkins-flask-pipeline-app'
        APP_PORT = '5001'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code checked out successfully.'
            }
        }

        stage('Build Docker Image') {
            steps {
                 bat '"%DOCKER%" build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
                 bat '"%DOCKER%" tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:latest'
    }
}

        stage('Deploy') {
            steps {
                bat '''
                    "%docker%" rm -f %CONTAINER_NAME% 2>NUL
                    "%docker%" run -d --name %CONTAINER_NAME% --restart unless-stopped -p %APP_PORT%:5000 %IMAGE_NAME%:%BUILD_NUMBER%
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Health Check') {
             steps {
                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; $ok=$false; for($i=0; $i -lt 12; $i++){ try { $r=Invoke-WebRequest -UseBasicParsing http://127.0.0.1:5001/health -TimeoutSec 3; if($r.StatusCode -eq 200){ Write-Host $r.Content; $ok=$true; break } } catch { Write-Host 'Waiting for application health...'; Start-Sleep -Seconds 5 } }; if(-not $ok){ & $env:DOCKER logs jenkins-flask-pipeline-app; exit 1 }"
                '''
    }
}

        stage('Deployment Verification') {
            steps {
                bat '"%DOCKER%" ps --filter "name=%CONTAINER_NAME%"'
                bat '"%DOCKER%" inspect --format="{{.Config.Image}}" %CONTAINER_NAME%'
                echo 'Deployment verification completed.'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Review the Console Output and Docker logs.'
            bat '"%DOCKER%" logs %CONTAINER_NAME% 2>NUL || exit /b 0'
        }
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
