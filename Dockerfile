FROM ubuntu:trusty
MAINTAINER "Tully Foote<tfoote@osrfoundation.org"

RUN apt-get update
RUN apt-get install -qy apt-src

RUN echo "deb http://packages.ros.org/ros/ubuntu trusty main" > /etc/apt/sources.list.d/ros-latest.list
ADD https://raw.githubusercontent.com/ros/rosdistro/master/ros.key /tmp/ros.key
RUN apt-key add /tmp/ros.key

RUN mkdir /dbuilder
WORKDIR /dbuilder
ADD dbuilder.sh /dbuilder/dbuilder.sh
ENTRYPOINT ["/dbuilder/dbuilder.sh"]
