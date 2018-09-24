FROM python:3.6-slim
ADD . /myapp
WORKDIR /myapp
RUN pip install -r requirements.txt
