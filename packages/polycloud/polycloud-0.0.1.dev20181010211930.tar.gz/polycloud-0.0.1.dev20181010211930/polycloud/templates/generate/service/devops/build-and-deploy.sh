#!/bin/bash
set -ex

# SET THE FOLLOWING VARIABLES
# docker hub username 
USERNAME={{dockerusername}}
# image name TODO get this from config? replace this placeholder when the repository is initialize with the repo/api name via sed
IMAGE={{apiname}}
# get latest githash
LATEST_GIT_HASH=$(git log -1 --format=%h)

# bump version
bump patch
version=`cat VERSION`
echo "version: $version"
# run build
docker build -t $USERNAME/$IMAGE:latest --build-arg GIT_COMMIT=$LATEST_GIT_HASH .

#display the githash in the image
docker inspect $USERNAME/$IMAGE:latest | jq '.[].ContainerConfig.Labels'

# UNIT TESTS
# docker exec $USERNAME/$IMAGE:latest npm run test

# update the deployment config with the new version
cd ./devops/config && sed "s@\$version@$version@g" deployment.yaml > deployment.tmp && mv deployment.tmp deployment.yaml && cd ../..

# push to docker hub
docker login -u $USERNAME -p $DOCKER_PASSWORD 
docker tag $USERNAME/$IMAGE:latest $USERNAME/$IMAGE:$version
# push it
docker push $USERNAME/$IMAGE:latest
docker push $USERNAME/$IMAGE:$version

# install app
kubectl apply -f  devops/config/deployment.yaml
kubectl apply -f  devops/config/network.yaml

# Confirm all services and pods are correctly defined and running
kubectl get services
kubectl get pods

# confirm bookinfo app is running (can I use a health-check or prometheus?)
#curl -o /dev/null -s -w "%{http_code}\n" http://${GATEWAY_URL}/productpage

# RLEASE AS BUILD VERSION (X.X.X+1)
# login to github
git config --global user.email "den.seidel+cicd@gmail.com"
git config --global user.name "cicd"
git config --global push.default simple
# tag it
git add -A
git commit -m "version $version [skip ci]"
git tag -a "$version" -m "version $version"
#git push
git push
git push --tags