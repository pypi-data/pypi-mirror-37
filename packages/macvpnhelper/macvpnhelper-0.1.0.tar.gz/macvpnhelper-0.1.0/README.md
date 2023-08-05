INSTALLATION
------------
1)  Homebrew
  a) Install Homebrew (if you don't have it)
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  b) Update Homebrew
    brew update && brew upgrade
2) Install python3
  brew install python
3) Install package
  pip3 install macvpnhelper

Run by typing "macvpnhelper" in the terminal.

Alternatively, you can run the script located in this package directly. It is located in the bin/ folder.
  ./macvpnhelper
  
NOTE: You will be prompted for keychain access for storing/retrieving the user, password, and vpn name.

UPDATING
--------
  pip3 install --upgrade macvpnhelper
or
  pip3 uninstall macvpnhelper
  pip3 --no-cache-dir install macvpnhelper

USAGE
-----
usage: macvpnhelper [-h] [--duration DURATION] [--clickspeed CLICKSPEED]
                    [--fillpassword FILLPASSWORD] [--warning WARNING]
                    [--interval INTERVAL] [--simulate] [--reset] [--vpn VPN]

Examples:
      macvpnhelper
  Uses existing defaults of --warning=yes --duration=fd --clickspeed=normal.  The app will display a warning (which must be clicked) before filling password information and stop executing at 6pm.

      macvpnhelper --fillpassword=andReturn --warning=no --clickspeed=fast --interval=3
  Fills password prompt and doesn't warn that it is doing so (could type password into a different active dialog!), clicks dialog buttons quickly (use on fast machine)

      macvpnhelper --reset --vpn="ISS Wi-fi" --duration=3h
  Clears existing user/password information and defines a new VPN name. Runs for 3 hours before terminating.

optional arguments:
  -h, --help            show this help message and exit
  --duration DURATION, -d DURATION
                        (time in hours|'wd'|'fd'|'runOnce') E.g., 8h, the amount of time (in hours) to keep the VPN active. Use 'wd' to do 9-12 and 1-6 (default), 'fd' to do 9-6, and 'runOnce' to do a single check and then terminate.
  --clickspeed CLICKSPEED, -cs CLICKSPEED
                        (superfast|fast|normal|slow|superslow) adjust based on responsiveness of your GUI
  --fillpassword FILLPASSWORD, -fp FILLPASSWORD
                        (yes|no|andReturn) type in password and optionally hit return in the dialogs.  CAUTION: since this password is provided to the GUI, it is possible that intermediate clicks will result in your password being typed to, e.g., chat dialogs. Prevent this by using 'yes' instead of 'andReturn', or making sure the clickspeed matches your GUI responsiveness.
  --warning WARNING, -w WARNING
                        (yes|no) Displays warning message prior to filling in password.
  --interval INTERVAL, -i INTERVAL
                        number of seconds to wait between polling connection status (default is 5)
  --simulate, -s        When set, script which would be executed is instead printed to the terminal.
  --reset               Use to reset your login information.
  --vpn VPN, -n VPN     Name of VPN to connect to. Must match your configured connection.