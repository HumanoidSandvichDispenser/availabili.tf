# Use an official Python runtime as a parent image
FROM python:3.12-slim

COPY requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

# Expose the Flask development server port
EXPOSE 5000

# Set the Flask environment to development
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]
