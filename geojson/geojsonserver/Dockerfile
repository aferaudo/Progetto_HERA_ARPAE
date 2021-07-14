# Running docker container: sudo docker run -itd -p 8000:8000 --name 'geojsonserv' geoserver
FROM python:3.8-slim-buster

WORKDIR /geojsonserver

EXPOSE 8000


# copy server needed files
COPY file_to_serve/colors.json /geojsonserver/file_to_serve/colors.json
COPY file_to_serve/data.json /geojsonserver/file_to_serve/data.json
COPY file_to_serve/confinati_sup.json /geojsonserver/file_to_serve/confinati_sup.json

# Copy server script
COPY my_server.py my_server.py
RUN chmod +x my_server.py


# It runs a server on port 8000
CMD ["python3", "/geojsonserver/my_server.py"]