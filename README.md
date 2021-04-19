# Akamai NetStorage Report

Python script to create a space usage report of directories of an Akamai NetStorage account and send it via email.

This script is most useful for resellers when they have access to a single storage group and have a sub-directory inside of it for each one of its customers.

## Prerequisites

* Python 2.7
* Akamai [NetStorageKit](https://pypi.org/project/NetStorageKit/) python module
* A SMTP server

## Usage

1. Configure your Akamai API credentials on `.netstoragekit.json`:

```
{
    "key_name": "kay_name",
    "key": "api_key",
    "host": "NS hostame",
    "cpcode": "Akamai cpcode"
}
```

2. Clone this repo and set the following environment variables:

* REMOTEPATH: Path inside the NetStorage account from where to start calculating the space usage. Default is /.
* SMTP_FROM= Email address to send the report from.
* SMTP_TO= Email address where to send the report.


3. Run the script:
```
$ python ./netstorage_report.py
```

### Sample Output

```
--------- ------ --------
NetStorage Report Program
--------- ------ --------


Sending report to: foo@bar.com

companyA          : 18.87 GB            
companyB          : 0 B                 
companyC          : 1.98 GB             
companyD          : 240.84 GB           
companyE          : 1.68 MB             
companyF          : 310.63 MB           

Total             : 262.01 GB
```

### Docker image

There is available a docker image that can be used to schedule the report using cron. Check out the [docker-compose.yml](docker-compose.yml) file to use it. To set the time for the report you can use the environment variable `CRONJOB_TIME` in cron format.
