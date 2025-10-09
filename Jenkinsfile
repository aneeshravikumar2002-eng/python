pipeline {
    agent any

    environment {
        IMAGE_NAME = "aneesh292002/beautiful-flask-app"
        CONTAINER_NAME = "beautiful-flask-container"
        BUILD_TAG = "build-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Checking out repository..."
                git branch: 'master', url: 'https://github.com/aneeshravikumar2002-eng/python.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh "docker build -t $IMAGE_NAME:$BUILD_TAG -t $IMAGE_NAME:latest ."
            }
        }

        stage('Run Docker Container') {
            steps {
                echo "Running Docker container..."
                sh """
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true
                    docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME:latest
                """
            }
        }

        stage('Test Application') {
            steps {
                echo "Testing application..."
                sh """
                    sleep 10
                    curl -f http://localhost:5000
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Pushing image to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-login', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh """
                        echo "$DOCKERHUB_PASS" | docker login -u aneesh292002
                        docker push $IMAGE_NAME:$BUILD_TAG
                        docker push $IMAGE_NAME:latest
                        docker logout
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Build succeeded. Cleaning up..."
            node('any') {
                sh 'docker system prune -f'
            }
        }
        failure {
            echo "Build failed. Keeping Docker artifacts for debugging."
        }
    }
}

