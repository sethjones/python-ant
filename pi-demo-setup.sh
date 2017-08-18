#!/bin/bash
#title          :pi-demo-setup.sh
#description    :Script will install prerequisites for ant-demo.py
#author		 	:Seth Jones
#email			:sajones4@oakland.edu
#date           :20170818
#version        :0.1
#usage		 	:execute ./pi-demo-setup.sh
#notes          :Requires internet connection and root
#bash_version   :4.3.30(1)-release
#==============================================================================

# Check if user is Root.
if [ `id -u` -eq 0 ]; then
	# Check for active internet connection.
	nc -z 8.8.8.8 53  >/dev/null 2>&1
	connected=$?
	if [ $connected -eq 0 ]; then
		echo "Active internet connection detected. Continuing setup..."
	    # Create the USB rules so that it activates on insert.  May be redundant.
		if [ -e /etc/udev/rules.d/ant-usb.rules ]; then
		  echo "File ant-usb.rules already exists!"
		else
		  echo "SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"0fcf\", ATTRS{idProduct}==\"1008\", RUN+=\"/sbin/modprobe usbserial vendor=0x0fcf product=0x1008\", MODE=\"0666\", OWNER=\"pi\", GROUP=\"root\"" > /etc/udev/rules.d/ant-usb.rules
		fi

	    # Setup Python environment.
	    echo "Installing python-setuptools."
		apt-get -qq update
		apt-get install -y python-setuptools

		# Install Python-Ant
		echo "Cloning python-ant library."
		git clone -b 20170813 https://github.com/sethjones/python-ant.git /usr/bin/python-ant
		cd /usr/bin/python-ant/
		python /usr/bin/python-ant/setup.py install

		# TODO
		# Add auto start of HRM listener upon startup.
	else
		echo "Offline! Please connect an internet connection."
	fi
else
    echo "Please run using sudo, or as ROOT"
    exit 1
fi