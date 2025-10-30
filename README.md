# **CI/CD Pipeline for Flask Application using Jenkins, Docker, SonarQube, and Kubernetes**

## **1. Project Overview**
This project implements a **Continuous Integration and Continuous Deployment (CI/CD)** pipeline for a Flask application using Jenkins.  
The pipeline automates:
- Cloning from GitHub
- Building & pushing Docker images
- Running SonarQube analysis
- Deploying to Kubernetes

## **2. Technologies Used**
| Tool | Purpose |
|------|----------|
| Jenkins | CI/CD Automation |
| GitHub | Source Code Management |
| Docker | Containerization |
| Docker Hub | Container Registry |
| SonarQube | Code Quality Analysis |
| Kubernetes | Deployment & Scaling |
| Flask | Web Application Framework |

## **3. Jenkins Setup**

### **3.1 Install Jenkins**
https://www.jenkins.io/doc/book/installing/linux/
```
Access Jenkins: `http://<EC2-IP>:8080`
```

### **3.2 Install Docker**
Follow: https://docs.docker.com/engine/install/ubuntu/

### **3.2.1 Install Docker Compose**
Follow: https://docs.docker.com/compose/install/linux/

### **3.3 Install SonarQube with Docker Compose**
```yaml
version: "3.9"
services:
  sonarqube:
    image: sonarqube:latest
    ports:
      - "9000:9000"
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://db:5432/sonarqube
      SONAR_JDBC_USERNAME: sonarqube
      SONAR_JDBC_PASSWORD: sonarpass
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: sonarqube
      POSTGRES_PASSWORD: sonarpass
      POSTGRES_DB: sonarqube
```

### **3.4 Initialize Kubernetes Cluster**
Follow: https://github.com/aneeshravikumar2002-eng/Kubeadm-Installation-Guide.git

## **4. Jenkins Plugin Installation**
| Plugin | Purpose |
|---------|----------|
| Git Plugin | Clone Repos |
| Docker Pipeline | Docker Builds |
| Kubernetes CLI Plugin | Kubectl Integration |
| SonarQube Scanner Plugin | Code Analysis |
| Maven | Java Builds |

## **5. Jenkins Credentials Setup**
Go to: `Manage Jenkins → Credentials → System → Global credentials`

### **5.1 DockerHub Credentials**
| Field | Value |
|--------|--------|
| Kind | Username with password |
| ID | dockerhub-login |

**Steps:**
- Click Add Credentials
- In the form:
  - Kind: Username with password
  - Scope: Global (for all pipelines)
  - Username: Your Docker Hub username
  - Password: Your Docker Hub password or access token
  - ID: dockerhub-login
  - Description: Docker Hub credentials for image push
- Click Create

**Used in Jenkinsfile:**
```groovy
withCredentials([usernamePassword(credentialsId: 'dockerhub-login', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
  sh 'echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin'
}
```

### **5.2 Kubernetes Credential (kubeconfig)**
**Steps:**
- On your local machine or control node, locate your kubeconfig file:
  ```bash
  cat /etc/kubernetes/admin/config > kubeconfig
  ```
  Using MobaXterm download the file to your local machine.
- In Jenkins, click Add Credentials again.
- Fill out the form:
  - Kind: Secret file
  - Scope: Global
  - File: Upload your config file
  - ID: kubeconfig
  - Description: Kubernetes cluster configuration
- Click Create

**Used in Jenkinsfile:**
```groovy
withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
    sh '''
        kubectl --kubeconfig=$KUBECONFIG apply -f k8s/deployment.yml
    '''
}
```

### **5.3 SonarQube Token**
**Generate token in SonarQube → My Account → Security → Generate User level Token**  
Add in Jenkins as **Secret text** with ID `sonarqube-token`.

**Steps:**
- In SonarQube:
  - Open SonarQube in your browser (`http://<EC2-IP>:9000`)
  - Log in as admin (default password: admin)
  - Go to *My Account → Security → Generate Token*
  - Name it (e.g., jenkins-token)
  - Copy the token — this is shown only once!
- In Jenkins:
  - Go to *Manage Jenkins → Credentials → System → Global credentials*
  - Click *Add Credentials*
  - Fill in:
    - Kind: Secret text
    - Scope: Global
    - Secret: Paste your SonarQube token
    - ID: sonarqube-token
    - Description: Token for SonarQube server
  - Click Create

**Configure Jenkins with SonarQube Server:**
- Go to *Manage Jenkins → Configure System*
- Scroll to *SonarQube servers*
- Click *Add SonarQube*
- Fill:
  - Name: My SonarQube Server
  - Server URL: `http://<EC2-IP>:9000`
  - Server authentication token: choose the token credential you just added (sonarqube-token)
- Click Apply and Save

**Used in Jenkinsfile:**
```groovy
withSonarQubeEnv('My SonarQube Server') {
    sh """
        ${scannerHome}/bin/sonar-scanner \
        -Dsonar.projectKey=python \
        -Dsonar.projectName='python' \
        -Dsonar.sources=.
    """
}
```
Click Apply → Save. Then Click Build.

## **6. Create Jenkins Pipeline Job (Build Remotely)**

### **6.1 Create New Pipeline Job**
`Jenkins Dashboard → New Item → Pipeline`

### **6.2 Build Triggers**
Select **Build when a remote trigger is invoked**  
Set token: `flaskbuildtoken123`

### **6.3 Script Source**
**Option 1 (Recommended):** Pipeline script from SCM
```
SCM: Git
Repo URL: https://github.com/aneeshravikumar2002-eng/python.git
Branch: */main
Script Path: Jenkinsfile
```

### **6.4 Verify**
Check console for:
- Git clone
- Docker image built
- SonarQube analysis
- Kubernetes deployed

## **Final Result**
You now have a **complete CI/CD pipeline** deploying Flask app via Jenkins, Docker, SonarQube, and Kubernetes.





