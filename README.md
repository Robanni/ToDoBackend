I use devcontainer

devcontainer.json->
{
	"name": "Python 3 & PostgreSQL",
	"dockerComposeFile": "docker-compose.yml",
	"service": "app",
	"workspaceFolder": "/workspaces/${localWorkspaceFolderBasename}"
}
<-


docker-compose->
version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile

    volumes:
      - ../..:/workspaces:cached

    command: sleep infinity

    network_mode: service:db


  db:
    image: postgres:latest
    restart: unless-stopped
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: postgres
      POSTGRES_DB: postgres
      POSTGRES_PASSWORD: postgres

volumes:
  postgres-data:
->


Dockerfile->
FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

ENV PYTHONUNBUFFERED 1
<-

