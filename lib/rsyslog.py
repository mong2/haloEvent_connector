import lib.validate as validate
import lib.loadyaml as loadyaml

try:
    import syslog
except ImportError:
    import socket

class Rsyslog(object):
    def __init__(self):
        self.operating_system = validate.operating_system()
        self.rsys = loadyaml.load_rsyslog()
        self.portal = loadyaml.load_portal()
        self.host = self.portal["windows_syslog_host"]
        self.port = self.portal["windows_syslog_port"]
        self.facility = None
        self.priority = None

    def parse_facility(self, facility_option):
        facility, priority = facility_option.split(",")
        self.facility = self.rsys["facility"][self.operating_system][facility]
        self.priority = self.rsys["level"][priority]

    def linux_openlog(self):
        syslog.openlog('cpapi', 0, self.facility)

    def linux_syslog(self, data):
        syslog.syslog(self.priority, data)

    def windows_openlog(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def windows_syslog(self, data):
        self.windows_openlog().sendto('<%d>%s' % (self.priority + self.facility*8, data), (self.host, self.port))

    def windows_closelog(self):
        self.windows_openlog().close()

    def process_openlog(self, facility_option):
        self.parse_facility(facility_option)
        if self.operating_system is 'linux':
            return self.linux_openlog()
        return self.windows_openlog()

    def process_syslog(self, data):
        for i in data:
            if self.operating_system is 'linux':
                self.linux_syslog(i)
            else:
                self.windows_syslog(i)

    def closelog(self):
        if self.operating_system is 'windows':
            return self.windows_openlog().close()

