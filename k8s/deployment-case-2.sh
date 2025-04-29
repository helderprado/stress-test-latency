kubectl apply -f secrets.yaml
kubectl apply -f postgres.yaml
kubectl apply -f api-single.yaml
kubectl apply -f rabbitmq.yaml
kubectl apply -f redis.yaml
kubectl apply -f flower.yaml
kubectl apply -f celery.yaml
kubectl apply -f stress-test-case-2.yaml