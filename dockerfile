FROM ubuntu:22.04

ENV LANG C.UTF-8

# install mysql-server, mysql-client
RUN apt-get update && \
    apt-get install -y tzdata systemctl && \
    apt-get install -y mysql-server && \
    echo "Asia/Shanghai" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get install -y mysql-client

# config a root with password 123456
RUN systemctl enable mysql && \
    service mysql start && \
    mysql -e "CREATE USER 'luling'@'%' IDENTIFIED BY '123456'; GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION; FLUSH PRIVILEGES;"

# create a database and create the table
RUN service mysql restart && \
    mysql -u root -p123456 -e "CREATE DATABASE IF NOT EXISTS aimemory; USE aimemory;CREATE TABLE IF NOT EXISTS main(\`id\` int not null auto_increment,\`sender\` varchar(64) not null,\`group\` varchar(64) not null,\`content\` varchar(4096) not null,\`date\` datetime(3),\`reply\` int unsigned default 0,primary key(\`id\`))ENGINE=InnoDB DEFAULT CHARSET=utf8;"

# install python3.8
RUN apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.8

# install ubuntu requirements
RUN apt-get install -y openjdk-17-jdk git pip curl openssh-server wget vim

# pull backend and install python requirements
RUN mkdir /home/luling-backend && \
    cd /home/luling-backend && \
    git clone https://github.com/huan-yp/luling-backend.git /home/luling-backend && \
    pip install -r /home/luling-backend/requirement.txt

# install mirai-console and lulingAI plugin
RUN mkdir /home/luling-frontend && \
    cd /home/luling-frontend && \
    wget https://github.com/iTXTech/mcl-installer/releases/download/v1.0.7/mcl-installer-1.0.7-linux-amd64 -O installer && \
    chmod 777 installer && echo -e "N\nY\n" | ./installer && \
    mkdir ./plugins && \
    wget http://47.109.84.142:8001/fix-protocol-version-1.3.0.mirai2.jar -O "./plugins/fix-protocol.jar" && \
    wget http://47.109.84.142:8001/LuLing%20AI-0.2.0.mirai2.jar -O "./plugins/LuLingAI-0.2.0.mirai2.jar"