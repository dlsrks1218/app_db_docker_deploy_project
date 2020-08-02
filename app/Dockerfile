FROM python:3.7

# (1) 파이썬 애플리케이션 디렉토리 복사
WORKDIR /root/mod_project
COPY ./__init__.py /root/mod_project
COPY ./main.py /root/mod_project
COPY ./salesperson_module.py /root/mod_project
COPY ./customer_module.py /root/mod_project
COPY ./user_init.py /root/mod_project

# (2) mysql-client 및 pymysql 설치 후 프로젝트 실행
RUN apt-get update -y; apt-get upgrade -y;
RUN apt-get install -y default-mysql-client
RUN pip install pymysql
RUN echo "python main.py" >> ~/.bashrc
