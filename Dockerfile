FROM --platform=arm64 node:20.5.1 as build

WORKDIR /app

COPY . .

RUN npm ci
RUN npm run build
RUN npm prune --production


FROM --platform=arm64 node:20.5.1 as deploy
WORKDIR /app
COPY --from=build /app/build build/
COPY --from=build /app/node_modules node_modules/
COPY package.json .

ENTRYPOINT [ "node", "build"]