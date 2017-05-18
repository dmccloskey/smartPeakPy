##Dockerfile
#https://hub.docker.com/r/ducatel/visual-studio-linux-build-box/

FROM dmccloskey/docker-openms:latest
EXPOSE 3000
USER root
COPY docker-entrypoint.sh /usr/local/bin/
RUN ln -s /usr/local/bin/docker-entrypoint.sh / && chmod +x /usr/local/bin/docker-entrypoint.sh
RUN apt-get update && \
	apt-get install -y openssh-server g++ gdb gdbserver sudo build-essential git && \
	mkdir /var/run/sshd && \
    ##sets the user/password to root/toor
	echo 'root:toor' | chpasswd && \
	# sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
	# sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd && \
	sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
	sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config && \
	apt-get clean

USER user

CMD ["docker-entrypoint.sh"]