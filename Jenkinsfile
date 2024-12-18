pipeline {
    agent any
    
    environment {
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')
    }
    
    stages {
        stage('Build Images') {
            steps {
                script {
                    bat "docker build -t sabryfarraj/auth-service:latest ./backend/auth-service"
                    bat "docker build -t sabryfarraj/video-service:latest ./backend/video-service"
                    bat "docker build -t sabryfarraj/storage-service:latest ./backend/storage-service"
                    bat "docker build -t sabryfarraj/frontend:latest ./frontend"
                }
            }
        }
        
        stage('Login to DockerHub') {
            steps {
                bat "docker login -u %DOCKER_CREDENTIALS_USR% -p %DOCKER_CREDENTIALS_PSW%"
            }
        }
        
        stage('Push Images') {
            steps {
                bat "docker push sabryfarraj/auth-service:latest"
                bat "docker push sabryfarraj/video-service:latest"
                bat "docker push sabryfarraj/storage-service:latest"
                bat "docker push sabryfarraj/frontend:latest"
            }
        }
    }
    
    post {
        always {
            bat "docker logout"
        }
    }
}
