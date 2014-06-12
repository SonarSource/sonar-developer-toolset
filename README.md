Developer Toolset for Sonar-* Projects
======================================

Toolset for the developers contributing to http://github.com/SonarSource and http://github.com/SonarCommunity repositories.

Git
---

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

Code Style
----------

Eclipse settings are available in the directory [/eclipse](/eclipse). 
Intellij IDEA users must install the plugin [Eclipse Code Formatter](http://plugins.jetbrains.com/plugin/?id=6546) and import Eclipse settings files.

![Intellij code style](/intellij/intellij-code-style.png)
