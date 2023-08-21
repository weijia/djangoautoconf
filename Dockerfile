FROM python:3.11.4

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
# COPY requirements.txt ./
# RUN pip install -r requirements.txt
RUN pip install django
COPY . ./djangoautoconf
WORKDIR /usr/src/app/djangoautoconf
RUN python setup.py install

WORKDIR /usr/src/app
RUN django-admin startproject commonsite
WORKDIR /usr/src/app/commonsite
RUN mv manage.py original_manage.py
COPY auto_manage.py manage.py

EXPOSE 8000
CMD python manage.py migrate; python manage.py runserver 0.0.0.0:8000