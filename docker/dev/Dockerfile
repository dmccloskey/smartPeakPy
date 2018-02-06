FROM dmccloskey/docker-openms:develop
USER root

# install PTVS
EXPOSE 3000
RUN pip3 install --no-cache-dir \
		ptvsd==3.0.0 \
		optlang \
	&&pip3 install --upgrade

USER user

# # RUN:
# docker run -v //C/path_to_data/Data/:/home/user/Data/
#  //C/path_to_repo/smartPeak/:/home/user/code/
#  dmccloskey/docker-pyopenms-vscode:develop python /home/user/code/debug_local.py