#!/bin/bash

ln -s $PWD fancontrol

sudo mv fancontrol /opt

sudo cp fancontrol.service /usr/lib/systemd/system/

sudo cp fancontrol.sh /usr/lib/systemd/scripts/

sudo chmod u+x /usr/lib/systemd/scripts/fancontrol.sh

sudo systemctl daemon-reload

sudo systemctl enable --now fancontrol
