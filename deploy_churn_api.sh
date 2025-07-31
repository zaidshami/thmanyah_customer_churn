#!/bin/bash

# ---- CONFIG ----
ACCOUNT_ID="767397763254"
REGION="ap-south-1"
REPO_NAME="thmanyah-container"
PORT=8000

# ---- AUTHENTICATE WITH ECR ----
echo "[1/5] Authenticating with ECR..."
aws ecr get-login-password --region $REGION | \
docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

## ---- BUILD DOCKER IMAGE ----
#echo "[2/5] Building Docker image..."
#docker build -t $REPO_NAME .
#
## ---- TAG IMAGE FOR ECR ----
#echo "[3/5] Tagging Docker image..."
#docker tag $REPO_NAME:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest
#
## ---- PUSH TO ECR ----
#echo "[4/5] Pushing image to ECR..."
#docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest

# ---- RUN CONTAINER ----
echo "[5/5] Running container on port $PORT..."
docker stop churn-api || true
docker rm churn-api || true
docker run -d --name churn-api -p 80:$PORT $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest
docker update --restart=always churn-api

echo "✅ Deployment complete. API running on port 80 → http://<EC2_PUBLIC_IP>/predict"
