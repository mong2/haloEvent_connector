#Halo Event Connector

###Required package:
Cloudpassage SDK:

Install from pip with `pip install cloudpassage`. If you want to make modifications to the SDK you can install it in editable mode by downloading the source from this github repo, navigating to the top directory within the archive and running pip install -e . (note the . at the end). Or you can visit https://github.com/cloudpassage/cloudpassage-halo-python-sdk to clone it directly from our github.

###Intro - Quick Start
In this repo we have included the pdf documentation for using these scripts to pull Halo event alerts into either Sumo Logic or Splunk - however, you will just as easily be able to integrate Halo events into other popular SIEM tools, such as ArcSight, or with your Syslog infrastructure.

In addition, there are several ways you can run this script to stream event data to your desired target.

For example, let's say, you wanted to setup this script to be run from cron, emit Halo events as key-value name pairs and append them to a file on the local filesystem. And you wanted to pull only those events that were logged since Nov 10, 2012 onwards. And instead of using the script defaults where the files are expected to be in the program directory, let's say you wanted to use a different working directory /opt/cloudpassage, for example.

For that, you would do something like this:

Run crontab -e and add a line with the desired schedule, such as the following to run, say every 5 minutes

```
*/5 * * * * /opt/cloudpassage/bin/haloEvents.py --starting=2012-11-10 --auth=/opt/cloudpassage/config/myHaloKeys.auth --configdir=/opt/cloudpassage/config --kvfile=/opt/cloudpassage/logs/eventsInKVFormat >/dev/null 2>&1
```

Save your changes before you exit.

If you are extracting events from more than one (supports up to 5) Halo accounts, you can specify those in your myHaloKeys.auth file like this:

```
key_id_1|secret_1
key_id_2|secret_2
...
...
key_id_5|secret_5
```

```
usage: haloEvents.py [-h] [--starting STARTING] --auth AUTH
                     [--threads THREADS] [--batchsize BATCHSIZE]
                     [--configdir CONFIGDIR] [--jsonfile JSONFILE]
                     [--ceffile CEFFILE] [--leeffile LEEFFILE]
                     [--kvfile KVFILE] [--facility FACILITY] [--cef] [--kv]
                     [--leefsyslog] [--cefsyslog] [--kvsyslog]

Event Connector

optional arguments:
  -h, --help            show this help message and exit
  --starting STARTING   Specify start of event time range in ISO-8601 format
  --auth AUTH           Specify a file containing CloudPassage Halo API keys -
                        Key ID and Key secret pairs (up to 5)
  --threads THREADS     Start num threads each reading pages of events in
                        parallel
  --batchsize BATCHSIZE
                        Specify a limit for page numbers, after which we use
                        since
  --configdir CONFIGDIR
                        Specify directory for configration files (saved
                        timestamps)
  --jsonfile JSONFILE   Write events in raw JSON format to file with given
                        filename
  --ceffile CEFFILE     Write events in CEF (ArcSight) format to file with
                        given filename
  --leeffile LEEFFILE   Write events in LEEF (QRadar) format to file with
                        given filename
  --kvfile KVFILE       Write events as key/value pairs to file with given
                        filename
  --facility FACILITY   --facility=<faility,priority> Facility options:auth
                        authpriv cron daemon kern local0 local1 local2local3
                        local4 local5 local6 local7 lpr mail news sysloguser
                        uucp Priority options: alert crit debug emerg errinfo
                        notice warning [default: user,info]
  --cef                 Write events in CEF (ArcSight) format to standard
                        output (terminal)
  --kv                  Write events as key/value pairs to standard output
                        (terminal)
  --leefsyslog          Write events in LEEF (QRadar) format to syslog server
  --cefsyslog           Write events in CEF (ArcSight) format to syslog server
  --kvsyslog            Write events as key/value pairs to local syslog daemon
```



<!---
#CPTAGS:community-supported integration archive
#TBICON:images/python_icon.png
-->
