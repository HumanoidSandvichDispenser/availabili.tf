# Use the official Node.js runtime as a parent image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy the entire app into the container
COPY . .

# Expose the Vite development server port
EXPOSE 5173

# Command to start the Vite development server
CMD ["npm", "run", "dev", "--", "--host"]
