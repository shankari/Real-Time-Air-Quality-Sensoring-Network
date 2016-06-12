#!/bin/bash

./shut_drivers.sh
nohup twistd --logfile logs/safar_driver.log --pidfile logs/safar_pid.log -n smap conf/safar_conf.ini >logs/safar_driver.out 2>&1&
nohup twistd --logfile logs/twitter_post.log --pidfile logs/twitter_pid.log -n smap conf/twitter_conf.ini >logs/twitter_driver.out 2>&1&
nohup twistd --logfile logs/aqi_converter.log --pidfile logs/aqi_pid.log -n smap conf/aqi_converter_conf.ini >logs/aqi_driver.out 2>&1&
