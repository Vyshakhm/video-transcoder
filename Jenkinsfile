stage('Build & Deploy') {
     steps {
            sh '''
                echo "Tearing down old containers..."
                docker-compose down --remove-orphans

                echo "Rebuilding and starting fresh containers..."
                docker-compose up -d --build
             '''
        }
    }
