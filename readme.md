docker-commands
docker compose -f docker-compose.prod.yml --env-file ./.envs/.prod/.compose.env build
docker compose -f docker-compose.prod.yml --env-file ./.envs/.prod/.compose.env stop
docker compose -f docker-compose.prod.yml --env-file ./.envs/.prod/.compose.env up -d --scale app=8 --remove-orphans

Tasks

1. add reports to db
2. add endpoints for fetching report
3. add endpoints for fetching stats
4. configure email sending
