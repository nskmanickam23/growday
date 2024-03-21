# Development stage
FROM python:alpine AS development

WORKDIR /python-docker

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the application code
COPY . .
RUN ls

# Run tests
CMD ["python3", "main.py", "-v"]
