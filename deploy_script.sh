#!/bin/bash
# command: bash deploy_script.sh $VERSION
VERSION=$1
echo "docker pull ieltslms/app-api-promting:$VERSION"
docker pull ieltslms/app-api-promting:$VERSION
sed -i "s/ieltslms\/app-api-promting.*/ieltslms\/app-api-promting:$VERSION/g" docker-compose.yaml
docker compose up app-api-promting -d