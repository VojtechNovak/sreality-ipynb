FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set the ChromeDriver version as a build argument
ARG CHROME_DRIVER_VERSION=114.0.5735.90

# Download and install ChromeDriver
RUN curl -SL "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" -o /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /app


COPY . .

CMD ["python","sreality.py" ,"server.py"]
