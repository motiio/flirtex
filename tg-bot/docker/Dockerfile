FROM node:21-alpine3.18

RUN mkdir -p /app
WORKDIR /app

COPY ./package.json ./

RUN npm install

COPY ./src ./src

CMD ["npm", "run", "start"]
