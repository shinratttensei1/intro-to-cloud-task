# Intro to Cloud: Flask + MongoDB Notes App

This project demonstrates a containerized Python Flask application connected to a MongoDB database using Docker Compose.

## 1. Project Structure
Ensure your directory contains the following files:
- app.py (Flask application code)
- requirements.txt (Dependencies)
- Dockerfile (Build instructions)
- docker-compose.yml (Service orchestration)

## 2. Local Development (venv)
Use these commands to set up a local virtual environment for your IDE (VS Code/PyCharm) to recognize imports and provide autocomplete.

# Create the virtual environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt

## 3. Docker Compose Instructions
Docker Compose handles the networking between the Flask app and MongoDB automatically.

# Build the images and start the services
docker-compose up --build

# Start services in the background (detached mode)
docker-compose up -d

# Check the status of the containers
docker-compose ps

# Stop and remove the containers
docker-compose down

# Stop and remove containers AND delete the database volume
docker-compose down -v

## 4. Usage
Once the containers are running, access the application via your browser:

- Web UI: http://localhost:5050/
- JSON API: http://localhost:5050/notes

## 5. File Contents Reference

# requirements.txt
flask==3.0.3
pymongo==4.7.3

# Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5050
CMD ["python", "app.py"]

# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "5050:5050"
    environment:
      - MONGO_URI=mongodb://db:27017
    depends_on:
      - db
  db:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
volumes:
  mongo-data:
