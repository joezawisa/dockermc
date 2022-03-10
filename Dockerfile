FROM openjdk:latest

# Install Python 3
RUN microdnf install python3

WORKDIR /mc

# Install Python requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Include the startup script
COPY start.py .

ENTRYPOINT ["python3", "start.py"]