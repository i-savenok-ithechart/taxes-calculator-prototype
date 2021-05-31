FROM tiangolo/uwsgi-nginx:python3.8
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install python-dev postgresql-client libssl-dev -y
RUN pip3 install pipenv
RUN mkdir /code
WORKDIR /code
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN export LC_ALL=C.UTF-8 && export LANG=C.UTF-8 && pipenv lock -r > requirements.txt
RUN pip3 install -r requirements.txt
COPY src /code/
COPY ./entrypoint.sh /code/
RUN apt install -y netcat
RUN chmod +x /code/entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]

EXPOSE 8000
