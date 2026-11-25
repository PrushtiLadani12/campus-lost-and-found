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

### Week 5 (Session 5): Orchestration & High Availability Failover
- **What we built:** Deployed replicated container microservices (`backend1` and `backend2`) behind an Nginx upstream reverse-proxy load balancer with automated health failover (`proxy_next_upstream`) and Docker `restart: always`.
- **Why:** Automates process restarts, health monitoring, and scaling. Demonstrated self-healing by stopping one container live while the service survived with zero downtime.
- **Contributions:**
  - *Prushti:* Authored container task definitions and container health check endpoints (`/healthz`).
  - *Jeetkumar:* Configured Nginx upstream load balancing, auto-recovery, and live container kill testing.

### Week 6–7 (Sessions 6 & 7): Managed Database, RPO/RTO & Serverless Events
- **What we built:**
  1. Configured managed database schema with automated snapshots:
     - **RPO (Recovery Point Objective):** 1 hour (hourly automated snapshot).
     - **RTO (Recovery Time Objective):** 15 minutes (re-provisioning from snapshot).
     - **Replica vs. Backup:** Replicas provide real-time high availability; backups protect against data corruption and human error (`DROP TABLE`).
  2. Implemented event-driven AWS Lambda pipeline triggered on S3 image upload with **retries (exponential backoff)** and **idempotency** (deduplication via unique item UUIDs).
- **Contributions:**
  - *Prushti:* Provisioned RDS database architecture, RPO/RTO planning, and replica vs. backup documentation.
  - *Jeetkumar:* Designed the idempotent serverless Lambda handler with retry mechanisms for S3 upload events.

### Week 8 (Session 8): Security Audit, Secrets & Hidden Cost Analysis
- **What we built:** Hardened IAM roles, moved database credentials to Secrets Manager / Parameter Store, and performed a comprehensive cost model including **hidden cloud costs** (outbound data egress, NAT gateway idle fees, and orphaned EBS volumes).
- **Contributions:**
  - *Prushti:* Conducted the security audit, least-privilege IAM review, and secret parameter isolation.
  - *Jeetkumar:* Modeled the 100 vs. 10,000 user monthly costs, identified hidden cloud charges, and configured \$1.00 budget alerts.

---

## 🛠️ Tech Stack Summary
- **Cloud Provider:** AWS (Free Tier)
- **IaaS:** EC2 `t3.micro` Ubuntu 26.04 (Reverse Proxy, TLS termination)
- **PaaS / Containers:** Docker, Docker Compose, Nginx Gateway, FastAPI
- **Storage:** Amazon S3 (Decoupled Object Storage) + Amazon RDS PostgreSQL
- **Serverless / Event-Driven:** AWS Lambda (S3 trigger) + Amazon SES (Email alerts)
- **Security:** Security Groups, AWS Budgets ($1.00 Alert), Environment Secrets Isolation
