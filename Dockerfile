# Build stage for frontend
FROM node:16 as frontend-builder

WORKDIR /app/frontend

# Install quasar CLI globally
RUN npm install -g @quasar/cli

# Copy frontend package files first to leverage Docker cache
COPY frontend/package*.json ./
RUN npm install

# Copy the rest of the frontend source
COPY . .

# Build the Quasar app
RUN npx quasar build

# Final stage
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the built frontend from previous stage
COPY --from=frontend-builder /app/frontend/dist/spa /app/frontend/dist/spa

# Install the dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

EXPOSE 9000

ENV GOOGLE_APPLICATION_CREDENTIALS=able-81a4e-e694abda18d2.json

CMD ["python", "backend/server.py"]