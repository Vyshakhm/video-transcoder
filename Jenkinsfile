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
                    echo 🗂️ Copying source files to remote server...
                    rsync -avz --delete -e "ssh -o StrictHostKeyChecking=no" ./ $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH
                    '''
                }
            }
        }

        stage('Cleaning build..') {
            steps {
                sshagent(credentials: ['Jenkins_ssh']) {
                    sh '''
                    echo 🚀 Cleaning old build...
                    ssh -o StrictHostKeyChecking=no $REMOTE_USER@$REMOTE_HOST << EOF
                        cd $REMOTE_PATH
                        docker compose down || true
                        docker rm -f django-app || true
                        docker rm -f nginx-proxy || true
                        docker network prune -f || true
                    EOF
                    '''
                }
            }
        }

        stage('Cleaning build..') {
            steps {
                sshagent(credentials: ['Jenkins_ssh']) {
                    sh '''
                echo 🚀 Deploying on remote server...
                ssh -o StrictHostKeyChecking=no $REMOTE_USER@$REMOTE_HOST << EOF
                    docker compose build
                    docker compose up -d
                EOF
                '''
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
}
