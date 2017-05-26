#!/bin/bash          
echo Tool Operator Shutting Down

sudo supervisorctl stop all
sudo shutdown now