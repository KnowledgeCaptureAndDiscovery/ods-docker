FROM debian:stretch

# Point to a local mirror if needed
RUN sed -i 's/deb.debian.org/debianmirror.nkn.in/' /etc/apt/sources.list

# Install the apache-mysql-php stack
RUN apt-get update
RUN apt-get -y install apache2 mysql-server php php-mysql php-mbstring php-xml php-dom php-zip php-gd
RUN apt-get -y install curl unzip git

# Set environment
ENV WIKI_NAME "Enigma"
ENV ONT_URL "http://w3id.org/enigma"
ENV ADMIN_USER "admin"
ENV ADMIN_PW "admin123"
ENV WIKI_PATH "wiki"
ENV HTTP_PORT 8080
ENV HTTP_SERVER "localhost"
ENV MW_URL "https://releases.wikimedia.org/mediawiki/1.29/mediawiki-1.29.2.tar.gz"
ENV SMW_VERSION "2.5.5"

ENV WEB_HOME /var/www/html
ENV MW_HOME $WEB_HOME/$WIKI_PATH 

# Install Mediawiki
# ADD $MW_URL /tmp/mediawiki.tar.gz
RUN curl -sS $MW_URL | tar -C $WEB_HOME -xvz
RUN mv $WEB_HOME/mediawiki* $MW_HOME
RUN service mysql start && \
	php $MW_HOME/maintenance/install.php \
	--dbname "wiki" --dbuser "root" --dbpass "" \
	--pass $ADMIN_PW --scriptpath /$WIKI_PATH $WIKI_NAME $ADMIN_USER && \
	service mysql stop

# Install Mediawiki extensions
RUN cd $MW_HOME && curl -sS https://getcomposer.org/installer | php
RUN cd $MW_HOME && php composer.phar require mediawiki/semantic-media-wiki $SMW_VERSION --update-no-dev
RUN cd $MW_HOME && php composer.phar update --no-dev
RUN service mysql start && \
	cd $MW_HOME && php maintenance/update.php && \
	service mysql stop
RUN cd $MW_HOME && php composer.phar require easyrdf/easyrdf "*"
RUN cd $MW_HOME && php composer.phar require mediawiki/maps "*"
RUN cd $MW_HOME && php composer.phar update --no-dev
#RUN cd $MW_HOME && php composer.phar require scholarslab/bagit "~0.2" # For Linked Earth

# Patch mediawiki
RUN sed -i "s/ns < 0/ns < -1/" $MW_HOME/includes/page/WikiPage.php

# Install OrganicDataScience & extra extensions
ADD organicdatascience $MW_HOME/extensions/WorkflowTasks
ADD extra/PageObjectModel $MW_HOME/extensions/PageObjectModel
ADD extra/AccessControl $MW_HOME/extensions/AccessControl

# Modify LocalSettings.php
ADD config/enigma/LocalSettings.txt /tmp/LocalSettings.txt
RUN cat /tmp/LocalSettings.txt >> $MW_HOME/LocalSettings.php

# Configure Apache Server
RUN sed -i "s/Listen 80/Listen $HTTP_PORT/" /etc/apache2/ports.conf
RUN echo "ServerName $HTTP_SERVER" >> /etc/apache2/apache2.conf
EXPOSE $HTTP_PORT

# Configure Mysql Server
RUN sed -i "s/\[mysqld\]/\[mysqld\]\\nskip-grant-tables/" /etc/mysql/mariadb.conf.d/*-server.cnf

# Import Enigma Ontology on the wiki
ADD scripts/import_ontology.sh /tmp/import_ontology.sh
RUN service mysql start && \
	service apache2 start &&  \
	/tmp/import_ontology.sh "http://$HTTP_SERVER:$HTTP_PORT/$WIKI_PATH" "$ADMIN_USER" "$ADMIN_PW" "$ONT_URL" && \
	php $MW_HOME/maintenance/runJobs.php && \
	service apache2 stop && \
	service mysql stop

# Start Apache & Mysql Servers, and go to terminal
CMD service apache2 start && service mysql start && /bin/bash
