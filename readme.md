docker-commands
docker compose -f docker-compose.prod.yml --env-file ./.envs/.prod/.compose.env build
docker compose -f docker-compose.prod.yml --env-file ./.envs/.prod/.compose.env stop
docker compose -f docker-compose.prod.yml --env-file ./.envs/.prod/.compose.env up -d --scale app=8 --remove-orphans

Tasks

1. add reports to db
2. add endpoints for fetching report
   -> report for each client type per date range(per month)
   -> month on month report for the past 12 months for each report type
   -> top 5 clients for the previous month
3. add endpoints for fetching stats
4. configure email sending
