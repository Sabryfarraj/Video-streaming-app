pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKER_USERNAME = 'sabryfarraj'
    }

    stages {
        stage('Build Images') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_USERNAME}/auth-service:${BUILD_NUMBER} ./backend/auth-service"
                    sh "docker build -t ${DOCKER_USERNAME}/video-service:${BUILD_NUMBER} ./backend/video-service"
                    sh "docker build -t ${DOCKER_USERNAME}/storage-service:${BUILD_NUMBER} ./backend/storage-service"
                    sh "docker build -t ${DOCKER_USERNAME}/frontend:${BUILD_NUMBER} ./frontend"
                }
            }
        }

        stage('Login to DockerHub') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }

        stage('Push Images') {
            steps {
                script {
                    sh "docker push ${DOCKER_USERNAME}/auth-service:${BUILD_NUMBER}"
                    sh "docker push ${DOCKER_USERNAME}/video-service:${BUILD_NUMBER}"
                    sh "docker push ${DOCKER_USERNAME}/storage-service:${BUILD_NUMBER}"
                    sh "docker push ${DOCKER_USERNAME}/frontend:${BUILD_NUMBER}"
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
    }
}
