# zip2git

## Requirements

It uses PythonGit, which requires a git installation.
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
