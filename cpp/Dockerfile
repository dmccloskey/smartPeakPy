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
	apt-get install -y gawk openssh-server gdb gdbserver sudo build-essential git && \
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
# #GLIB_2.18 workaround for vscode (testing)
# #https://github.com/Microsoft/vscode-cpptools/issues/19
# # COPY Microsoft.VSCode.CPP.Extension.linux.sh ~/.vscode/extension/ms-vscode.cpptools-0.9.3/bin
# RUN unset LD_LIBRARY_PATH && \
# 	mkdir /home/user/tmp && \
# 	cd /home/user/tmp && \
# 	wget http://ftp.gnu.org/gnu/glibc/glibc-2.18.tar.xz && \
# 	tar xvf glibc-2.18.tar.xz && \
# 	cd glibc-2.18 && \
# 	mkdir build && \
# 	cd build && \
# 	../configure --prefix=/opt/glibc-2.18 && \
# 	sudo make install && \ 
# 	rm -rf glibc-2.18.tar.xz
# 	# && \
# 	# chmod a+x Microsoft.VSCode.CPP.Extension.linux.sh && \
# 	# Modify "~/.vscode/extensions/ms-vscode.cpptools-0.9.3/out/src/LanguageServer/C_Cpp.js"
# 	# Change the following line from " extensionsProcessName += '.linux'; " to " extensionProcessName += '.linux.sh'; "
# ENV LD_LIBRARY_PATH /usr/local/openms-build/lib/:$LD_LIBRARY_PATH

# USER user
CMD ["docker-entrypoint.sh"]