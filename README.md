# TELNET SCANNER / BRUTER
- made by dalas_16., contributed by \_hackerbob\_
(reach us on [discord](https://discord.com/app))


## join the Discord server : https://discord.gg/4ZnMFruApm
DD*S, BULLETPROOF VPS and much more !    

## SETUP
- Buy or use a Vps/dedicated server, with preferably a unmetered / 10 Gbps internet connection.
- install python (preferably the latest version)
- Upload every file to the vps and run the below commands on it.
- Run `pip install -r requirements.txt` to install the required modules.
- Run `python scan.py <folder_name>` with a chosen folder_name. WARNING: You might need to run the script as root.
This will scan for IPs that have the 23 port opened, it might take a long time, depending on your internet connection.
When you are satisfied with the number of ips, hit CTRL+C.
- Run `python brute.py <same_folder_name>`
This will try to brute force the diffrent found IPs.
- Enjoy your free bots !
Need help with our script ? join the discord    

## Advanced:
Depending on your vps capabilities, you might want to adapt the number of workers in brute.py, 
as well as modifying the "zmap" command in scan.py to ensure maximum script performance.



### Changelog:
Type hint added,    
Help messages added,    
Better syntax,    
added support for multiple scans at the same time,    
Added bandwitdh limiter to zmap, to prevent overusage of bandwitdh (Can be tweaked in scan.py)    
Lowered amount of workers (Better for less powerful servers)    
Argument usage instead of calling input() -> enable automation    
Custom telnet implementation this telnetlib is deprecated in python 3.13    
Memory efficient ip loading in brute, no need to load possibly millions of ips into the ram :)    

### Final words
Tested (and working) on a rasberry pi 4, running debian

nice loading bar go brrr