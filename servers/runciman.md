---
hostname: runciman
fqdn: runciman.hacksoc.org
name: Shell Server
---

A plain-text version of this README can be found on `runciman.hacksoc.org:/README`.

Runciman is a shell server maintained by [HackSoc](https://www.hacksoc.org) for the use of members of the society. 

## Shell Accounts
Shell accounts are only available for paid members of the society, in order to request one either speak to a member of the committee, or email [hack@yusu.org](mailto:hack@yusu.org)

To prevent abuse, accounts are restricted. There are three tiers, which currently differ only in the process limit:

<dl>
    <dt>small</dt>
    <dd>1.5GB disk, 6GB RAM, 50 processes</dd>
    <dt>medium</dt>
    <dd>1.5GB disk, 6GB RAM, 150 processes</dd>
    <dt>large</dt>
    <dd>1.5GB disk, 6GB RAM, 500 processes</dd>
</dl>

All new accounts start out small, but if you need more resources, and can explain why, you may be able to get an upgrade.

All users with shell accounts are required to have read the Bytemark [Acceptable Usage Policy](https://www.bytemark.co.uk/terms/aup/). Any users who we (or Bytemark) believe to be in violation of this, or who are otherwise causing any problem which affects other users, will receive a warning, and may lose their account.

## Hosting
All users with a shell account have `~/public_html` and `~/private_html` directories:
 - `~/public_html`: https://runciman.hacksoc.org/~user/ , directory contents **are listed**
 - `~/private_html`: https://runciman.hacksoc.org/~/user/ , directory contents **not listed**
  
This space is subject to the same disk quota as usual.

## IRC bouncer
There is a [ZNC] server running on Runciman, speak to your Infrastructure Officer to get an account set up (available to all paying members). Connect from your IRC client via:
- `irc.hacksoc.org:6667` - plaintext
- `irc.hacksoc.org:7000` - SSL (recommended)

## Minecraft server
There is a vanilla Minecraft server (1.12.2) running on Runciman, connect on `runciman.hacksoc.org` (default port). If it's whitelisted, speak to your Infrastructure Officer or put a message in Slack.

## Scheduled downtime
Runciman is scheduled to reboot at 4AM on the second Monday of each month. Services or tmuxes that you leave running will be killed, make sure they can come back up!

## Sponsorship
This server has been very kindly given to us by Bytemark, who are a wonderful company and you should definitely check them out.

[![Bytemark](https://runciman.hacksoc.org/bytemark_logo_411_x_31.png)](https://www.bytemark.co.uk/r/hacksoc)

[ZNC]: https://wiki.znc.in/ZNC