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

        stage('Fix nginx/default.conf File') {
            steps {
                echo "🧹 Ensuring nginx/default.conf is a file..."
                sh '''
                    if [ -d nginx/default.conf ]; then
                        echo "Found a directory instead of a file. Deleting it."
                        rm -rf nginx/default.conf
                    fi
                    mkdir -p nginx
                    cat <<EOF > nginx/default.conf
server {
    listen 8000;
    location / {
        proxy_pass http://django-app:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
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
