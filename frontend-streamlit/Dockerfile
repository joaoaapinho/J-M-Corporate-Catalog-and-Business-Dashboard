# Using the official Python image as the base image.
FROM python:3.11.2

# Setting the working directory.
WORKDIR /frontend-streamlit

# Copying requirements.txt into the Docker container.
COPY requirements.txt .

# Installing the dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copying the rest of your application's code into the Docker container.
COPY . .

# Setting the PORT environment variable.
ENV PORT 8080

# Exposing the port your app runs on.
EXPOSE $PORT

# Starting the application.
CMD streamlit run main.py --server.port $PORT --server.address 0.0.0.0