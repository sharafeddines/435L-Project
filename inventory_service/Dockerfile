# start by pulling the python image
FROM python:3.9-slim
# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt
# switch working directory
WORKDIR /app
RUN apt-get update && apt-get install -y \
    curl \
    gpg \
    gnupg2 \
    apt-transport-https \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y \
    msodbcsql17 \
    unixodbc-dev \
    g++ \
    && rm -rf /var/lib/apt/lists/*
# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt
# copy every content from the local file to the image
EXPOSE 5002
COPY . /app
WORKDIR /app
CMD ["sh", "-c", "sleep 60 && python3 inventory_service.py"]
