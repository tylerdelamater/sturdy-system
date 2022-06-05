#! /bin/bash
docker run --net mynet123 --ip 172.18.0.22 -e AZURE_CLIENT_ID -e AZURE_TENANT_ID -e AZURE_CLIENT_SECRET sturdysystemcr.azurecr.io/sturdy-system-u &
