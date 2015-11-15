#!/bin/bash

twistd --logfile logs/twitter_post.log --pidfile logs/twitter_pid.log -n smap conf/twitter_conf.ini &
twistd --logfile logs/safar_driver.log --pidfile logs/safar_pid.log -n smap conf/safar_conf.ini &