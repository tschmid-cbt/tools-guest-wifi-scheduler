# Guest Wifi Scheduler

This tool runs on a server at HQ and allows anyone with an AD account to schedule the Guest WIFI for up to 8 hours.  The WIFI password is rolled each time and emailed to the user & the IT team.

[[https://github.com/tschmid-cbt/tools-guest-wifi-scheduler/images/cbt-guest-index.png|alt=screenshot]]

### Prerequisites

To run properly we need Apache and Python3.  This installation used a CentOS7 host.

Apache requires the cbt-tools.conf file and the following modules:
```
LoadModule ldap_module modules/mod_ldap.so
LoadModule authnz_ldap_module modules/mod_authnz_ldap.so
LoadModule ssl_module modules/mod_ssl.so
```

The credentials need to be supplied to bind to AD.  These should be added to /etc/httpd/conf.d/deets - restrict access to deets via:
```
chmod chmod o-rwx deets
```

Update the credentials for Reggie as well - file deets.py - also update emailAddrs if anyone else wishes to be added to notifications.

Python3's requirements can be satisfied with:
```
yum -y install python36u python36u-pip
/usr/bin/pip3 install requirements.txt
```

Make sure SSL cert is copied to directory - if not get it from nuggdrive2/DEVOPS_IT/devops/Certificates/cbt-nuggets/wildcard.cbt.nuggets.cer & .key
The cert and key would then need to be copied to /etc/ssl/certs/

### Installation

Copy the files to the appropriate place
```
mkdir /opt/wifi-scheduler
mv tools-cbt-guest-wifi-scheduler /opt/wifi-scheduler
cd /opt/wifi-scheduler/
mv cbt-tools.conf /etc/httpd/conf.d/
mv wifi-enabler.service /etc/systemd/system/
mv wifi-webfront.service /etc/systemd/system/
```

Reload Apache and Start Services
```
systemctl restart httpd
systemctl daemon-reload
systemctl enable wifi-enabler
systemctl enable wifi-webfront
systemctl start wifi-enabler
systemcty start wifi-webfront
```

Update the DNS Alias to point to the new server.

## Verify tool is up and running.

Login to https://cbt-guest.cbt.nuggets with your AD password.
You should now be able to run a test Schedule to verify functionality.

### Break down into end to end tests

A successful test would include:
 * User can login with AD password.
 * WIFI is scheduled & shows up under [View Schedule](https://cbt-guest.cbt.nuggets/view_schedule)
 * User receives an email from Reggie with correct password.
 * WIFI network is removed upon schedule completion.

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [CentOS7](https://www.centos.org/) - the brains
* [Apache2](https://httpd.apache.org/) - the beauty
* [Python3](https://www.python.org/) - the brawn

## License

This project is licensed under the Apache license - see the [https://github.com/tschmid-cbt/tools-guest-wifi-scheduler/LICENSE.md](LICENSE.md) file for details
