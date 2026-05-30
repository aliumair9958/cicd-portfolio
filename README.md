# 🚀 CI/CD Pipeline — Portfolio Project

> **End-to-end DevOps pipeline** built with Python · Flask · Docker · Kubernetes · Jenkins · GitHub Actions · AWS EC2 (Free Tier)

![CI](https://github.com/YOUR_USERNAME/cicd-portfolio/actions/workflows/ci.yml/badge.svg)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-deployed-326CE5?logo=kubernetes&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-pipeline-D24939?logo=jenkins&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)

---

## 📐 Architecture

```
Developer pushes code
        │
        ▼
  GitHub (source)
        │
        ├──► GitHub Actions (free CI — lint, syntax check, docker build test)
        │
        └──► Jenkins (on AWS EC2 Free Tier)
                  │
                  ├── 1. Checkout code
                  ├── 2. Run tests
                  ├── 3. Build Docker image
                  ├── 4. Push to Docker Hub
                  └── 5. Deploy to Kubernetes (Minikube)
                              │
                              └── 2 Pods running Flask app
                                  exposed via NodePort Service
```

---

## 🛠 Tech Stack

| Layer | Tool | Why |
|---|---|---|
| App | Python + Flask | Lightweight, easy to containerize |
| Containerization | Docker (multi-stage build) | Portable, reproducible builds |
| Orchestration | Kubernetes (Minikube) | Industry-standard, free locally |
| CI/CD | Jenkins + GitHub Actions | Dual pipeline — Jenkins for full deploy, GHA for free gate |
| Registry | Docker Hub | Free image hosting |
| Cloud | AWS EC2 t2.micro | Free Tier — 750 hrs/month |

---

## 📁 Project Structure

```
cicd-portfolio/
├── app/
│   ├── app.py              # Flask application
│   └── requirements.txt    # Python dependencies
├── k8s/
│   ├── deployment.yaml     # Kubernetes Deployment (2 replicas)
│   └── service.yaml        # Kubernetes Service (NodePort)
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions free CI
├── Dockerfile              # Multi-stage Docker build
├── Jenkinsfile             # Full Jenkins pipeline-as-code
└── README.md
```

---

## ⚙️ How to Run Locally (5 minutes)

### Prerequisites (all free)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) — local Kubernetes
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/cicd-portfolio.git
cd cicd-portfolio

# 2. Build and run with Docker only (quickest)
docker build -t cicd-portfolio .
docker run -p 5000:5000 cicd-portfolio
# Visit http://localhost:5000

# 3. OR deploy to local Kubernetes via Minikube
minikube start
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
minikube service cicd-app-service   # Opens in browser automatically
```

---

## 🔧 Jenkins Setup (on AWS EC2 Free Tier)

1. **Launch EC2** — t2.micro, Ubuntu 22.04, open ports 8080 (Jenkins) + 22 (SSH)
2. **Install Jenkins:**
   ```bash
   sudo apt update
   sudo apt install -y openjdk-17-jdk
   curl -fsSL https://pkg.jenkins.io/debian/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
   echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
   sudo apt update && sudo apt install -y jenkins
   sudo systemctl start jenkins
   ```
3. **Install Docker on EC2:**
   ```bash
   sudo apt install -y docker.io
   sudo usermod -aG docker jenkins
   sudo systemctl restart jenkins
   ```
4. **Create Pipeline job** in Jenkins → point to this GitHub repo → Jenkins auto-finds `Jenkinsfile`
5. **Add credentials** in Jenkins → Manage → Credentials → add Docker Hub username/password with ID `dockerhub-credentials`

---

## 🌐 API Endpoints

| Endpoint | Description | Response |
|---|---|---|
| `GET /` | Main dashboard | HTML page |
| `GET /health` | Health check (used by K8s probes) | `{"status": "healthy", ...}` |

---

## 💡 Key Concepts Demonstrated

- **Pipeline-as-Code** — entire pipeline lives in `Jenkinsfile`, versioned with the app
- **Multi-stage Docker build** — smaller, more secure final image
- **Non-root container user** — security best practice
- **Kubernetes health probes** — liveness + readiness checks for zero-downtime deploys
- **Rolling updates** — Kubernetes replaces pods gradually (no downtime)
- **Dual CI strategy** — GitHub Actions as fast gate, Jenkins as full deploy pipeline
- **Secrets management** — credentials stored in Jenkins, never in code

---

## 📸 Screenshots

> *(Add screenshots of your Jenkins pipeline, the running app, and `kubectl get pods` output here — recruiters love this!)*

---

## 👤 Author

**Your Name** — [LinkedIn](https://linkedin.com/in/yourprofile) · [GitHub](https://github.com/YOUR_USERNAME)

---

*This project was built to demonstrate end-to-end DevOps practices using 100% free tools and services.*
