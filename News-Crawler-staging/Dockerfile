FROM python:3.11.4-slim-bullseye

# Set the working directory
WORKDIR /usr/src/news/

# Set environment variables
ENV TZ=Asia/Kolkata

# Copy requirements and install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set appropriate permissions
RUN chmod 755 /usr/src/news/run.sh

# Set the default command
CMD ["python", "api.py"]
