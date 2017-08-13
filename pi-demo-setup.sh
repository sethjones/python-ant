#!/bin/bash
if [ `id -u` -eq 0 ]
then
    # Create the USB rules so that it activates on insert.  May be redundant.
	if [ -e /etc/udev/rules.d/ant-usb.rules ]; then
	  echo "File ant-usb.rules already exists!"
	else
	  echo "SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"0fcf\", ATTRS{idProduct}==\"1008\", RUN+=\"/sbin/modprobe usbserial vendor=0x0fcf product=0x1008\", MODE=\"0666\", OWNER=\"pi\", GROUP=\"root\"" > /etc/udev/rules.d/ant-usb.rules
	fi

    # Setup Python environment.
	apt-get update
	apt-get install -y python-setuptools

	# Install Python-Ant
	git clone -b 20170813 https://github.com/sethjones/python-ant.git /usr/bin/python-ant
	cd /usr/bin/python-ant/
	python /usr/bin/python-ant/setup.py install

	# TODO
	# Add auto start of HRM listener upon startup.
else
        echo "Please run using sudo, or as ROOT"
        exit 1
fi
