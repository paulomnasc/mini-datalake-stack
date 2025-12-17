#!/bin/bash

echo "======================================"
echo "  MinIO Bucket Setup"
echo "======================================"
echo ""

# Wait for MinIO to be ready
echo "⏳ Waiting for MinIO to be ready..."
sleep 5

# Create buckets using mc (MinIO Client)
docker run --rm --network mini-datalake-stack_datalake-network \
  minio/mc:latest \
  sh -c "
    mc alias set myminio http://minio:9000 minioadmin minioadmin123 && \
    mc mb myminio/raw --ignore-existing && \
    mc mb myminio/bronze --ignore-existing && \
    mc mb myminio/silver --ignore-existing && \
    mc mb myminio/gold --ignore-existing && \
    echo '' && \
    echo '✅ Buckets created successfully!' && \
    echo '' && \
    mc ls myminio
  "

echo ""
echo "✅ MinIO setup complete!"
echo ""
