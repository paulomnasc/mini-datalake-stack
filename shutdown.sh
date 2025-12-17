#!/bin/bash

echo "======================================"
echo "  Mini Datalake Stack - Shutdown"
echo "======================================"
echo ""

echo "🛑 Stopping all services..."
docker-compose down

echo ""
echo "✅ All services stopped successfully!"
echo ""
echo "💡 To remove all data, run:"
echo "   docker-compose down -v"
echo "   rm -rf data/"
echo ""
