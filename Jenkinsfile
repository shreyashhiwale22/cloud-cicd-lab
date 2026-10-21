
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/shreyashhiwale22/cloud-cicd-lab.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t student-service:latest .'
            }
        }

        stage('Test Flask App') {
            steps {
                sh '''
                    docker run -d --name student-service-test -p 5000:5000 student-service:latest
                    sleep 5
                    curl -f http://localhost:5000/
                    curl -f http://localhost:5000/student
                    docker rm -f student-service-test
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker rm -f student-service || true
                    docker run -d --restart unless-stopped --name student-service -p 5000:5000 student-service:latest
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded: Flask application deployed!'
        }
        always {
            sh 'docker rm -f student-service-test 2>/dev/null || true'
        }
    }
}
