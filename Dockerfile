FROM python:3.9.6
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y apt-utils && apt-get install -y opus-tools && apt-get install -y ffmpeg
#  | tee /logs/my-install-cmd.log
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD backend_youtube_dl.py /usr/local/lib/python3.9/site-packages/pafy
ADD ffmpeg.exe /usr/local/lib
ADD ffmpeg.exe /app
COPY . /app
# RUN apt-get update   
# RUN apt-get update && apt-get install -y openssh-server
# RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
# RUN useradd -m -s /bin/bash sshuser

# ENTRYPOINT service ssh start && bash
# RUN echo "sshuser:Changeme" | changepasswd
# COPY id_rsa.pub /home/sshuser/.ssh/authorized_keys
# RUN chown -R sshuser:sshuser /home/sshuser/.ssh
# RUN chmod 600 /home/sshuser/.ssh/authorized_keys