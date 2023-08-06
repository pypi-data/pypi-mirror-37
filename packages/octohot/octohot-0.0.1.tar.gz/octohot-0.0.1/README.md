# octohot

A git command automation for multiple repositories

  #### Local Installation
    Clone
    ./build_local
    source venv/bin/activate

# First use

Create a octohot.yml in an empty folder with organization name, your token and a
repo list 
#### octohot.yml example  
    github_organization: Hotmart-Org
    github_token: <GITHUB_TOKEN>
    repositories:
    - git@github.com:organization/repo1.git
    - git@github.com:organization/repo2.git
    - git@github.com:organization/repo3.git

# Sync, replace and apply usage

    octohot sync # Clone, reset, delete unpushed Branches, pull all repos
    octohot regex find "[A-Z]*" # Find all upper case words
    octohot regex replace "[0-9]*" "" # remove all numbers
    octohot regex replace "foo" "bar" # remove matches  
    octohot apply # Pull, branch, add, commit, push and make a optional PR
   
# Main commands

Clone, reset, delete unpushed branches, pull all repos

    octohot sync
    
Pull, create branch, add, commit, push and make an optional PR on all branches

    octohot apply

# All Commands
    
    octohot --help

### git Provider

git provider for octohot

    octohot git --help
        
Create/Change branch in all repos

    octohot git branch

Clone all repos

    octohot git clone
    
Commit added changes in all repos

    octohot git commit
    
Get diff from all repos

    octohot git diff

Pull all repos

    octohot git pull
    
Push all repos    
    
    octohot git push
    
Reset all repos

    octohot git reset
     
### GitHub Provider

GitHub provider for octohot

    octohot github --help

Make a PR in all GitHub repos from a specific branch

    octohot github pr
    
Import all repositories to octohot.yml config file from a Organization from 
GitHub

    octohot github org import
    
List all repositories to octohot.yml config file from a Organization from 
GitHub

    octohot github org list
    
### RegEx Provider

Perl RegEx provider for octohot
    
    octohot git --help

Find a regular expression in all repos and list files and matches

    octohot regex find
     
Find and replace a string in all repos

    octohot regex replace 

## Contributing

Pull requests for new features, bug fixes and suggestions are welcome!

## License

GNU General Public License v3 (GPLv3)

