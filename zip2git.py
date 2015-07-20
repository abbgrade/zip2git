"""
zip2git converts a set of backups in zip archives into a git repository.

## Contribution

For questions or improvements visit [the GitHub Page](https://github.com/abbgrade/zip2git).

## Requirements

It uses [PythonGit](https://github.com/gitpython-developers/GitPython), which requires a git installation.
Under Windows an entry for git in the PATH variable is necessary.

## Usage

zip2git uses two directories. One that contains the backup zip archives and another restore directory that will contain the git repository.
The contents of the restore directory will be deleted in runtime.
The backup archive filenames need to have the backuped directory name as prefix to the first underscore. If your file schema is different you have to change this script.

### Example

    Backup
    - scripts_20150716.zip
    - scripts_20150717.zip
    - scripts_20150718.zip
    - docs_20150716.zip
    - docs_20150717.zip
    - docs_20150718.zip

Will be converted to a git repository like:

    Restore
    - scripts
      - a
      - b
    - docs
      - x
      - y

## Documentation

The documentation uses [pycco](https://github.com/abbgrade/pycco).
Generate it with the following command:

    python ..\pycco\pycco\main.py -d .\doc .\zip2git.py

"""

backup_path = 'Backup'
restore_path = 'Restore'

import os
import zipfile
import git

# # Runtime

# ## Open Git Repo
#
# Create the git repository or use the existing.

repo = None

if not os.path.exists(restore_path):
    os.mkdir(restore_path)

try:
    repo = git.Repo(restore_path)
except:
    repo = git.Repo.init(restore_path)

# ## List Archives 
#
# List the files in the backup directory ordered by modification time.

files = []

for file in os.listdir(backup_path):
    files.append((os.path.getmtime(os.path.join(backup_path, file)), file))

files.sort(key = lambda a: a[0])
files = list(zip(*files)[1])

# ## Restore and Commit
#
# Restore each zip archive and commit the changes to the git repository if not already committed.

commits = []
try:
    commits = [commit.message.strip() for commit in repo.iter_commits(repo.active_branch)]
except:
    print 'could not select previous commits'

for file in files:
    if file in commits:
        print 'skip', file
        continue

    folder = file.split('_')[0]
    
    with open(os.path.join(backup_path, file), 'rb') as zip_handle:
     
        # Clean the restore directory.

        if os.path.exists(os.path.join(restore_path, folder)):
            for delete_root, delete_folders, delete_files in os.walk(os.path.join(restore_path, folder), topdown=False):
                for name in delete_files:
                    os.remove(os.path.join(delete_root, name))
                for name in delete_folders:
                    os.rmdir(os.path.join(delete_root, name))
        
        # Iteratre over the files in the archive.

        z = zipfile.ZipFile(zip_handle)
        for name in z.namelist():

            # Create the subdirectories.
            
            destination_path = os.path.join(restore_path, folder, name.decode('CP437').replace('/', os.path.sep))
            destination_path_parts = destination_path.split(os.path.sep)
            for part_index in range(1, len(destination_path_parts)):
                destination_sub_path = os.path.sep.join(destination_path_parts[:part_index])
                if not os.path.exists(destination_sub_path):
                    os.mkdir(destination_sub_path)

            # Restore the file.

            with open(destination_path, 'wb') as outfile:
                outfile.write(z.read(name))
                
        zip_handle.close()

    # Add the new files to the git repository.

    repo.index.add(repo.untracked_files)
    
    # Commit the changes.

    print 'commit', file
    repo.git.commit(m=file)
