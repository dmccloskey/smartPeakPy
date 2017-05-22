FROM dmccloskey/docker-openms:latest
EXPOSE 3001
USER root
RUN pip3 install --no-cache-dir \
		ptvsd \
	&&pip3 install --upgrade
USER user