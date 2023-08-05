FROM python:3.7-rc-alpine

RUN mkdir /code
ADD . /code
WORKDIR /code
RUN apk add --no-cache alpine-sdk libffi-dev openssl-dev
RUN pip install -r requirements.txt

EXPOSE 9080
CMD ["connexion", "run", "/code/swagger/swagger.yaml",  "--mock=all", "-v", "-p", "9080"]