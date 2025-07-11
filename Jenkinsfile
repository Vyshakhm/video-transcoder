pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'video_transcoder'
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Vyshakhm/video-transcoder.git'
            }
        }

        stage('Stop & Remove Existing Containers') {
            steps {
                script {
                    sh """
                    docker-compose down --remove-orphans
                    """
                }
            }
        }

        stage('Build & Deploy with Docker Compose') {
            steps {
                script {
                    sh """
                    docker-compose build
                    docker-compose up -d
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Deployment completed successfully.'
        }
        failure {
            echo '❌ Deployment failed.'
        }
    }
}
