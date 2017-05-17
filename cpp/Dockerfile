##Dockerfile
#https://hub.docker.com/r/ducatel/visual-studio-linux-build-box/

FROM dmccloskey/docker-openms:latest
EXPOSE 3000
USER root
RUN apt-get update && \
	apt-get install -y openssh-server gdb gdbserver sudo build-essential git && \
	mkdir /var/run/sshd && \
	echo 'root:toor' | chpasswd && \
	sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
	sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd && \
	apt-get clean	
USER user
	
#useradd -m -d /home/<user-name>/ -s /bin/bash -G sudo <user-name>
#passwd <user-name>

CMD ["/usr/sbin/sshd", "-D"]