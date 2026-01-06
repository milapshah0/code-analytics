FROM node:22-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application code
COPY . .

# Expose port
EXPOSE 4200

# Start application
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0"]
