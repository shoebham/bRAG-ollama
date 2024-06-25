FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install
RUN npm i marked
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]