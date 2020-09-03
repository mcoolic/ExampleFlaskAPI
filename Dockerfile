# parent image
FROM python:3.7-slim

# install FreeTDS and dependencies
RUN apt-get update
RUN apt-get install g++ -y
RUN apt-get install curl -y
RUN apt-get install gcc -y
RUN apt-get install --reinstall build-essential -y
RUN apt-get update && apt-get install -y gnupg2
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/19.10/prod.list > /etc/apt/sources.list.d/mssql-release.list
# RUN exit

RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev 

RUN pip install pypyodbc
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install msodbcsql17
RUN ACCEPT_EULA=Y apt-get install mssql-tools
RUN apt-get install unixodbc-dev -y

ADD application.py /

RUN pip install flask

RUN pip install pyodbc

RUN pip install flask_cors

EXPOSE 5000
CMD [ "python", "./application.py" ]