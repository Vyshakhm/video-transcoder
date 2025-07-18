pipeline {
    agent any

    environment {
        PROJECT_DIR = "transcode_project"
        REMOTE_USER = "ubuntu"
        REMOTE_HOST = "10.0.1.126"
        REMOTE_PATH = "/home/ubuntu/app"
        SSH_KEY = credentials('Jenkins_ssh') // Add your SSH private key in Jenkins Credentials
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Vyshakhm/video-transcoder.git'
            }
        }

        stage('Copy Files to Remote') {
            steps {
                sshagent(credentials: ['Jenkins_ssh']) {
                    sh '''
                    echo "🗂️ Copying files to remote..."
                    rsync -avz --delete --ignore-errors --exclude=.git --exclude=*.sock -e "ssh -o StrictHostKeyChecking=no" ./ ubuntu@10.0.1.126:/home/ubuntu/app

                    '''

                }
            }
        }

        stage('Cleaning build..') {
            steps {
                sshagent(credentials: ['Jenkins_ssh']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@10.0.1.126 <<EOF
                    echo "✅ Connected to remote server"

                    # Navigate to app folder
                    cd /home/ubuntu/app

                    # Stop and remove containers safely
                    docker stop django-app || true
                    docker rm django-app || true
                    docker stop nginx-proxy || true
                    docker rm nginx-proxy || true

                    # Deploy fresh containers
                    docker compose down || true
                    docker compose up -d --build

                    echo "✅ Deployment complete"
                    EOF
                    """
                }
            }
        }

    
    }

    post {
        failure {
            echo "Deployment failed."
        }
        success {
            echo "Deployment completed successfully."
        }
    }
}

