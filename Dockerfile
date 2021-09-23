FROM continuumio/miniconda3
LABEL maintainer="weberdak"

ENV PYTHONBUFFERED 1

EXPOSE 8888

COPY ./scripts /scripts

RUN apt-get update && apt-get -y install tcsh && \
	rm -rf /var/lib/apt/lists/* && \
 	mkdir /spartaplus && cd /spartaplus && \
	wget http://spin.niddk.nih.gov/bax/software/SPARTA+/sparta+.tar.Z && \
	tar -zxvf sparta+.tar.Z && cd SPARTA+ && \
	chmod +x install.com && ./install.com && \
	rm /spartaplus/sparta+.tar.Z && \
	conda install jupyter && \
	conda install -c conda-forge mdtraj && \
  	mkdir /app /data && \
	useradd -ms /bin/bash app && \
	chown -R app:app /data /app && \
	chmod -R 755 /data /app && \
	chmod -R +x /scripts

ENV SPARTAP_DIR=/spartaplus/SPARTA+
ENV PATH="$PATH:$SPARTAP_DIR/bin"
ENV PYTHONPATH=/app:$PYTHONPATH

WORKDIR /data

USER app
