FROM python:3.7 as builder

RUN pip3 install pipenv --no-cache-dir
RUN apt-get update && apt-get install -y swig glpk-utils libglpk-dev
COPY Pipfile Pipfile.lock /
ENV PIPENV_CLEAR 1
RUN pipenv install --system --verbose --ignore-pipfile


FROM python:3.7-slim
RUN adduser --no-create-home --disabled-login --group --system django
RUN mkdir /srv/starter && chown -R django:django /srv/starter
COPY config/django-uwsgi.ini /etc/uwsgi/django-uwsgi.ini

RUN apt-get update && apt-get install -y swig glpk-utils libxml2 && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/
COPY --from=builder /usr/local/bin/uwsgi /usr/local/bin/uwsgi
COPY vizan_rest_server/ /srv/starter
COPY config/start.sh /

CMD ["./start.sh"]
