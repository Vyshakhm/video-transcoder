pipeline {
    agent any

    environment {
        PROJECT_DIR = "transcode_project"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Vyshakhm/video-transcoder.git'
            }
        }

        stage('Clean Up Containers') {
            steps {
                echo "🧹 Stopping and removing any existing containers..."
                sh '''
                    docker compose down || true
                    docker rm -f django-app || true
                    docker rm -f nginx-proxy || true
                    docker network prune -f || true
                '''
            }
        }

    

        stage('Build & Deploy') {
            steps {
                echo "🚀 Building and deploying Docker containers..."
                sh '''
                    docker compose build
                    docker compose up -d
                '''
            }
        }
    }

    post {
        failure {
            echo "❌ Deployment failed."
        }
        success {
            echo "✅ Deployment completed successfully."
        }
    }
}
