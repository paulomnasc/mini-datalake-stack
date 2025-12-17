#!/bin/bash

echo "======================================"
echo "  Service Status Check"
echo "======================================"
echo ""

# Function to check if a service is healthy
check_service() {
    local service=$1
    local url=$2
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "200\|302"; then
        echo "✅ $service is running"
    else
        echo "❌ $service is not responding"
    fi
}

echo "Checking services..."
echo ""

# Check MinIO
check_service "MinIO" "http://localhost:9000/minio/health/live"

# Check Spark Master
check_service "Spark Master" "http://localhost:8080"

# Check Airflow
check_service "Airflow" "http://localhost:8081/health"

echo ""
echo "Docker container status:"
docker-compose ps

echo ""
