#!/bin/bash

echo "======================================"
echo "  Mini Datalake Stack - Startup"
echo "======================================"
echo ""

# Check if docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "🚀 Starting all services..."
echo ""

# Create necessary directories
echo "📁 Creating data directories..."
mkdir -p data/minio data/postgres data/spark data/logs

# Start services
echo "🐳 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "======================================"
echo "  ✅ Startup Complete!"
echo "======================================"
echo ""
echo "🌐 Access Points:"
echo "  - MinIO Console:    http://localhost:9001"
echo "    User: minioadmin / Pass: minioadmin123"
echo ""
echo "  - Spark Master UI:  http://localhost:8080"
echo ""
echo "  - Airflow Web UI:   http://localhost:8081"
echo "    User: admin / Pass: admin"
echo ""
echo "📝 Useful Commands:"
echo "  - View logs:        docker-compose logs -f [service-name]"
echo "  - Stop all:         ./shutdown.sh"
echo "  - Restart:          ./restart.sh"
echo ""
