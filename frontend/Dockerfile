FROM node:18-alpine AS build
WORKDIR /app
COPY . .
RUN npm install && npm run build

FROM node:18-alpine
RUN npm install -g http-server
WORKDIR /app
COPY --from=build /app/dist .
CMD ["http-server", "-p", "80"]
