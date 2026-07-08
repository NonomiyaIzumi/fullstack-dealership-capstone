FROM node:20-slim

WORKDIR /app

# The mongod binary mongodb-memory-server downloads at runtime is a real
# MongoDB server build that needs these shared libraries, which node's slim
# base image strips out to save space.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcurl4 libssl3 libgssapi-krb5-2 liblzma5 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY package.json ./
RUN npm install

COPY . .

ENV PORT=3030
EXPOSE 3030

CMD ["npm", "start"]
