#!/bin/bash
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
kubectl apply -f k8s/contato-service-deployment.yaml
kubectl apply -f k8s/contato-service-clusterip.yaml
kubectl apply -f k8s/graphql-gateway-deployment.yaml
kubectl apply -f k8s/graphql-gateway-nodeport.yaml

