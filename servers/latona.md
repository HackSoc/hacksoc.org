---
hostname: latona
fqdn: latona.hacksoc.org
name: Storage Server
uoy: yes
---

<!-- name is temporary before names are voted on -->

Latona <!-- let's go away--> is a storage server maintained by [HackSoc](https://www.hacksoc.org) for the use of members of the society. 

## Storage
Storage shares are available to paid members of the society*, in order to request one either message your [infrastructure officer][about] or email [hack@yusu.org](mailto:hack@yusu.org).

Storage shares are **50GB** per member.  
Storing pornographic material or content that infringes copyright is stricly forbidden; members found to be in breach of these rules will have their account removed (including other HackSoc accounts), and may be reported to the University.

**users must also be current members of the university.*

## Connecting
Mounting shares is done over SSH. There is no shell access (for that, see [runciman] server).

### On-campus
To connect on-campus, use the following command:
```
sshfs <hacksocuser>@latonahacksoc: <mountpoint>
```
Where `<hacksocuser>` is your HackSoc username, and `<mountpoint>` is the folder on the local computer you want to mount your share to. This must be an empty directory. You may run into issues if you are using a computer managed by ITS (eg `csteach1` or a lab PC) and try to mount to a folder in your home directory, as your home directory itself is mounted from another server. The most robust method is to create a folder in `/tmp` to mount to, and then optionally create a symlink in your home directory.

### Off-campus
Latona is hosted in the University Data Center, which means it is behind the campus firewall. In order to access it off-campus, use the uni [SSH service]. Once registered with the SSH service, you can use a command like the following to mount Latona.

```
sshfs <hacksocuser>@latonahacksoc: <mountpoint> -o ProxyJump=<itsuser>@ssh.york.ac.uk 
```
Where `<hacksocuser>` is your HackSoc username, `<mountpoint>` is the mount point on your computer (as before), and `<itsuser>` is your IT Services username (same as your student email address).  
The SSH service accepts public key authentication, so you may wish to add your public keys to `~/.ssh/known_hosts` on your university account to speed up this step.

[about]: https://hacksoc.org/about.html
[runciman]: https://runciman.hacksoc.org
[SSH service]: https://www.york.ac.uk/it-services/services/ssh/