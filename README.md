# 📌 Project Purpose

The purpose of this project is to design and deploy a scalable cloud-based web application architecture using Google Cloud Platform (GCP) services. 
The system consists of a backend served on a Virtual Machine (VM), a frontend deployed on a Kubernetes cluster, and a serverless function to demonstrate flexibility and integration of cloud-native components.

Through this project, the goal is to:
* Understand and implement core concepts of cloud computing architectures.
* Build a containerized frontend and deploy it using Google Kubernetes Engine (GKE).
* Deploy a backend service on a VM instance with proper firewall and accessibility settings.
* Integrate serverless functions for lightweight operations.
* Evaluate the scalability and performance of the system using load testing tools such as Locust.
* Analyze how system configurations (e.g., number of users, ramp-up rate, pod count) impact performance metrics and resource utilization.


## Backend Setup

### 1. Create a VM Instance
Create a VM instance on **Google Cloud Platform (GCP)** using an image like **Ubuntu 22.04 LTS**.

### 2. Install Required Libraries

Open your terminal and run the following commands:

```bash
sudo apt update
sudo apt install
python3-pip python3-venv -y
source venv/bin/activate
pip install fastapi uvicorn
clone the code via github url and go to backend directory
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 5000
```
### 3. Add firewall rule to the VM 

```bash
* Name: allow-backend-port
* Targets: All instances in the network
* Protocols: TCP 5000
* Source IP: 0.0.0.0/0 
```
### 4. Check if it works
* get the external ip of your VM instance
* go to:
```bash
http://<YOUR_EXTERNAL_VM_IP>:<5000/process
```

## Frontend Setup
### 1. Created a cluster
```bash
* gcloud services enable container.googleapis.com
* gcloud container clusters create YOUR_CLUSTER_NAME --num-nodes=1 --zone=us-central1-a
```

### 2. Go to the project frontend folder and run 
```bash
* npm run build
```

### 3. Add some artifacts
```bash
* gcloud artifacts repositories create ARTIFACT_NAME --repository-format=docker --location=us-central1
```

### 4. Build & push docker image for frontend
```bash
* docker build -t us-central1-docker.pkg.dev/YOUR_GCP_PROJECT_ID/ARTIFACT_NAME/IMAGE_NAME:latest .
* docker push us-central1-docker.pkg.dev/YOUR_GCP_PROJECT_ID/ARTIFACT_NAME/IMAGE_NAME:latest
```

### 5. Deploy frontend to kubernates cluster
```bash
* gcloud container clusters get-credentials YOUR_CLUSTER_NAME --zone=us-central1-a
```

### 6. Update react-deployment file with your image name and run the following commands:
```bash
* kubectl apply -f react-deployment.yaml
* kubectl get services 
 ```
### 7. Go to the following url to check the system
```bash
http://<YOUR_CLUSTER_IP>:30036
```


## Serverless function
* In the github repository there is a file named as serverless.
* The serverless function is written there.
* You can change it if you want.
* To implement the serverless function in GCP, these are the steps that needed to be followed:
* ```bash
  * functions deploy NAME_OF_THE_FUNCTION --runtime python311 –trigger region us-central1
  ```
* use the URL that GCP returnes and add it to the frontend app.js file where the fecth operation occurs for the serverless function
* ![image](https://github.com/user-attachments/assets/2b54180c-75d0-4a30-8b76-19f3d91b721f)


  
