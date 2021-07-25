
# Use node alpine as it's a small node image
FROM alpine:3.11

# Create the directory on the node image 
# where our Next.js app will live
RUN mkdir -p /app

# Set /app as the working directory
WORKDIR /app

# Copy package.json and package-lock.json
# to the /app working directory
COPY package*.json /app/

# Install dependencies in /app
RUN apk add --no-cache nodejs npm
Run npm install


# Copy the rest of our Next.js folder into /app
COPY . /app

# Ensure port 3000 is accessible to our system
EXPOSE 3000

# Run npm run dev, as we would via the command line 
CMD ["npm", "run", "dev"]
