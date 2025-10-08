pipeline {
  agent { label 'slave3' }

  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub')
    IMAGE_NAME = "aneesh292002/weekdays-docker"
  }

  stages {

    stage('Git Clone') {
      steps {
        git 'https://github.com/aneeshravikumar2002-eng/python.git'
      }
    }

    stage('Build App') {
      steps {
        echo "Building the application..."
        sh 'bin/build .'
      }
    }

    stage('Docker Login') {
      steps {
        echo "Logging in to Docker Hub..."
        sh '''
          echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
        '''
      }
    }

    stage('Build & Tag Image') {
      steps {
        script {
          def tag = "demo-java-${env.BUILD_NUMBER}"
          sh """
            docker build -t ${IMAGE_NAME}:${tag} .
            docker tag ${IMAGE_NAME}:${tag} ${IMAGE_NAME}:latest
          """
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          def tag = "demo-java-${env.BUILD_NUMBER}"
          sh """
            docker push ${IMAGE_NAME}:${tag}
            docker push ${IMAGE_NAME}:latest
          """
        }
      }
    }
  }

  post {
    always {
      echo "Cleaning up and logging out..."
      sh 'docker logout || true'
    }
  }
}
