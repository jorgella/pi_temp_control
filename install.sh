#!/bin/bash

sudo cp -r . /opt/fancontrol

sudo cp fancontrol.service /usr/lib/systemd/system/

sudo chmod u+x /usr/lib/systemd/scripts/fancontrol.sh

sudo systemctl daemon-reload

sudo systemctl enable --now fancontrol