pipeline {
    agent any

    environment {
        DOCKERHUB_USER = credentials('dockerhub-login')
    }

    stages {
        stage('Git Clone') {
            steps {
                echo 'Checking out repository...'
                git 'https://github.com/aneeshravikumar2002-eng/python.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('My SonarQube Server') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                              -Dsonar.projectKey=python \
                              -Dsonar.projectName=python \
                              -Dsonar.sources=.
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh """
                    docker build -t aneesh292002/beautiful-flask-app:${BUILD_NUMBER} \
                                 -t aneesh292002/beautiful-flask-app:latest .
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-login', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh """
                        echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker push aneesh292002/beautiful-flask-app:${BUILD_NUMBER}
                        docker push aneesh292002/beautiful-flask-app:latest
                        docker logout
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes...'
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh """
                        kubectl --kubeconfig=$KUBECONFIG apply -f k8s/deployment.yml
                        kubectl --kubeconfig=$KUBECONFIG apply -f k8s/service.yml
                        kubectl --kubeconfig=$KUBECONFIG rollout status deployment/beautiful-flask-deployment
                    """
                }
            }
        }
    }

    post {
        failure {
            echo 'Build failed. Keeping Docker artifacts for debugging.'
        }
    }
}
