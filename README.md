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

To be sure that code changes do not break the build in master branch, the [spush](/git/spush) command must be executed to push commits. It's especially useful when many people work on the same codebase.

    # To be executed in the root directory of the Git repository
    spush

Codebase is forked, built then committed changes are pushed to the remote branch if the build passes. Forking in another directory allows developer to continue working and editing code in his workspace.

Build automatically executes the script `build.sh` if it exists, else it executes `mvn clean install`

## Eclipse Configuration

Eclipse settings are available in the directory [/eclipse](/eclipse).

### Imports

[sonar-formatter.xml](/eclipse/sonar-formatter.xml):
positions new lines, comments, spaces, parentheses, etc. To be imported in Window > Preferences > Java > Code Style > Formatter.

[sonar.importorder](/eclipse/sonar.importorder):
organizes the "import" lines. To be imported in Window > Preferences > Java > Code Style > Organize Imports.

[sonar-cleanup.xml](/eclipse/sonar-cleanup.xml):
cleans up the code, by organizing imports, formating source code, correcting indentation, etc.
To be imported in Window > Preferences > Java > Code Style > Clean Up. If additionally you want to perform clean up at every "save" action, check the checkboxes in Window > Preferences > Java > Editor > Save Actions.

[junit-templates.xml](/eclipse/junit-templates.xml) (optional):
defines shortcuts "temp" and "thrown" in the unit tests. To be imported in Window > Preferences > Java > Editor > Template.

### Additional Configuration

In Window > Preferences > Maven > Errors/Warnings, set "Plugin execution not covered by lifecycle execution" to "Ignore". This will silence out error messages when importing your Maven projects

On Windows, in Window > Preferences > General > Workspace, set "Text file encoding" to "UTF-8" and "New text file line delimiter" to "Unix".

## Code Style Configuration for Intellij

Intellij IDEA users must install the plugin [Eclipse Code Formatter](http://plugins.jetbrains.com/plugin/?id=6546) and import Eclipse settings files:
* check the "Use the Eclipse code formatter" option and use [sonar-formatter.xml](/eclipse/sonar-formatter.xml) as the Eclipse Java Formatter config file
* check the "From file" option in the "Import order" section and use [sonar.importorder](/eclipse/sonar.importorder)

![Intellij code style](/intellij/intellij-code-style.png)

IDEA must also be manually configured for imports : Preferences > Editor > Code Style > Java > Imports
* Class count to use import with '*'" -> 999
* Names count to use static import with '*' -> 999
* Import Layout
  * import all other imports
  * &lt;blank line&gt;
  * import static all other imports

![Intellij imports](/intellij/intellij-imports.png)

Eclipse 4.4 formatter support must not be enable in order to use recent versions of the Eclipse Code Formatter plugin (at least 4.5.1):

![enable Eclipse 4.5.1 formatter](/intellij/intellij-eclipse-formatter_4_5_1.png)

## Plugin (Almost) Hot Deploy

SonarQube 4.3 allows to quickly restart server when the development mode is enabled (sonar.dev=true in conf/sonar.properties). It's used to deploy a new version of the plugin under development. It's a bit faster than restarting the server in a standard way (JRuby environment is not reloaded). Execute the following command from plugin sources :

    mvn package org.codehaus.sonar:sonar-dev-maven-plugin::upload -DsonarHome=/path/to/server/home -DsonarUrl=http://localhost:9000

Note that the default value of sonarUrl is http://localhost:9000.
