FROM apache/hadoop:3

WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN sudo yum update -y
RUN sudo yum install -y centos-release-scl
RUN sudo yum install -y rh-python36
RUN scl enable rh-python36 bash && sudo /opt/rh/rh-python36/root/usr/bin/pip install --upgrade pip && /opt/rh/rh-python36/root/usr/bin/pip install Flask

COPY . .
RUN scl enable rh-python36 bash && pip install -r requirements.txt
EXPOSE 5000 9870 8020

# Set environment variables, if needed
ENV LC_ALL=en_US.utf8

RUN sudo chmod 777 ./temp


# Set the default command to run HDFS Namenode and Flask application
CMD ["hdfs","namenode"]