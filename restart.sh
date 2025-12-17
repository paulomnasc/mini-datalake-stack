#!/bin/bash

echo "======================================"
echo "  Mini Datalake Stack - Restart"
echo "======================================"
echo ""

echo "🔄 Restarting all services..."
docker-compose restart

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✅ Restart complete!"
echo ""
