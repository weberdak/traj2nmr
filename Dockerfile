FROM continuumio/miniconda3
LABEL maintainer="weberdak"

ENV PYTHONBUFFERED 1

EXPOSE 8888

ARG DEBIAN_FRONTEND=noninteractive

COPY ./scripts /scripts
COPY ./dependencies /dependencies

RUN apt-get update && apt-get -y install tcsh && \
	rm -rf /var/lib/apt/lists/* && \
 	cd /dependencies && tar -zxvf sparta+.tar.Z && \
	cd SPARTA+ && chmod +x install.com && \
	./install.com && rm /dependencies/sparta+.tar.Z && \
	cd /dependencies && tar -xvf ppm_linux.tar && rm ppm_linux.tar && \
	conda install jupyter && \
	conda install -c conda-forge mdtraj && \
  	mkdir /app /data && \
	useradd -ms /bin/bash app && \
	chown -R app:app /data /app /dependencies && \
	chmod -R 755 /data /app && \
	chmod -R +x /scripts

ENV SPARTAP_DIR=/dependencies/SPARTA+
ENV PATH=$PATH:$SPARTAP_DIR/bin:/dependencies/ppm_linux
ENV PYTHONPATH=/app:$PYTHONPATH

WORKDIR /data

USER app
