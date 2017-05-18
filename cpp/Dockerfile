##Dockerfile
#https://hub.docker.com/r/ducatel/visual-studio-linux-build-box/

FROM dmccloskey/docker-openms:latest
EXPOSE 3000
USER root
COPY docker-entrypoint.sh ./docker-entrypoint.sh
RUN apt-get update && \
	apt-get install -y openssh-server g++ gdb gdbserver sudo build-essential git && \
	# mkdir /var/run/sshd && \
	# echo 'root:toor' | chpasswd && \
	# sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
	# sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd && \
	# apt-get clean && \
    /usr/bin/ssh-keygen -A
USER user

ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["/usr/sbin/sshd", "-D"]