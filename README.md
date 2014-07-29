# Developer Toolset for Sonar-* Projects

Toolset for the developers contributing to http://github.com/SonarSource and http://github.com/SonarCommunity repositories.

## Git

If you have never used Git before, you need to do some setup first. Run the following commands so that Git knows your name and email.

    git config --global user.name "Your Name"
    git config --global user.email "your@email.com"

Setup line endings preferences:

    # For Unix/Mac users
    git config --global core.autocrlf input
    git config --global core.safecrlf true

    # For Windows users
    git config --global core.autocrlf true
    git config --global core.safecrlf true

The merge is working pretty well on small repositories (with move and rename of files). But it's not working on large repositories as the detection of file renaming is O(n²), so we need to update some threshold (more explanations are available in this post : http://blogs.atlassian.com/2011/10/confluence_git_rename_merge_oh_my/) :

    git config --global merge.renameLimit 10000
    
#### Commit messages

Commits must relate to a JIRA issue. Convention for messages inspired by http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html :

* The first line must be short (50 chars or less) and auto-descriptive in a format "<JIRA KEY> <DESCRIPTION>", for example "SONAR-1937 Code review"
* Write your commit message in the present tense: "Fix bug" and not "Fixed bug".
* The second line is blank.
* Next lines optionally define a short summary of changes (wrap them to about 72 chars or so).

Example :

    SONAR-2204,SONAR-2259 Fix URL encoding
    
    * For correct URL encoding we must encode parameters on lower level -
    in Query itself, but not in concrete implementation of Connector,
    because in Query we can distinguish concrete parts of URL.

    * Moreover in this case any additional encoding routines in Connector
    are useless, so were removed.


## The (Almost) Unbreakable Build

To be sure that code changes do not break the build in master branch, the [git-push](/git/git-push) command must be executed to push commits. It's especially useful when many people work on the same codebase. 

    # To be executed in the root directory of the Git repository
    git-push
    
Codebase is forked, built then committed changes are pushed to the remote branch if the build passes. Forking in another directory allows developer to continue working and editing code in his workspace.

Build automatically executes the script `build.sh` if it exists, else it executes `mvn clean install`

## Code Style

Eclipse settings are available in the directory [/eclipse](/eclipse). 
Intellij IDEA users must install the plugin [Eclipse Code Formatter](http://plugins.jetbrains.com/plugin/?id=6546) and import Eclipse settings files.

![Intellij code style](/intellij/intellij-code-style.png)
