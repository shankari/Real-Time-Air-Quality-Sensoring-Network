#!/bin/bash

nohup twistd --logfile logs/twitter_post.log --pidfile logs/twitter_pid.log -n smap conf/twitter_conf.ini >logs/twitter_driver.out 2>&1&
nohup twistd --logfile logs/safar_driver.log --pidfile logs/safar_pid.log -n smap conf/safar_conf.ini >logs/safar_driver.out 2>&1&