#!/bin/bash

twitter_pid=`cat logs/twitter_pid.log`
safar_pid=`cat logs/safar_pid.log`
aqi_pid=`cat logs/aqi_pid.log`

sudo kill -9 $twitter_pid
sudo kill -9 $safar_pid
sudo kill -9 $aqi_pid
