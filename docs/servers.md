# Writing server READMEs

| **You should know** |                     |
|---------------------|---------------------|
| Essential:          | Markdown formatting |

These pages appear at the hostname of each server (ie https://runciman.hacksoc.org) and provide some information about the servers to anyone curious. Information is written in Markdown. Files should be named after each server (eg `runciman.md`) and placed in `templates/content/servers`. Server READMEs were often updated by "pinging" a webhook on each server to tell it that the website had updated so that it could fetch the new README to serve. Whether this system is still in operation is unknown.

## Frontmatter
The server READMEs use more frontmatter than most pages.
 - `hostname`: The name of this server, in lowercase, eg `runciman`
 - `fqdn`: the Fully-Qualified Domain Name of this server, eg `runciman.hacksoc.org`
 - `name`: a short summary of the purpose of this server, eg `Shell Server`