#!/bin/bash
docker build -t mssql2019 SQL-server
docker run --rm -d --network Internal --ip 10.0.0.20 --name dbsqlserver2019 mssql2019
# wait to be sure that SQL Server came up
echo "Sleep.... 30s"
sleep 30s
echo "Done sleep"
# init SQL
docker exec dbsqlserver2019 /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P Trung@123456789 -i init.sql
echo "Done init"