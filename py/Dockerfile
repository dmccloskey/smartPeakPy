FROM dmccloskey/docker-openms:latest
EXPOSE 3000
USER root
RUN pip3 install --no-cache-dir \
		ptvsd==3.0.0 \
	&&pip3 install --upgrade
USER user