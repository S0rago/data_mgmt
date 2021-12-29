kubectl delete deployment kafka-deployment-consumer-afonin
kubectl apply -f .\yandex-kafka\consumer\k8-deploy.yml

kubectl delete deployment kafka-deployment-producer-afonin
kubectl delete service kafka-service-producer-afonin
kubectl apply -f .\yandex-kafka\producer\k8-service.yml
kubectl apply -f .\yandex-kafka\producer\k8-deploy.yml

kubectl delete deployment kafka-deployment-mongo-afonin
kubectl delete service kafka-service-mongo-afonin
kubectl apply -f .\yandex-kafka\mongo-service\k8-service.yml
kubectl apply -f .\yandex-kafka\mongo-service\k8-deploy.yml