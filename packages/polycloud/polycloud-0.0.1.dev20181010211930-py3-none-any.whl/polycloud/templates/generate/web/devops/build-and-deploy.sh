#!/bin/bash
set -ex

#!/bin/bash
set -ex

# move to script folder
cd $(dirname $0)
echo $(pwd)

# SET THE FOLLOWING VARIABLES
# docker hub username 
USERNAME={{dockerusername}}
# image name TODO get this from config? 
IMAGE={{frontendname}}
# get latest githash
LATEST_GIT_HASH=$(git log -1 --format=%h)

clustercheck=$(kubectl rollout status -n istio-system deployment/istio-ingressgateway || true)
if [[ $clustercheck != *"successfully rolled out"* ]]; then
  echo "Istio Ingress-Gateway or Cluster not reachable."
  exit 1
fi

# ensure we're up to date
git pull

# run build
docker build --no-cache -t $USERNAME/$IMAGE:latest --build-arg GIT_COMMIT=$LATEST_GIT_HASH ..

#display the githash in the image
docker inspect $USERNAME/$IMAGE:latest | jq '.[].ContainerConfig.Labels'

# push to docker hub
docker login -u $USERNAME -p $DOCKER_PASSWORD 
docker tag $USERNAME/$IMAGE:latest $USERNAME/$IMAGE:v5
# push it
docker push $USERNAME/$IMAGE:latest
docker push $USERNAME/$IMAGE:v5

# install app
kubectl apply -f config/$IMAGE.yaml
kubectl apply -f config/$IMAGE-gateway.yaml
# Confirm all services and pods are correctly defined and running
kubectl get services
kubectl get pods