# Use the official Node.js image as a base
FROM node:latest AS react-builder

# Set the working directory inside the container
WORKDIR /app/frontend

# Copy package.json and package-lock.json for npm install
COPY bubblescan-client/package*.json /app/frontend

# Install npm dependencies
RUN npm install

# Update npm
RUN npm install -g npm

# Install npm cors
RUN npm install cors

# Copy the React application code into the image
COPY bubblescan-client /app/frontend

# Expose port for React Vite development server
EXPOSE 5173

# Start React Vite development server
CMD ["npm", "run", "dev"]