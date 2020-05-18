## Build
docker build . -t "api:latest"

## Run
docker run -d -p 5000:5000 api:latest
