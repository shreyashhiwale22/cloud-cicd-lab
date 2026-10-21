
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
                    docker run -d --name student-service-test student-service:latest
                    sleep 3

                    docker exec student-service-test python -c \
                    "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/').read().decode())"

                    docker exec student-service-test python -c \
                    "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/student').read().decode())"
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
                docker run --rm \
                    -e AWS_ACCESS_KEY_ID \
                    -e AWS_SECRET_ACCESS_KEY \
                    -e AWS_DEFAULT_REGION="$AWS_REGION" \
                    amazon/aws-cli:latest \
                    ecr get-login-password \
                    --region "$AWS_REGION" |
                docker login \
                    --username AWS \
                    --password-stdin \
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
