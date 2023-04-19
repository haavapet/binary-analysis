FROM node:19-alpine

WORKDIR /app

COPY package*.json ./

RUN yarn install

COPY ./ .

EXPOSE 3000

# Get arg from docker compose and pass it through to frontend container
ARG BACKEND_URL
ENV REACT_APP_BACKEND_URL=$BACKEND_URL

CMD [ "yarn", "start" ]