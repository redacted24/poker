FROM node:20

WORKDIR /site

RUN npm ci

WORKDIR /db

COPY . .

RUN npm ci

WORKDIR /site

COPY ./dist ../db/dist

ENTRYPOINT ["npm", "start"]