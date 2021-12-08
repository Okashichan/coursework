FROM python:slim

WORKDIR /coursework-app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "./main.py" ]