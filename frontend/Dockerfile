FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 3000

# Obs: não recomendado para produção
# mais informações: https://flask.palletsprojects.com/en/2.2.x/deploying/
CMD [ "python3", "app.py" ]
