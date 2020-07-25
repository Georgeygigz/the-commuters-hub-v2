docker-compose build
docker tag commuters-image 241619/commuters:latest
docker tag commuters-image 241619/commuters:$SHA
docker push 241619/commuters:latest
docker push 241619/commuters:$SHA
# kubectl apply -f k8s/deployments
# kubectl apply -f k8s/ingress
# kubectl apply -f k8s/pvcs
# kubectl apply -f k8s/services

kubectl apply -f k8s/prod/deployments
kubectl apply -f k8s/prod/ingress
kubectl apply -f k8s/prod/services

kubectl set image deployments/server-deployment server=241619/commuters:$SHA