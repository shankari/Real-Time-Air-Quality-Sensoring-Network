#!/bin/bash

twistd --logfile logs/twitter_post.log --pidfile logs/twitter_pid.log -n smap conf/twitter_conf.ini