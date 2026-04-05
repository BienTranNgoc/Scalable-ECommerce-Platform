# Scalable E-Commerce Platform

![Architecture Diagram](docs/architecture.png)

## 🚀 Overview

This project implements a **scalable, production-ready e-commerce platform** using a **microservices architecture**. The platform is designed to handle high traffic loads with enterprise-grade observability, security, and reliability features.

### Key Features

- **Microservices Architecture**: 5 core services (User, Product, Cart, Order, Payment)
- **Event-Driven**: Apache Kafka for inter-service communication
- **Observability Stack**:
  - **Metrics**: Prometheus + Grafana
  - **Tracing**: Jaeger (OpenTelemetry)
  - **Logging**: OpenSearch + Logstash
- **API Gateway**: Kong with Admin UI
- **Service Discovery**: HashiCorp Consul
- **Databases**: PostgreSQL, MongoDB, Redis
- **Security**:
  - JWT Authentication
  - RBAC (Role-Based Access Control)
  - HTTPS with TLS Certificates
- **Infrastructure**:
  - Docker Compose for local development
  - Kubernetes-ready (Helm charts available)
  - CI/CD pipeline (GitHub Actions)

## 🛠️ Tech Stack

### Application Layer

| Layer | Technology | Purpose |
|-------|------------|---------|
| **API Gateway** | Kong | Reverse proxy, authentication, rate limiting |
| **Service Discovery** | Consul | Service registration and discovery |
| **Message Broker** | Apache Kafka | Asynchronous communication |
| **Databases** | PostgreSQL, MongoDB, Redis | Relational, NoSQL, Caching |
| **Authentication** | JWT + bcrypt | Secure user authentication |
| **Authorization** | RBAC | Role-based access control |
| **Notifications** | WebSocket | Real-time updates |

### Observability Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Metrics** | Prometheus | Time-series metrics collection |
| **Visualization** | Grafana | Dashboards and alerting |
| **Tracing** | Jaeger | Distributed tracing |
| **Logging** | OpenSearch | Centralized logging |
| **Log Shipper** | Logstash | Log processing and forwarding |
| **Collector** | OpenTelemetry Collector | Data collection and processing |

### Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Containerization** | Docker | Container management |
| **Orchestration** | Kubernetes | Cluster management |
| **CI/CD** | GitHub Actions | Automated pipelines |
| **Infrastructure as Code** | Terraform | Cloud resource management |
| **Configuration** | Helm | Kubernetes package management |

## 📂 Project Structure

```
Scalable-ECommerce-Platform/
├── services/                # Microservices
│   ├── user-service/
│   ├── product-service/
│   ├── cart-service/
│   ├── order-service/
│   ├── payment-service/
│   └── common/
├── infrastructure/          # Infrastructure components
│   ├── postgres/
│   ├── mongodb/
│   ├── redis/
│   ├── kafka/
│   ├── opensearch/
│   ├── grafana/
│   ├── jaeger/
│   ├── kong/
│   ├── consul/
│   └── otel/
├── k8s/                     # Kubernetes manifests
│   ├── base/
│   ├── overlays/
│   └── helm/
├── terraform/               # Terraform configurations
├── .github/workflows/       # GitHub Actions CI/CD
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
└── .env.example             # Environment variables template
```

## 🏗️ Architecture

### Service Communication

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            CLIENTS                                          │
│  Web App  |  Mobile App  |  3rd Party  |  Admin Dashboard                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            KONG API GATEWAY                                 │
│  Authentication | Rate Limiting | Load Balancing | SSL Termination          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌─────────────────────────┴─────────────────────────┐
        ▼                                                   ▼
┌──────────────────────┐                        ┌────────────────────────┐
│  USER SERVICE        │                        │  PRODUCT SERVICE       │
│  PostgreSQL          │                        │  MongoDB               │
└──────────────────────┘                        └────────────────────────┘
        │                                                   │
        └──────────────┐     ┌────────────────────────────┘
                       ▼     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       APACHE KAFKA                                          │
│  user-created | product-viewed | order-placed | payment-processed          │
└─────────────────────────────────────────────────────────────────────────────┘
        │                                                   │
        ▼                                                   ▼
┌──────────────────────┐                        ┌────────────────────────┐
│  CART SERVICE        │                        │  ORDER SERVICE         │
│  Redis               │                        │  PostgreSQL            │
└──────────────────────┘                        └────────────────────────┘
                                    │
                                    ▼
                        ┌────────────────────────┐
                        │  PAYMENT SERVICE       │
                        │  PostgreSQL            │
                        └────────────────────────┘
```

### Observability Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            APPLICATIONS                                     │
│  User Service | Product Service | Cart Service | Order Service | Payment Svc  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OPEN TELEMETRY COLLECTOR                                 │
│  (Receives: Traces, Metrics, Logs)                                          │
│  (Processes: Batching, Sampling, Enrichment)                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌─────────────────────────┴─────────────────────────┐
        ▼                                                   ▼
┌──────────────────────┐                        ┌────────────────────────┐
│  JAEGER              │                        │  PROMETHEUS            │
│  (Distributed Tracing) │                        │  (Metrics Collection)  │
└──────────────────────┘                        └────────────────────────┘
                                    │
                                    ▼
                        ┌────────────────────────┐
                        │  OPENSEARCH            │
                        │  (Logging & Analytics) │
                        └────────────────────────┘
```

## 🚀 Getting Started

### Prerequisites

- Docker Desktop (v20.10+)
- Docker Compose (v2)
- Git

### Installation

1. **Clone the repository**
```bash
cd /path/to/development
git clone https://github.com/yourusername/Scalable-ECommerce-Platform.git
cd Scalable-ECommerce-Platform
```

2. **Create environment file**
```bash
cp .env.example .env
```

3. **Configure environment variables**
Edit the `.env` file with your specific configurations:
```bash
# Database credentials
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=ecommerce_db

# JWT configuration
JWT_SECRET=your_jwt_secret
JWT_EXPIRES_IN=24h

# Redis configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Kafka configuration
KAFKA_BROKERS=kafka:9092

# OpenSearch configuration
OPENSEARCH_HOSTS=opensearch:9200

# Grafana admin password
GRAFANA_ADMIN_PASSWORD=admin
```

4. **Start the platform**
```bash
make up
```

### Access Points

After running `make up`, the following services will be available:

| Service | URL | Credentials |
|---------|-----|-------------|
| **API Gateway** | `http://localhost:8000` | - |
| **Kong Admin UI** | `http://localhost:8002` | - |
| **Consul UI** | `http://localhost:8500` | - |
| **Kafka UI** | `http://localhost:8080` | - |
| **OpenSearch Dashboards** | `http://localhost:5601` | - |
| **Grafana** | `http://localhost:3000` | admin / `GRAFANA_ADMIN_PASSWORD` |
| **Prometheus** | `http
