FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip \
                                               libxml2 \
                                               libxml2-dev \
                                               libxslt1-dev \
					       python3-setuptools
RUN pip3 install setuptools \
		 slackclient \
                 robobrowser \
                 lxml \
                 yapsy

ARG slack_token
ARG packtpub_login
ARG packtpub_pass

ENV SCRAPPER_SLACK_TOKEN=$slack_token
ENV PACKTPUB_LOGIN=$packtpub_login
ENV PACKTPUB_PASS=$packtpub_pass

RUN mkdir -p  /opt/slackscrapper/
COPY * /opt/slackscrapper/
RUN chmod +x /opt/slackscrapper/Scrapper.py
ENTRYPOINT ["python3","/opt/slackscrapper/Scrapper.py"]



