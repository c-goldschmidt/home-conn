# stage 1: build frontend using npm
FROM node:12-alpine AS frontend

COPY frontend/package.json frontend/package-lock.json ./frontend/

WORKDIR frontend
RUN npm ci

COPY frontend/ ./
RUN npm run build-prod

# stage 2: build final container
FROM python:3.8-alpine

RUN apk add gcc musl-dev --no-cache

COPY ./Pipfile* ./server/
WORKDIR server

RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

COPY server/ ./
COPY entrypoint.sh .

# use previously build frontend
COPY --from=frontend /frontend/dist /frontend/dist

RUN chmod +x entrypoint.sh

RUN ls -la
ENTRYPOINT ./entrypoint.sh