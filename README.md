# 🚀 End-to-End MLOps Pipeline with Monitoring (CI/CD + AWS + Prometheus + Grafana)

## 📌 Overview

This project demonstrates a complete **production-grade MLOps pipeline** that covers:

* Data versioning using DVC
* Experiment tracking with MLflow + DagsHub
* CI/CD using GitHub Actions
* Containerization with Docker
* Deployment on AWS EC2 via ECR
* Real-time monitoring using Prometheus
* Visualization using Grafana

---

## 🏗️ Architecture

```
GitHub → CI/CD → Docker → AWS ECR → EC2 (Flask App)
                                   ↓
                              /metrics
                                   ↓
                             Prometheus
                                   ↓
                              Grafana 📊
```

---

## ⚙️ Tech Stack

* **ML & Tracking:** MLflow, DVC, DagsHub
* **Backend:** Flask
* **CI/CD:** GitHub Actions
* **Containerization:** Docker
* **Cloud:** AWS (EC2, ECR, S3)
* **Monitoring:** Prometheus, Grafana

---

## 🔁 Pipeline Workflow

### 1. Data & Model Pipeline

* Data ingestion → preprocessing → feature engineering
* Model training & evaluation
* Metrics logged using MLflow
* Data & artifacts versioned using DVC

---

### 2. CI/CD Pipeline

* Triggered on every GitHub push
* Runs DVC pipeline
* Executes unit tests
* Builds Docker image
* Pushes image to AWS ECR

---

### 3. Deployment

* EC2 instance hosts Flask app
* Docker container runs the model API
* Application exposed on port `5000`

---

### 4. Monitoring

* Flask exposes `/metrics` endpoint
* Prometheus scrapes metrics every 15s
* Grafana visualizes metrics via dashboards

---

## 🚀 Deployment Steps

### 🔹 Run Application on EC2

```bash
docker run -d -p 5000:5000 --name flask-app <ECR-IMAGE>
```

Access:

```
http://<EC2-IP>:5000
```

---

### 🔹 Run Prometheus

```bash
docker run -d \
  -p 9090:9090 \
  --name prometheus \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

Access:

```
http://<PROMETHEUS-IP>:9090
```

---

### 🔹 Run Grafana

```bash
docker run -d -p 3001:3000 --name grafana grafana/grafana
```

Access:

```
http://<PROMETHEUS-IP>:3001
```

---

## 📊 Monitoring Dashboard

### Metrics Tracked:

* `app_request_count_total` → API usage
* `model_prediction_count_total` → prediction distribution
* `app_request_latency_seconds` → latency tracking

---

## 🔐 Security Configuration

* Flask EC2 → allows access only from Prometheus
* Prometheus EC2 → exposes ports 9090 & 3001
* AWS IAM roles used for secure ECR access

---

## 📈 Key Features

* ✅ End-to-end automated ML pipeline
* ✅ Model versioning & experiment tracking
* ✅ CI/CD with automated deployment
* ✅ Dockerized microservice architecture
* ✅ Real-time monitoring system
* ✅ Cloud-native deployment

---

## 💡 Key Learnings

* Building production ML pipelines
* Debugging CI/CD workflows
* Docker + AWS integration
* Monitoring real-world ML systems
* Observability using Prometheus & Grafana

---

## 🧠 Future Improvements

* Add Gunicorn + Nginx (production server)
* Add alerting (Slack/Email) 🚨
* Use Docker Compose for orchestration
* Deploy using Kubernetes (EKS)

---

## 🙌 Author

**Chinu (AI Engineer)**

* Passionate about building real-world ML systems
* Focused on MLOps, GenAI, and scalable AI systems

---
** check projectflow_updated.txt for detail flow of project 
