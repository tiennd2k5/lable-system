Activate venv:
for cmd: 
venv\Scripts\activate
for powershell:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1



Mysql docker compose:
name: Logistics-mysql

services:
  db-mysql:
    image: mysql:8.0.46
    container_name: Logistics-mysql
    restart: always
    environment:
      - MYSQL_DATABASE=LogisticsDB
      - MYSQL_ROOT_PASSWORD=Mst_0314120650
    ports:
      - "3307:3306"
    volumes:
      - Logistics-data:/var/lib/mysql
volumes:
 Logistics-data:



Overall workflow:
Shared folder 
-> watcher.py detect new PDF 
-> parser.py parse data
-> app.py receives JSON API request
-> store data in database

