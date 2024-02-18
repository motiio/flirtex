FROM node:latest

RUN mkdir -p /app
WORKDIR /app

COPY ../package.json ./
COPY ../package-lock.json ./

RUN npm install

COPY .. .

CMD ["npm", "run", "start"]
