FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .
ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000

HEALTHCHECK --interval=10s --timeout=5s --retries=5 CMD wget -q --spider http://localhost:3000 || exit 1

CMD ["nginx", "-g", "daemon off;"]