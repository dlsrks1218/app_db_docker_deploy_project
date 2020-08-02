FROM mysql:5.7

# (1) 패키지 업데이트 및 wget 설치
RUN apt-get update
RUN apt-get install -y wget

# (2) 스크립트 및 각종 설정 파일 복사
COPY etc/mysql/mysql.conf.d/mysqld.cnf /etc/mysql/mysql.conf.d/
COPY etc/mysql/conf.d/mysql.cnf /etc/mysql/conf.d/
COPY ./mysql_init_files/init.sql /docker-entrypoint-initdb.d/

# (3) 스크립트, mysqld 실행
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["mysqld"]
