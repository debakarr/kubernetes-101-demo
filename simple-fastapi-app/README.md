# Create a docker image

```console
docker build -t simple-fastapi-app
```

# Run it locally

```console
docker run -d --name simple-fastapi-app -p 80:80 simple-fastaspi-app
```

# Access it locally

```console
curl 127.0.0.1:80
```

# Push it to DockerHub

```console
docker tag simple-fastapi-app debakarr/simple-fastapi-app:1.0.0
docker push debakarr/simple-fastapi-app:1.0.0
```
