---
hostname: runciman
fqdn: runciman.hacksoc.org
name: Shell Server
---

A plain-text version of this README can be found on `runciman.hacksoc.org:/README`.

Runciman is a shell server maintained by [HackSoc](https://www.hacksoc.org) for the use of members of the society (with some functionality restricted to paid members).

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

<!-- BM AUP 404's - TODO find updated link -->
All users with shell accounts are required to have read the Bytemark [Acceptable Usage Policy](https://www.bytemark.co.uk/support/terms/aup/). Any users who we (or Bytemark) believe to be in violation of this, or who are otherwise causing any problem which affects other users, will receive a warning, and may lose their account

## Hosting
<!-- this is just plain inaccurate, README.webspace is more up-to-date -->
All users with a shell account have ~/public_html and ~/public_gopher directories, and files placed there will appear at {http,gopher}://runciman.hacksoc.org/{~,1users/}$user. This space is subject to the same disk quota as usual.

## Mumble
There is a mumble server (VoIP) server available.
<!-- not for much longer >:) -->

## Sponsorship
This server has been very kindly given to us by Bytemark, who are a wonderful company and you should definitely check them out.

[![Bytemark](https://runciman.hacksoc.org/bytemark_logo_411_x_31.png)](https://www.bytemark.co.uk/r/hacksoc)