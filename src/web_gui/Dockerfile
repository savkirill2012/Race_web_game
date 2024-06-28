FROM node:22-alpine

WORKDIR /web

ADD package.json /web

RUN npm install --no-root --no-interaction --no-ansi

COPY . /web/
COPY ./start_web.sh /web/

RUN npm run build
RUN chmod +x start_web.sh

EXPOSE 5173

# CMD ["npm", "run", "preview"]