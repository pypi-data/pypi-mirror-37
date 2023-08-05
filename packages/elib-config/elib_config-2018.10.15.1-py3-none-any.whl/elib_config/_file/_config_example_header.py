# coding=utf-8
"""
Header template for the example config file
"""

# flake8: noqa

HEADER = r'''This is an example configuration file for {app_name}.

Version: {app_version}.

WARNING: this example file will be overwritten every time {app_name} starts. Make sure to save your work under another 
name!

It must be renamed to "{config_file_path}" in order to come into effect.

The configuration file follows the TOML format specification.

Mandatory and optional values
=============================

Some values are mandatory, some aren't. Mandatory values are marked with the "MANDATORY VALUE" tag. If mandatory values
are missing, {app_name} will not start.

Note that, while not necessary for {app_name} to function, failing to provide non-mandatory values may prevent 
non-essential modules to start.

OS environment
==============

All configuration values may also be given using the OS environment instead of the config file. However, 
the "{app_name}_" prefix must be added (this is to prevent any potential conflict with other application.

For example, the configuration "dummy_key: dummy_value" would be set in the OS environment using the variable
"{app_name}_DUMMY_KEY=dummy_value".

Values types
=============

Value types will be checked at runtime.

TOML specification
==================

The full TOML specification can be found at: 

Here's an example taken from the readme:

####################################################################
# This is a TOML document.

title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00 # First class dates

[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
connection_max = 5000
enabled = true

[servers]

  # Indentation (tabs and/or spaces) is allowed but not required
  [servers.alpha]
  ip = "10.0.0.1"
  dc = "eqdc10"

  [servers.beta]
  ip = "10.0.0.2"
  dc = "eqdc10"

[clients]
data = [ ["gamma", "delta"], [1, 2] ]

# Line breaks are OK when inside arrays
hosts = [
  "alpha",
  "omega"
]
####################################################################
'''
