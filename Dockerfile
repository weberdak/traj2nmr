FROM continuumio/miniconda3
LABEL maintainer="weberdak"

ENV PYTHONBUFFERED 1

EXPOSE 8888

ARG DEBIAN_FRONTEND=noninteractive

COPY ./scripts /scripts
COPY ./dependencies /dependencies

RUN mkdir -p /usr/share/man/man1 && \
	apt-get update && apt-get -y install tcsh libomp-dev python2.7 default-jre && \
	rm -rf /var/lib/apt/lists/* && apt-get -y autoremove && \
 	cd /dependencies && tar -zxvf sparta+.tar.Z && \
	cd SPARTA+ && chmod +x install.com && \
	./install.com && rm /dependencies/sparta+.tar.Z && \
	cd /dependencies && mkdir ppm_linux && tar -xvf ppm_linux.tar -C ppm_linux && \
	rm ppm_linux.tar && \
	cd /dependencies && tar -xzvf shiftx2-v113-linux-20180808.tgz && \
	rm shiftx2-v113-linux-20180808.tgz && cd /dependencies/shiftx2-linux && \
	awk '{ gsub(/python/, "python2.7"); print }' shiftx2.py > temp && mv temp shiftx2.py && \
	chmod +x shiftx2.py && \
	conda install jupyter && \
	conda install -c conda-forge mdtraj matplotlib && \
  	mkdir /app /data && \
	useradd -ms /bin/bash app && \
	chown -R app:app /data /app /dependencies && \
	chmod -R 755 /data /app && \
	chmod -R +x /scripts

ENV SPARTAP_DIR=/dependencies/SPARTA+
ENV SHIFTX2_DIR=/dependencies/shiftx2-linux
ENV PPM_DIR=/dependencies/ppm_linux
ENV PATH=$PATH:$SPARTAP_DIR/bin:$SHIFTX2_DIR:$PPM_DIR
ENV PYTHONPATH=/app:$PYTHONPATH

WORKDIR /data

USER app
