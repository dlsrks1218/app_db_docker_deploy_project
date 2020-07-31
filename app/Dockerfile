FROM python:3.7

WORKDIR /root/mod_project
COPY ./__init__.py /root/mod_project
COPY ./main.py /root/mod_project
COPY ./salesperson_module.py /root/mod_project
COPY ./customer_module.py /root/mod_project
COPY ./user_init.py /root/mod_project

RUN apt-get update -y; apt-get upgrade -y;
RUN apt-get install -y default-mysql-client
RUN pip install pymysql
