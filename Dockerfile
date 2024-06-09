FROM python:3.9
WORKDIR /app
COPY . /app 
ADD ./requirements.txt ./
RUN python3 -m pip install -r requirements.txt

# Copiar el script de entrada
COPY entrypoint.sh /app/entrypoint.sh

# Hacer el script ejecutable
RUN chmod +x /app/entrypoint.sh

# Usar el script de entrada
ENTRYPOINT ["/app/entrypoint.sh"]