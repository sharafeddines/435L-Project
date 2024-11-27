FROM mcr.microsoft.com/mssql/server:2022-latest

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=SO@12345
ENV MSSQL_TCP_PORT=1433

USER root
RUN apt-get update && \
apt-get remove -y libodbc2 libodbcinst2 unixodbc-common && \
apt-get install -y --no-install-recommends \
curl apt-transport-https gnupg && \
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /etc/apt/keyrings/microsoft.gpg && \
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/ubuntu/20.04/prod focal main" > /etc/apt/sources.list.d/mssql-release.list && \
apt-get update && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
mssql-tools unixodbc-dev && \
apt-get clean && rm -rf /var/lib/apt/lists/*

# Switch back to the mssql user
USER mssql

# Copy the SQL script into the container
COPY create-database.sql /usr/src/app/create-database.sql

# JSON CMD format to avoid signal issues
CMD /bin/bash -c "/opt/mssql/bin/sqlservr & sleep 60 && /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P '$SA_PASSWORD' -i /usr/src/app/create-database.sql; wait"
