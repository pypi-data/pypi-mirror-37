===============================
neutron-bsn-lldp
===============================

LLDP Agent for Big Switch Networks integration.

This custom LLDP agent is used to send LLDPs on interfaces connected to
Big Cloud Fabric (BCF). In environments with os-net-config installed, it reads
config from os-net-config to automagically identify and send LLDPs.

For all other purposes, Big Switch Openstack Installer (BOSI) configures the
service file based on environment info.
