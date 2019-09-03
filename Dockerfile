FROM python:3.7

WORKDIR /app

COPY requirements requirements
RUN pip install -r requirements/dev.txt

COPY . .

EXPOSE 5000
