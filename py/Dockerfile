FROM dmccloskey/docker-openms:AbsoluteQuantitation
USER root

# install PTVS
EXPOSE 3000
RUN pip3 install --no-cache-dir \
		ptvsd==3.0.0 \
		optlang \
	&&pip3 install --upgrade

USER user