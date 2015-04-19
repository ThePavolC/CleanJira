# CleanJira
Couple of scripts to remove stuff from Jira. By stuff I mean old projects, permission schemes and user groups.

- `./sql`
    - contains sql queries to get data for each script
    - contains sample data output from DB. Scripts are expecting the same file format as is in sample data
- `./src`
    - each script is located here
    - properties file`
    - `./utils` contains some helper functions
        - `files.py` handles file processing
        - `run_check.py` checks if there are all needed arguments when running script

# Remove projects

Script removes projects specified in file. Script is used to remove old projects.
To find old projects run `old_projects.sql` in Jira DB. In my file I am looking for projects that were last time updated before 2013-01-01.

Then run Python script `remove_projects.py` :

```
$ python remove_projects.py [-test|-live] <file-with-projects.txt>
```

# Remove user groups

Script removes user groups specified in file. To get user groups run query similar to the one in `usergroups.sql` in Jira DB.

Then run Python script `remove_usergroups.py` :

```
$ python remove_usergroups.py [-test|-live] <file-with-usergroups.txt>
```

# Remove permission schemes

Script removes permission schemes without projects. To find permission schemes run `permission_schemes_without_project.sql` in Jira DB.

Then run Python script `remove_permission_schemes.py` :

```
$ python remove_permission_schemes.py [-test|-live] <file-with-permission-schemes.txt>
```
