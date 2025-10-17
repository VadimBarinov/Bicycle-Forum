FROM mysql:latest

ENV MYSQL_DATABASE=db_forum
ENV MYSQL_ROOT_PASSWORD=root

RUN chown -R mysql:mysql /docker-entrypoint-initdb.d/

EXPOSE 3306