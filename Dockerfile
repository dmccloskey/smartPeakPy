FROM dmccloskey/docker-openms:AbsoluteQuantitation
USER root

EXPOSE 3000
RUN pip3 install --no-cache-dir \
		optlang \
	&& pip3 install --upgrade && \
	mkdir /home/user/code
COPY smartPeak /home/user/code/smartPeak
COPY tests /home/user/code/tests
COPY main.py /home/user/code/main.py

USER user

# # RUN:
# docker run -v //C/path_to_data/Data/:/home/user/Data/
#  dmccloskey/smartpeak:latest python /home/user/code/debug_local.py