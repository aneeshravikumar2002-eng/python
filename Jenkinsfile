pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'aneesh292002'
        IMAGE_NAME = 'beautiful-flask-app'
        IMAGE_TAG = 'latest'
        CONTAINER_NAME = 'beautiful-flask-container'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Cloning repository...'
                // Replace the URL with your GitHub repo
                git branch: 'master', url: 'https://github.com/aneeshravikumar2002-eng/python.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Run Docker Container') {
            steps {
                echo 'Running Docker container...'
                sh '''
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true
                    docker run -d --name $CONTAINER_NAME -p 5000:5000 $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Test Application') {
            steps {
                echo 'Testing application health...'
                // wait for Flask app to boot up
                sh 'sleep 5 && curl -f http://localhost:5000 || (echo "App did not start" && exit 1)'
            }
        }

        stage('Push to Docker Hub') {
            when {
                expression { return env.DOCKERHUB_USER != '' }
            }
            steps {
                echo 'Pushing image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push aneesh292002/beautiful-flask-app:latest
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'docker system prune -f'
        }
    }
}
