
pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REPOSITORY = '772498066230.dkr.ecr.ap-south-1.amazonaws.com/student-service'
        IMAGE_NAME = 'student-service:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/shreyashhiwale22/cloud-cicd-lab.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Test Flask App') {
            steps {
                sh '''
                    docker rm -f student-service-test 2>/dev/null || true
                    docker run -d --name student-service-test \
                        -p 5001:5000 student-service:latest

                    sleep 5
                    curl -f http://localhost:5001/
                    curl -f http://localhost:5001/student
                '''
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-ecr-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        set +x
                        export AWS_DEFAULT_REGION="$AWS_REGION"
                        aws ecr get-login-password --region "$AWS_REGION" |
                        docker login --username AWS --password-stdin \
                            772498066230.dkr.ecr.ap-south-1.amazonaws.com
                    '''
                }
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh '''
                    docker tag "$IMAGE_NAME" "$ECR_REPOSITORY:latest"
                    docker push "$ECR_REPOSITORY:latest"
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker rm -f student-service 2>/dev/null || true
                    docker run -d --restart unless-stopped \
                        --name student-service \
                        -p 5000:5000 student-service:latest
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded: Flask app built, tested, pushed to ECR, and deployed!'
        }
        always {
            sh 'docker rm -f student-service-test 2>/dev/null || true'
        }
    }
}
