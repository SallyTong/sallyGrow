As you may know our postgresql image can’t restart when you restart docker. This is very painful when you have lots of data in this db.

This morning I meet this situation. After struggling for some hours, I got a solution. Now share with you, hope it is useful.

Steps as below:

1.	Postgresql looks like:
docker@default:~$ docker ps -a

CONTAINER ID        IMAGE                                                         COMMAND             CREATED             STATUS   PORTS          NAMES
8b3e135d54ea        cnshdocker.sh.cn.ao.ericsson.se/bolte/bmc-postgresql:latest   "bash initdb"    5 days ago          Exited (0) 10 minutes ago   postgresql
2.	Because initdb can’t run successfully twice. So we need to replace initdb file. Prepare initdbNew file, the content as below:
   .....
3.	Copy initdbNew to postgresql container
   $ docker cp initdbNew postgresql:initdbNew

4.	Edit postgresql configuration file, Change all initdb to initdbNew in config.json file
docker@default:~$ sudo -s
root@default:/home/docker# cd /var/lib/docker/containers/8b3e135d54ea…
root@default:/mnt/sda1/var/lib/docker/containers/8b3e135d54eaf62ee950c3c57ea6b67629e91aa872c9522381bd66254b167c3b# vi config.json
5.	Restart the docker service:
$ docker-machine restart default
6.	List your containers and make sure the command has changed:
docker@default:~$ docker ps -a
CONTAINER ID        IMAGE                                                         COMMAND             CREATED             STATUS   PORTS          NAMES
8b3e135d54ea        cnshdocker.sh.cn.ao.ericsson.se/bolte/bmc-postgresql:latest   "bash initdbNew "    5 days ago          Exited (0) 15 minutes ago   postgresql
7.	Start the postgresql container, then you will see postgresql can start successfully.
