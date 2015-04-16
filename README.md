# CleanJira
Couple of scripts to remove stuff from Jira. By stuff I mean old projects, permission schemes and user groups.

# Remove projects

Script to remove projects specified in file. Script is used to remove old projects.
To find old projects run `old_projects.sql` in Jira DB. In my file I am looking for projects that were last time updated before 2013-01-01.

Then run Python script `remove_projects.py` :

"""
python remove_projects.py [-test|-live] <file-with-projects.txt>
"""
