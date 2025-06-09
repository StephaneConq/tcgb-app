# 1. Use an official Node image as the base
FROM node:23

# 2. Set working directory
WORKDIR /app

# 3. Copy package.json and lock files first for caching
COPY package*.json ./

COPY svelte.config.js svelte.config.js
COPY tsconfig.json tsconfig.json
COPY vite.config.ts vite.config.ts

# 4. Install dependencies
RUN npm install

# 5. Copy the rest of your application code
COPY src src
COPY static static
COPY .env .env

RUN echo 'VITE_API_BASE_URL="https://tcgb-back-780761084412.europe-west9.run.app"' >> .env

# 6. Build the SvelteKit app (uses adapter-node)
RUN npm run build

RUN npm run prepare

# 7. Expose the default port used by SvelteKit adapter-node
EXPOSE 3000

# 8. Start the Node server
CMD [ "node", "build" ]
