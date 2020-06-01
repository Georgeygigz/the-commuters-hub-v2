docker-compose build
docker tag commuters-image 241619/commuters:latest
docker tag commuters-image 241619/commuters:$SHA
docker push 241619/commuters:latest
docker push 241619/commuters:$SHA
kubectl apply -f k8s
kubectl set image deployments/server-deployment server=241619/commuters:$SHA