FROM python:3.9

COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

WORKDIR /app

RUN chmod +x run.sh

EXPOSE 80

CMD ["./run.sh"]