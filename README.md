# Campus Lost & Found — Cloud Computing Project Log

> **Course:** Cloud Computing  
> **Group Members:**
> 1. **Prushti Alpeshbhai Ladani**
> 2. **Jeetkumar Damodar Kaneriya**  
> **Repository:** [https://github.com/PrushtiLadani12/campus-lost-and-found](https://github.com/PrushtiLadani12/campus-lost-and-found)  
> **Live Demo URL:** [http://13.53.117.78](http://13.53.117.78)  
> **Health Check Endpoint:** [http://13.53.117.78/healthz](http://13.53.117.78/healthz)  
> **API Cloud Status:** [http://13.53.117.78/api/cloud-status](http://13.53.117.78/api/cloud-status)  

---

## 📌 Project Overview
A cloud-native lost and found portal for university campuses. Built to demonstrate key cloud computing paradigms: IaaS virtual machines, OCI containerization, object storage decoupling, container orchestration, managed relational databases, and serverless event-driven notifications.

---

## 🚀 Quick Start (Run Locally in Docker)

```bash
cd campus-lost-and-found
docker compose up --build
```
- Web Portal: `http://localhost:80`
- REST API / Swagger: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/healthz`

---

## 📅 Weekly Project Log & Contributions

### Week 1 (Session 1): Problem Formulation & Cloud Models
- **What we built:** Architecture sketch, user personas, and cloud model analysis (IaaS vs. PaaS vs. SaaS).
- **Why:** Evaluated on-premise vs. public cloud tradeoffs. Chose public cloud (free tier) due to unpredictable student load spikes around exams.
- **Contributions:**
  - *Prushti:* Drafted problem statement, user workflows, and cloud service model breakdown (IaaS, PaaS, SaaS).
  - *Jeetkumar:* Created initial cloud architecture sketch and deployment model analysis.

### Week 2 (Session 2): Cloud Virtual Machine & Network Perimeter
- **What we built:** Provisioned an AWS EC2 `t3.micro` Ubuntu instance running an Nginx reverse proxy.
- **Why:** To demonstrate IaaS host provisioning, OS configuration, and ingress security.
- **Firewall & Security Rules:**
  - Port 80/443 open to `0.0.0.0/0` (public web traffic).
  - Port 22 (SSH) strictly restricted to group members' IP addresses (`/32`).
- **Contributions:**
  - *Prushti:* Configured security groups, VPC routing, and SSH key pair hardening.
  - *Jeetkumar:* Deployed Ubuntu instance, configured Nginx reverse proxy and firewall rules.

### Week 3 (Session 3): Containerization with Docker
- **What we built:** Dockerfiles for `frontend` and `api-service`, plus a `docker-compose.yml` for unified local execution.
- **Why:** Eliminates the "works on my machine" issue and provides reproducible, immutable deployment units.
- **Contributions:**
  - *Prushti:* Containerized the backend API service and tested multi-stage build optimization.
  - *Jeetkumar:* Containerized the web UI and wrote the root `docker-compose.yml` configuration.

### Week 4 (Session 4): Decoupled Storage & Ingress
- **What we built:** Integrated cloud object storage (AWS S3) for photo uploads and connected DNS/public IP.
- **Why:** Preserves statelessness in containers. Storing uploaded images on container file systems leads to data loss upon container replacement or scaling.
- **Contributions:**
  - *Prushti:* Implemented S3 image upload and presigned URL retrieval in API.
  - *Jeetkumar:* Configured S3 bucket security policies, CORS rules, and VM public IP routing.

### Week 5 (Session 5): Orchestration
- **What we built:** Deployed containers using a managed container platform (AWS ECS / Cloud Run / k3s).
- **Why:** Automates process restarts, health monitoring, and scaling without manual Docker CLI intervention.
- **Contributions:**
  - *Prushti:* Authored container task definitions and container health check endpoints.
  - *Jeetkumar:* Configured auto-recovery, container resource limits, and ingress routing.

### Week 6–7 (Sessions 6 & 7): Managed Database & Serverless Events
- **What we built:**
  1. Migrated database to Amazon RDS PostgreSQL (db.t3.micro).
  2. Implemented an event-driven AWS Lambda function triggered on image upload to S3.
- **Why:** Offloads database patch management, replication, and automated backups. The Lambda function decouples image thumbnail generation and notification processing from the user-facing web request thread.
- **Contributions:**
  - *Prushti:* Provisioned RDS managed database, configured private subnet and database schema.
  - *Jeetkumar:* Wrote the serverless Lambda function for S3 upload events and keyword matching.

### Week 8 (Session 8): Security Audit, Secrets & Cost Analysis
- **What we built:** Hardened IAM roles, moved database credentials to Secrets Manager / Parameter Store, and set up billing alarms.
- **Why:** Prepares the system for production-readiness review and prevents accidental cloud overages.
- **Contributions:**
  - *Prushti:* Performed the security audit, least-privilege IAM review, and secret parameter isolation.
  - *Jeetkumar:* Developed the 100 vs. 10,000 user monthly cost model, configured \$1.00 budget alerts, and finalized the end-to-end demo.

---

## 🛠️ Tech Stack Summary
- **Cloud Provider:** AWS (Free Tier)
- **IaaS:** EC2 `t3.micro` Ubuntu 26.04 (Reverse Proxy, TLS termination)
- **PaaS / Containers:** Docker, Docker Compose, Nginx Gateway, FastAPI
- **Storage:** Amazon S3 (Decoupled Object Storage) + Amazon RDS PostgreSQL
- **Serverless / Event-Driven:** AWS Lambda (S3 trigger) + Amazon SES (Email alerts)
- **Security:** Security Groups, AWS Budgets ($1.00 Alert), Environment Secrets Isolation
