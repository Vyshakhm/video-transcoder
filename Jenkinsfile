pipeline {
    agent any

    triggers {
        pollSCM('* * * * *') // every minute (adjust as needed)
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Vyshakhm/video-transcoder.git'

            }
        }

        stage('Clean Up Containers') {
            steps {
                sh '''
                    docker compose down --remove-orphans || true
                    docker rm -f django-app nginx-proxy || true
                '''
            }
        }

        stage('Build & Deploy') {
            steps {
                sh '''
                    docker compose build
                    docker compose up -d
                '''
            }
        }
    }

    post {
        failure {
            echo '❌ Deployment failed.'
        }
        success {
            echo '✅ Deployment succeeded.'
        }
    }
}
