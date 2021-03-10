# irccloud.self
A Self hosted version of the irc cloud script (Meant for people who want to setup stuff on their own)

- Be sure to have `python-dev` installed in your machine.  
- Clone the repository with `git clone https://github.com/vijaiaeroastro/irccloud.self.git`  
- Enter into the cloned repository with `cd irccloud`  
- Install the requirements with `python -m pip install -r requirements.txt`  
- If the above command fails, install `python-pip`  
- Use the bash script `irccloud_cronjob` provided for ease of use  
- You can also specify everything on a `crontab` entry instead. Just type `crontab -e`, choose your favourite text editor  
and add this to it (this will  be executed every hour):  
`0 * * * * cd $HOME/irccloud.self; IRCCLOUD_USERNAME="your@email.address" IRCCLOUD_PASSWORD="your_password" python3 $HOME/irccloud.self/irccloud.py; cd >/dev/null 2>&1`

**NOTE**: If you have a VPS running Linux, i assume you know how to use basic Linux commands. I would highly advise you to do what suits your workflow the most.

### Automated Solution

If you do not have a VPS / would prefer a more automated solution, have a look at 
[https://github.com/vijaiaeroastro/irccloud.git](https://github.com/vijaiaeroastro/irccloud.git)
