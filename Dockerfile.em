FROM @os:@codename
MAINTAINER "Tully Foote<tfoote@@osrfoundation.org"

RUN apt-get update
RUN apt-get install -qy apt-src devscripts

RUN echo "deb http://packages.ros.org/ros/ubuntu trusty main" > /etc/apt/sources.list.d/ros-latest.list
RUN echo "deb-src http://packages.ros.org/ros/ubuntu trusty main" >> /etc/apt/sources.list.d/ros-latest.list
ADD https://raw.githubusercontent.com/ros/rosdistro/master/ros.key /tmp/ros.key
RUN apt-key add /tmp/ros.key

# echo to invalidate caching
RUN echo "Adding dependencies @build_depends"
RUN apt-get update
@[for dep in build_depends]
RUN apt-get install -yV @dep
@[end for]

RUN mkdir /dbuilder
WORKDIR /dbuilder
ADD dbuilder.sh /dbuilder/dbuilder.sh
ENTRYPOINT ["/dbuilder/dbuilder.sh"]
