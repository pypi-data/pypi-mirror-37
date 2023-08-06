Apeeper: The EC2 Metadata Service Token
==================================

Apeeper is an application which will run on your EC2 instance
and listen for requests (from the EC2 instance) to the meta data
service url of `http://169.254.169.254/`. 

Getting Started
---------------

Step 1: Create an Apeeper Factory Url on your Canary Console
Step 2: Copy the startup script supplied on your Canary Console into
        your ec2 instance's user data (so that it is run automagically on
        start-up). 
**NOTE:** We add apeeperd to your `/etc/rc.local` so that it continues to start
        automatically at each instance start up.
**or**
Step 2: run `yum update -y`
Step 3: run `yum install python python-pip -y`
Step 4: run `pip install apeeper` on your ec2 instance.
Step 3: run `apeeperd -a <factory_url> [-b <comma-separated blacklist>| -w <comma-separated whitelist>]` where
        you MUST only choose to whitelist or blacklist. These lists are comma separated paths. The `factory_url`
        is supplied to your by your Canary Console.
Step 4: run `echo 'apeeperd -s' >> /etc/rc.local` to ensure that apeeper starts up on subsequent instance start ups.
Step 5: run `chmod +x /etc/rc.local` to make sure that the file is executable.

NB Notes to running Apeeper
---------------------------

1) Please check `/tmp/apeeper.log` for errors or debugging.
2) Apeeper must be run as root because it uses iptables.
3) Once again, whitelist and blacklist CANNOT be used together. Please only specify one at a time.

Usage
-----
Running apeeper as vanilla (it will alert on any request to `http://169.254.169.254/`).
`$ apeeperd -a <factory_url>`

Or, you can run apeeper, blacklisting suspicious paths, causing apeeper to alert when a
path requested starts with that,
`$ apeeperd -a <factory_url> -b '/latest/user-data,/latest/network/`

Or, you can run apeeper, whitelisting known used paths, causing apeeper to alert on anything
other then those supplied paths,
`$ apeeperd -a <factory_url> -w '/latest/`

Please note that both sets of paths, whitelist and blacklist, can be comma separated.