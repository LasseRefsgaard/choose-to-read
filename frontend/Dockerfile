# Dockerfile for Vue.js
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Set npm registry to default
RUN npm config set registry https://registry.npmjs.org/

# Install dependencies
RUN npm install

# Copy the rest of your frontend code into the container
COPY . .

# Build the Vue.js application
RUN npm run build

# Expose the port that Vue.js runs on
EXPOSE 8080

# Command to run the application
CMD ["npm", "run", "serve"]