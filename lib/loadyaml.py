import os
import yaml

rsyslog_config = os.path.join(os.path.dirname(__file__), '../configs/rsyslog.yml')
portal_config = os.path.join(os.path.dirname(__file__), '../configs/portal.yml')
cef_config = os.path.join(os.path.dirname(__file__), '../configs/cef.yml')
leef_config = os.path.join(os.path.dirname(__file__), '../configs/leef.yml')

def load_rsyslog():
	return yaml.load(file(rsyslog_config, 'r'))

def load_portal():
	return yaml.load(file(portal_config, 'r'))

def load_cef():
	return yaml.load(file(cef_config, 'r'))

def load_leef():
	return yaml.load(file(leef_config, 'r'))