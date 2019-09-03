FROM node:latest

RUN npm install -g http-server

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build prod

EXPOSE 8080

CMD ["http-server", "dist"]
