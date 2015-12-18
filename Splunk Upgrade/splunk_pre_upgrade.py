#!/usr/bin/env python
import os, json, ConfigParser

def read_time_conf(conf_file):
    """
    Extract the last finish time from the time.conf file and
    calculate the start and end time for the script
    """
    print 'Reading the conf file, %s' % (conf_file)
    try:
        f = open(conf_file, 'rb')
    except IOError as e:
        print 'Conf file, %s Reading Failed!' % conf_file
        raise
    data = f.readlines()
    f.close()
    time_params = {}
    for line in data:
        try:
            line.strip()
            if len(line) > 1:
                info = line.split('=')
                key = info[0].strip()
                val = info[1].strip('\r\n')
                val = info[1].strip()
                time_params[key] = val
        except Exception as e:
            print 'Conf file, %s contains corrupted data. [Details: %s]'\
                % (conf_file, str(e))
    print 'Time parameters has been read successfully: [%s]' % time_params
    return time_params

def update_conf(section, options):
    """
    update the conf table
    """
    LOCAL_CONFIG = "%s/etc/apps/iSIGHTPartners_ThreatScape_App/local/iSIGHTPartners_ThreatScape_App.conf" % os.environ['SPLUNK_HOME']
    try:
        if os.path.exists(LOCAL_CONFIG):
            print "Reading configuration file:    %s" % LOCAL_CONFIG
            config = ConfigParser.ConfigParser()
            config.read(LOCAL_CONFIG)
            if not config.has_section(section):
                config.add_section(section)
            for option, value in options.iteritems():
                config.set(section, option, value)
            conf_file = open(LOCAL_CONFIG, 'w')
            config.write(conf_file)
            conf_file.close()
            print '%s conf is successfully updated with values : %s' % (conf_file , json.dumps(options))
    except Exception, ex:
        print "Unable to read iSIGHT Parnters configuration files."
        raise

if __name__ == '__main__':
    """
    Pre-requisite check
    1. Check if $SPLUNK_HOME environment variable is set or not.
    2. Set path of all the destination directories as per SPLUNK_HOME
    """
    print "Checking if SPLUNK_HOME is set"
    if "SPLUNK_HOME" in os.environ:
        print "SPLUNK_HOME is set"
    else:
        print ("SPLUNK_HOME env variable is not set. Please set the SPLUNK_HOME path")
        splunk_home = raw_input('SPLUNK_HOME [Directory where splunk server is installed ex: /opt/splunk] = ')
        # Error Checking
        while not (splunk_home or splunk_home.strip() or splunk_home == ''):
            splunk_home = raw_input('SPLUNK_HOME [Directory where splunk server is installed ex: /opt/splunk] = ')
    
        if (splunk_home == ''):
            splunk_home = "/opt/splunk"
        os.environ['SPLUNK_HOME'] = splunk_home

    SPLUNK_BIN_DIR = os.environ['SPLUNK_HOME'] + "/etc/apps/iSIGHTPartners_ThreatScape_App/bin"
    params = read_time_conf(SPLUNK_BIN_DIR + '/isight_indicators.conf')
    update_conf('isight_indicators', params)
    params = read_time_conf(SPLUNK_BIN_DIR + '/isight_iocs.conf')
    update_conf('isight_iocs', params)

    if os.system("rm -r %s/*"%(SPLUNK_BIN_DIR)) == 0:
        print "Cleanup done Successfully"
    else:
        print "Cleanup Failed"
