# Docker Deployment Guide for ProxmoxMCP

*Complete guide for deploying ProxmoxMCP using Docker containers in development, testing, and production environments.*

## Table of Contents

- [Quick Start](#quick-start)
- [Container Registry](#container-registry)
- [Configuration](#configuration)
- [Deployment Methods](#deployment-methods)
- [Security Configuration](#security-configuration)
- [Monitoring and Logging](#monitoring-and-logging)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Quick Start

### Prerequisites

- **Docker** 20.10+ or **Docker Desktop**
- **Docker Compose** 2.0+ (included with Docker Desktop)
- **Proxmox VE** server with API access
- **Valid Proxmox API token** (see [API Token Setup](#proxmox-api-token-setup))

### 1. Instant Deployment

```bash
# Option 1: Direct Docker run
docker run -d \
  --name proxmox-mcp \
  -v ./proxmox-config:/app/proxmox-config:ro \
  -v ./logs:/app/logs \
  -e PROXMOX_MCP_CONFIG=/app/proxmox-config/config.json \
  ghcr.io/basher83/proxmox-mcp:latest

# Option 2: Docker Compose (Recommended)
curl -o docker-compose.yml https://raw.githubusercontent.com/basher83/ProxmoxMCP/main/compose.yaml
docker compose up -d
```

### 2. Verify Deployment

```bash
# Check container status
docker ps | grep proxmox-mcp

# View logs
docker logs proxmox-mcp

# Check health
docker inspect proxmox-mcp | grep Health
```

---

## Container Registry

### Available Images

#### GitHub Container Registry (Primary)

```bash
# Latest stable release
ghcr.io/basher83/proxmox-mcp:latest

# Specific version (recommended for production)
ghcr.io/basher83/proxmox-mcp:v1.0.0

# Development builds
ghcr.io/basher83/proxmox-mcp:main

# Pre-release builds
ghcr.io/basher83/proxmox-mcp:v1.0.0-rc1
```

#### Multi-Architecture Support

```bash
# Multi-architecture manifest (automatic selection)
ghcr.io/basher83/proxmox-mcp:latest

# Specific architecture (if needed)
ghcr.io/basher83/proxmox-mcp:latest  # Multi-arch
docker pull --platform linux/amd64 ghcr.io/basher83/proxmox-mcp:latest
docker pull --platform linux/arm64 ghcr.io/basher83/proxmox-mcp:latest
```

### Image Information

#### Security and Verification

```bash
# Verify image signature (if available)
cosign verify ghcr.io/basher83/proxmox-mcp:latest

# Check image metadata
docker inspect ghcr.io/basher83/proxmox-mcp:latest

# View SBOM (Software Bill of Materials)
syft ghcr.io/basher83/proxmox-mcp:latest
```

#### Image Details

- **Base Image:** python:3.10-slim
- **User:** Non-root (appuser:appgroup)
- **Port:** None (stdio MCP server)
- **Volumes:** `/app/proxmox-config`, `/app/logs`
- **Size:** ~200MB (compressed)

---

## Configuration

### Proxmox API Token Setup

#### 1. Create API Token in Proxmox

```bash
# In Proxmox web interface:
# 1. Go to Datacenter → Permissions → API Tokens
# 2. Create new token with appropriate permissions
# 3. Note the Token ID and Secret
```

#### 2. Configuration File

```json
{
  "host": "your-proxmox-host.example.com",
  "port": 8006,
  "user": "your-user@pam",
  "token_name": "your-token-name",
  "token_value": "your-token-secret",
  "verify_ssl": true,
  "timeout": 30
}
```

### Container Configuration Methods

#### Method 1: Configuration File (Recommended)

```bash
# Create configuration directory
mkdir -p ./proxmox-config
cat > ./proxmox-config/config.json << EOF
{
  "host": "proxmox.example.com",
  "port": 8006,
  "user": "mcp-user@pam",
  "token_name": "mcp-token",
  "token_value": "your-secret-token",
  "verify_ssl": true,
  "timeout": 30
}
EOF

# Run container with mounted config
docker run -d \
  --name proxmox-mcp \
  -v ./proxmox-config:/app/proxmox-config:ro \
  -e PROXMOX_MCP_CONFIG=/app/proxmox-config/config.json \
  ghcr.io/basher83/proxmox-mcp:latest
```

#### Method 2: Environment Variables

```bash
# Run with environment variables
docker run -d \
  --name proxmox-mcp \
  -e PROXMOX_HOST="proxmox.example.com" \
  -e PROXMOX_PORT="8006" \
  -e PROXMOX_USER="mcp-user@pam" \
  -e PROXMOX_TOKEN_NAME="mcp-token" \
  -e PROXMOX_TOKEN_VALUE="your-secret-token" \
  -e PROXMOX_VERIFY_SSL="true" \
  ghcr.io/basher83/proxmox-mcp:latest
```

#### Method 3: Docker Secrets (Production)

```bash
# Create secrets
echo "your-secret-token" | docker secret create proxmox_token -

# Run with secrets
docker service create \
  --name proxmox-mcp \
  --secret proxmox_token \
  -e PROXMOX_TOKEN_FILE=/run/secrets/proxmox_token \
  ghcr.io/basher83/proxmox-mcp:latest
```

### Encrypted Configuration

#### Using Built-in Encryption

```bash
# Generate encryption key
docker run --rm ghcr.io/basher83/proxmox-mcp:latest \
  python -m proxmox_mcp.utils.encrypt_config --generate-key

# Encrypt configuration
docker run --rm \
  -v ./proxmox-config:/app/proxmox-config \
  ghcr.io/basher83/proxmox-mcp:latest \
  python -m proxmox_mcp.utils.encrypt_config \
  /app/proxmox-config/config.json

# Run with encrypted config
docker run -d \
  --name proxmox-mcp \
  -v ./proxmox-config:/app/proxmox-config:ro \
  -e PROXMOX_MCP_CONFIG=/app/proxmox-config/config.encrypted.json \
  -e PROXMOX_MCP_MASTER_KEY="your-encryption-key" \
  ghcr.io/basher83/proxmox-mcp:latest
```

---

## Deployment Methods

### Docker Compose (Recommended)

#### Basic Deployment

```yaml
# docker-compose.yml
version: '3.8'

services:
  proxmox-mcp:
    image: ghcr.io/basher83/proxmox-mcp:latest
    container_name: proxmox-mcp
    restart: unless-stopped
    init: true
    tty: true
    stdin_open: true
    stop_signal: SIGINT
    
    environment:
      PROXMOX_MCP_CONFIG: /app/proxmox-config/config.json
      PYTHONPATH: /app/src
      LOG_LEVEL: INFO
    
    volumes:
      - ./proxmox-config:/app/proxmox-config:ro
      - ./logs:/app/logs
      - /etc/localtime:/etc/localtime:ro  # Sync timezone
    
    healthcheck:
      test: ["CMD", "/app/health_check.sh"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    
    # Resource limits (adjust as needed)
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 128M
          cpus: '0.1'
```

#### Production Deployment with Monitoring

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  proxmox-mcp:
    image: ghcr.io/basher83/proxmox-mcp:v1.0.0  # Pin specific version
    container_name: proxmox-mcp
    restart: unless-stopped
    init: true
    
    environment:
      PROXMOX_MCP_CONFIG: /app/proxmox-config/config.encrypted.json
      PROXMOX_MCP_MASTER_KEY_FILE: /run/secrets/master_key
      LOG_LEVEL: WARNING
      LOG_FORMAT: json
    
    volumes:
      - proxmox-config:/app/proxmox-config:ro
      - proxmox-logs:/app/logs
    
    secrets:
      - master_key
    
    healthcheck:
      test: ["CMD", "/app/health_check.sh"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s
    
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "service=proxmox-mcp,environment=production"
    
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.2'
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3

secrets:
  master_key:
    file: ./secrets/master_key.txt

volumes:
  proxmox-config:
    driver: local
  proxmox-logs:
    driver: local
```

### Docker Swarm

#### Swarm Service Deployment

```bash
# Initialize swarm (if not already done)
docker swarm init

# Create secrets
echo "your-encryption-key" | docker secret create proxmox_master_key -

# Deploy service
docker service create \
  --name proxmox-mcp \
  --replicas 1 \
  --restart-condition on-failure \
  --restart-max-attempts 3 \
  --secret proxmox_master_key \
  --mount type=bind,source=/path/to/config,target=/app/proxmox-config,readonly \
  --env PROXMOX_MCP_CONFIG=/app/proxmox-config/config.encrypted.json \
  --env PROXMOX_MCP_MASTER_KEY_FILE=/run/secrets/proxmox_master_key \
  ghcr.io/basher83/proxmox-mcp:latest
```

#### Stack Deployment

```yaml
# proxmox-mcp-stack.yml
version: '3.8'

services:
  proxmox-mcp:
    image: ghcr.io/basher83/proxmox-mcp:latest
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 128M
          cpus: '0.1'
      labels:
        - traefik.enable=false  # No HTTP exposure needed
    
    environment:
      PROXMOX_MCP_CONFIG: /app/proxmox-config/config.json
    
    volumes:
      - proxmox-config:/app/proxmox-config:ro
      - proxmox-logs:/app/logs

volumes:
  proxmox-config:
    external: true
  proxmox-logs:
    external: true

# Deploy stack
# docker stack deploy -c proxmox-mcp-stack.yml proxmox
```

### Kubernetes

#### Basic Deployment

```yaml
# proxmox-mcp-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: proxmox-mcp
  labels:
    app: proxmox-mcp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: proxmox-mcp
  template:
    metadata:
      labels:
        app: proxmox-mcp
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 10001
      
      containers:
      - name: proxmox-mcp
        image: ghcr.io/basher83/proxmox-mcp:v1.0.0
        imagePullPolicy: IfNotPresent
        
        env:
        - name: PROXMOX_MCP_CONFIG
          value: "/app/config/config.json"
        - name: LOG_LEVEL
          value: "INFO"
        
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
        - name: logs
          mountPath: /app/logs
        
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        
        livenessProbe:
          exec:
            command:
            - /app/health_check.sh
          initialDelaySeconds: 10
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
        
        readinessProbe:
          exec:
            command:
            - /app/health_check.sh
          initialDelaySeconds: 5
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
      
      volumes:
      - name: config
        secret:
          secretName: proxmox-mcp-config
      - name: logs
        emptyDir: {}

---
apiVersion: v1
kind: Secret
metadata:
  name: proxmox-mcp-config
type: Opaque
stringData:
  config.json: |
    {
      "host": "proxmox.example.com",
      "port": 8006,
      "user": "mcp-user@pam",
      "token_name": "mcp-token",
      "token_value": "your-secret-token",
      "verify_ssl": true,
      "timeout": 30
    }
```

#### Production Kubernetes with Helm

```yaml
# values.yaml for Helm chart
replicaCount: 1

image:
  repository: ghcr.io/basher83/proxmox-mcp
  tag: "v1.0.0"
  pullPolicy: IfNotPresent

config:
  host: "proxmox.example.com"
  port: 8006
  user: "mcp-user@pam"
  verify_ssl: true
  timeout: 30

secretRefs:
  tokenName: proxmox-token-secret
  tokenKey: token_value

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

nodeSelector: {}
tolerations: []
affinity: {}

persistence:
  logs:
    enabled: true
    size: 1Gi
    storageClass: ""

monitoring:
  enabled: true
  serviceMonitor:
    enabled: true

# Install with Helm
# helm install proxmox-mcp ./helm-chart -f values.yaml
```

---

## Security Configuration

### Container Security

#### Security Hardening

```yaml
# Secure Docker Compose configuration
services:
  proxmox-mcp:
    image: ghcr.io/basher83/proxmox-mcp:latest
    
    # Security options
    security_opt:
      - no-new-privileges:true
    read_only: true
    cap_drop:
      - ALL
    user: "10001:10001"  # Non-root user
    
    # Temporary filesystems
    tmpfs:
      - /tmp:size=100m,noexec,nosuid,nodev
      - /var/tmp:size=50m,noexec,nosuid,nodev
    
    # Resource limits
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

#### Network Security

```yaml
services:
  proxmox-mcp:
    image: ghcr.io/basher83/proxmox-mcp:latest
    
    # Custom network for isolation
    networks:
      - proxmox-network
    
    # No port exposure (stdio MCP server)
    # ports: []  # Commented out - no ports needed

networks:
  proxmox-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/24
```

### Secrets Management

#### Docker Compose Secrets

```yaml
version: '3.8'

services:
  proxmox-mcp:
    image: ghcr.io/basher83/proxmox-mcp:latest
    
    environment:
      PROXMOX_MCP_CONFIG: /app/proxmox-config/config.json
      PROXMOX_TOKEN_VALUE_FILE: /run/secrets/proxmox_token
      PROXMOX_MCP_MASTER_KEY_FILE: /run/secrets/master_key
    
    secrets:
      - proxmox_token
      - master_key

secrets:
  proxmox_token:
    file: ./secrets/proxmox_token.txt
  master_key:
    file: ./secrets/master_key.txt
```

#### External Secret Management

```bash
# Using HashiCorp Vault
vault kv put secret/proxmox-mcp \
  token_value="your-secret-token" \
  master_key="your-encryption-key"

# Using environment file
cat > .env.secrets << EOF
PROXMOX_TOKEN_VALUE=your-secret-token
PROXMOX_MCP_MASTER_KEY=your-encryption-key
EOF

# Load from environment file
docker compose --env-file .env.secrets up -d
```

### SSL/TLS Configuration

#### Custom CA Certificates

```dockerfile
# Custom Dockerfile for custom CA
FROM ghcr.io/basher83/proxmox-mcp:latest

# Add custom CA certificates
COPY ca-certificates/ /usr/local/share/ca-certificates/
RUN update-ca-certificates

# Or mount certificates at runtime
# -v ./ca-certificates:/usr/local/share/ca-certificates:ro
```

#### SSL Configuration Options

```json
{
  "host": "proxmox.example.com",
  "port": 8006,
  "verify_ssl": true,
  "ssl_ca_cert": "/app/ssl/ca-cert.pem",
  "ssl_client_cert": "/app/ssl/client-cert.pem",
  "ssl_client_key": "/app/ssl/client-key.pem"
}
```

---

## Monitoring and Logging

### Health Monitoring

#### Container Health Checks

```bash
# Manual health check
docker exec proxmox-mcp /app/health_check.sh

# View health status
docker inspect proxmox-mcp | jq '.[0].State.Health'

# Health check logs
docker logs proxmox-mcp --details | grep health
```

#### Advanced Health Monitoring

```yaml
# Docker Compose with monitoring
version: '3.8'

services:
  proxmox-mcp:
    image: ghcr.io/basher83/proxmox-mcp:latest
    
    healthcheck:
      test: ["CMD", "/app/health_check.sh"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s
    
    # Add monitoring labels
    labels:
      - "monitoring.enable=true"
      - "monitoring.service=proxmox-mcp"
```

### Logging Configuration

#### Log Aggregation

```yaml
# ELK Stack integration
version: '3.8'

services:
  proxmox-mcp:
    image: ghcr.io/basher83/proxmox-mcp:latest
    
    logging:
      driver: "fluentd"
      options:
        fluentd-address: "localhost:24224"
        tag: "proxmox-mcp.{{.Name}}"
    
    environment:
      LOG_FORMAT: json
      LOG_LEVEL: INFO

  # Optional: Local ELK stack
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    
  logstash:
    image: docker.elastic.co/logstash/logstash:8.8.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf:ro
    depends_on:
      - elasticsearch
    
  kibana:
    image: docker.elastic.co/kibana/kibana:8.8.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

#### Structured Logging

```yaml
services:
  proxmox-mcp:
    image: ghcr.io/basher83/proxmox-mcp:latest
    
    environment:
      LOG_FORMAT: json
      LOG_LEVEL: INFO
      LOG_TIMESTAMP: true
    
    # JSON logging configuration
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"
        compress: "true"
        labels: "service,environment,version"
    
    labels:
      - "service=proxmox-mcp"
      - "environment=production"
      - "version=1.0.0"
```

### Metrics and Monitoring

#### Prometheus Integration (Future)

```yaml
# Prometheus monitoring setup
version: '3.8'

services:
  proxmox-mcp:
    image: ghcr.io/basher83/proxmox-mcp:latest
    
    # Metrics port (if implemented)
    ports:
      - "9090:9090"
    
    environment:
      METRICS_ENABLED: "true"
      METRICS_PORT: "9090"
  
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9091:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  grafana-data:
```

---

## Troubleshooting

### Common Issues

#### 1. Container Won't Start

```bash
# Check container logs
docker logs proxmox-mcp

# Common causes and solutions:
# - Configuration file not found
# - Invalid JSON in config file
# - Permission issues with mounted volumes
# - Network connectivity to Proxmox server

# Debugging steps
docker run --rm -it \
  -v ./proxmox-config:/app/proxmox-config:ro \
  ghcr.io/basher83/proxmox-mcp:latest \
  /bin/sh
```

#### 2. Health Check Failures

```bash
# Manual health check
docker exec proxmox-mcp /app/health_check.sh

# Check configuration validity
docker exec proxmox-mcp python -c "
from proxmox_mcp.config.loader import load_config
try:
    config = load_config()
    print('Configuration loaded successfully')
except Exception as e:
    print(f'Configuration error: {e}')
"

# Check Proxmox connectivity
docker exec proxmox-mcp python -c "
import requests
try:
    response = requests.get('https://your-proxmox-host:8006/api2/json/version', verify=False, timeout=10)
    print(f'Proxmox server reachable: {response.status_code}')
except Exception as e:
    print(f'Proxmox server unreachable: {e}')
"
```

#### 3. Permission Issues

```bash
# Fix volume permissions
sudo chown -R 10001:10001 ./proxmox-config ./logs
sudo chmod 600 ./proxmox-config/config.json
sudo chmod 700 ./proxmox-config

# Check container user
docker exec proxmox-mcp id
# Expected: uid=10001(appuser) gid=10001(appgroup)
```

#### 4. SSL/TLS Issues

```bash
# Test SSL connectivity
docker exec proxmox-mcp openssl s_client -connect your-proxmox-host:8006

# Disable SSL verification temporarily (not recommended for production)
# Set verify_ssl: false in config.json

# Add custom CA certificate
docker run -v ./ca-cert.pem:/usr/local/share/ca-certificates/proxmox-ca.crt:ro \
  ghcr.io/basher83/proxmox-mcp:latest \
  update-ca-certificates
```

### Debugging Tools

#### Interactive Debugging

```bash
# Run interactive shell
docker run --rm -it \
  -v ./proxmox-config:/app/proxmox-config:ro \
  --entrypoint /bin/bash \
  ghcr.io/basher83/proxmox-mcp:latest

# Debug with Python
docker exec -it proxmox-mcp python
>>> from proxmox_mcp.config.loader import load_config
>>> config = load_config()
>>> print(config)
```

#### Development Mode

```bash
# Run in development mode with debugging
docker run --rm -it \
  -v ./src:/app/src:rw \
  -v ./proxmox-config:/app/proxmox-config:ro \
  -p 5678:5678 \
  -e PYTHON_DEV_MODE=1 \
  ghcr.io/basher83/proxmox-mcp:latest
```

### Performance Troubleshooting

#### Resource Monitoring

```bash
# Monitor container resources
docker stats proxmox-mcp

# Check container processes
docker exec proxmox-mcp ps aux

# Monitor system calls (if needed)
docker run --rm -it --pid container:proxmox-mcp \
  nicolaka/netshoot strace -p 1
```

#### Memory Issues

```bash
# Check memory usage
docker exec proxmox-mcp cat /proc/meminfo
docker exec proxmox-mcp free -h

# Adjust memory limits in compose file
deploy:
  resources:
    limits:
      memory: 1G  # Increase if needed
```

---

## Best Practices

### Production Deployment

#### Version Management

```bash
# Always pin specific versions in production
image: ghcr.io/basher83/proxmox-mcp:v1.0.0  # ✅ Good
image: ghcr.io/basher83/proxmox-mcp:latest  # ❌ Avoid in production

# Test upgrades in staging first
docker pull ghcr.io/basher83/proxmox-mcp:v1.1.0
docker-compose -f docker-compose.staging.yml up -d
```

#### Resource Planning

```yaml
# Production resource allocation
deploy:
  resources:
    limits:
      memory: 1G      # Conservative limit
      cpus: '1.0'     # Allow burst capacity
    reservations:
      memory: 256M    # Minimum guaranteed
      cpus: '0.2'     # Minimum guaranteed
```

#### Backup and Recovery

```bash
# Backup configuration and logs
tar -czf proxmox-mcp-backup-$(date +%Y%m%d).tar.gz \
  proxmox-config/ logs/

# Restore configuration
tar -xzf proxmox-mcp-backup-20240101.tar.gz

# Database backup (if applicable)
docker exec proxmox-mcp backup-command > backup.sql
```

### Security Best Practices

#### Principle of Least Privilege

```yaml
# Minimal permissions
security_opt:
  - no-new-privileges:true
read_only: true
cap_drop:
  - ALL
user: "10001:10001"
```

#### Secret Management

```bash
# Use external secret management
# - HashiCorp Vault
# - AWS Secrets Manager
# - Azure Key Vault
# - Kubernetes Secrets

# Rotate secrets regularly
# Audit secret access
# Monitor for secret exposure
```

#### Network Security

```yaml
# Network isolation
networks:
  proxmox-network:
    driver: bridge
    internal: true  # No external access
    ipam:
      config:
        - subnet: 172.20.0.0/24
```

### Monitoring Best Practices

#### Health Checks

```yaml
# Comprehensive health checks
healthcheck:
  test: ["CMD", "/app/health_check.sh"]
  interval: 30s      # Frequent enough to detect issues
  timeout: 10s       # Reasonable timeout
  retries: 3         # Allow temporary failures
  start_period: 30s  # Give time to start up
```

#### Log Management

```yaml
# Structured logging
environment:
  LOG_FORMAT: json
  LOG_LEVEL: INFO
  LOG_TIMESTAMP: true

# Log rotation
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "5"
    compress: "true"
```

### Performance Optimization

#### Container Optimization

```bash
# Use specific base image tags
FROM python:3.10.12-slim  # Specific version

# Optimize layer caching
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .  # Copy source last
```

#### Resource Tuning

```yaml
# Production tuning
environment:
  PYTHONOPTIMIZE: "2"           # Optimize Python
  PYTHONDONTWRITEBYTECODE: "1"  # No .pyc files
  PYTHONUNBUFFERED: "1"         # Immediate output

# System limits
ulimits:
  nofile:
    soft: 65536
    hard: 65536
```

### Maintenance

#### Regular Updates

```bash
# Automated update checking
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}"

# Update process
docker-compose pull
docker-compose up -d
docker image prune -f  # Clean old images
```

#### Monitoring and Alerting

```yaml
# Set up alerts for:
# - Container health failures
# - High memory/CPU usage
# - Log error patterns
# - SSL certificate expiration
# - Proxmox API connectivity issues
```

---

This comprehensive deployment guide provides everything needed to successfully deploy ProxmoxMCP using Docker in any environment, from local development to enterprise production deployments.
