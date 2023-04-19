# Docker compose setup

prerequisites: docker, docker-compose

- https://docs.docker.com/engine/install/ to setup docker
- https://docs.docker.com/compose/install/ to setup docker compose

```
// navigate to root folder
$  sudo docker-compose up --build
```

Navigate to localhost:8000 to view the frontend, use the quar.ch8 file in root as an example file

# Development setup

## Backend

Prerequisites: python, pip, poetry (can be installed with `pip install poetry`)

```
// navigate to backend folder
$  poetry install
$  poetry run start
```

The backend will now be running on port 3000 by default

## Frontend

Prerequisites: yarn, node.js

```
// navigate to frontend folder
$  yarn install
$  yarn start
```

The frontend will be running on port 8000 by default
