FROM nvidia/cuda:11.1-base-ubuntu20.04
RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list
RUN apt-key del 7fa2af80
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/7fa2af80.pub
RUN apt-get update && apt-get install -y python3 && apt-get install -y python3-pip
RUN apt update && apt install -y python3 && apt install -y python3-pip
RUN apt install -y vim
RUN apt install -y git
RUN mkdir /configfiles
COPY docker_requirements.txt /configfiles
RUN pip3 install -r /configfiles/docker_requirements.txt

