docker-commands
docker compose -f docker-compose.prod.yml --env-file ./.envs/.prod/.compose.env build
docker compose -f docker-compose.prod.yml --env-file ./.envs/.prod/.compose.env stop
docker compose -f docker-compose.prod.yml --env-file ./.envs/.prod/.compose.env up -d --scale app=8 --remove-orphans
