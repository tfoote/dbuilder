This is a proof of concept for building debian packages inside of docker.

To build a package execute:

`python dbuilder.py DEBIAN-PACKAGE-NAME [DEBIAN-PACKAGE-NAME2 ...]`

TODOs
-----

 * To be more generic we need to add multi arch support.
 * It should use a Docker instance for generating the Dockerfile to operate upon.
 * The apt-sources should be parameterized (also currently required on your host, move to docker above)
  * url and keys
 * The timestamping of packages should be optional. Possibly injected as a hook like pbuilder.
 * There should be real tempfiles used. Not foo*
 * Review the caching logic
 * Fix/parameterize the output directory 
