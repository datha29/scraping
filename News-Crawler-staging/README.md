# News Crawler API
FastApi app deployed on port 9123

## Deployment
Before deployment build, tag & push image to GCR

```bash
docker build . -t crawler_v1
docker tag crawler_v1 asia-south1-docker.pkg.dev/jiox-328108/pie-ds-stage/prod/crawler_v1:latest
docker push asia-south1-docker.pkg.dev/jiox-328108/pie-ds-stage/prod/crawler_v1:latest
```
For Deploymemt  
```bash
kubectl get deployment
kubectl rollout restart deployment crawler-deploy
```


## Additional Info
2 docker compose file (each for api & pub-sub)

CMD to bring up api container
```bash
docker-compose -f docker-compose-api.yml up --build -d  --remove-orphans 
```
