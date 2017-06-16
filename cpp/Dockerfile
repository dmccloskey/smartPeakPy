##Dockerfile
#https://hub.docker.com/r/ducatel/visual-studio-linux-build-box/

FROM dmccloskey/docker-openms:latest
##gbd port fowarding
EXPOSE 3000
##connection via sshd
# EXPOSE 22
USER root
COPY docker-entrypoint.sh /usr/local/bin/
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive && \
	apt-get install -y \
	gawk \
	openssh-server \
	gdb \
	gdbserver \
	sudo \
	build-essential \
	git \
	# Qt dev packages
	# qtconnectivity5-dev \
	# qtmobility-dev \
	# qtmultimedia5-dev \
	# libqt5opengl5-dev \
	# qtpositioning5-dev \
	# qtdeclarative5-dev \
	# qtscript5-dev \
	# libqt5svg5-dev \
	qtbase5-dev \
	qttools5-dev && \
	## openssh-server is required for sshd connection
	## gdbserver is required for debug (attach)
	## gawk is a requirement for GLIB_2.18 workaround (below)
	mkdir /var/run/sshd && \
    ##sets the user/password to root/toor
	##needed for connection using sh
	echo 'root:toor' | chpasswd && \
	sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
	sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd && \
	# sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
	# sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config && \
	apt-get clean && \
    rm -r /var/lib/apt/lists/* && \
	##change permissions
	ln -s /usr/local/bin/docker-entrypoint.sh / && \
	chmod +x /usr/local/bin/docker-entrypoint.sh
	# chmod +x /usr/bin/gdbserver
	# ##create a soft link to the OpenMS include path
	# mkdir /home/user/code && \
	# ln -s /usr/local/OpenMS/src/openms/include/OpenMS /home/user/code/OpenMS

# USER user
CMD ["docker-entrypoint.sh"]