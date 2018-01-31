#!/usr/bin/env bash

set -euo pipefail

sonarqube_url=https://next.sonarqube.com/sonarqube

# TODO
sonarqube_auth=admin:admin

# A GitHub API token with visibility on private SonarSource projects; used by this script for parameter validation
# TODO
github_auth=username:token

# The GitHub API token for the PR decoration user
github_token=TODO

org=default-organization

projects() {
   # public projects
    cat << EOF
org.jenkins-ci.plugins:sonar SonarSource/sonar-scanner-jenkins
org.sonarsource.analyzer-commons:sonar-analyzer-commons-parent SonarSource/sonar-analyzer-commons
org.sonarsource.auth.github:sonar-auth-github-plugin SonarSource/sonar-auth-github
foo bar
org.sonarsource.dotnet:sonar-csharp SonarSource/sonar-csharp
org.sonarsource.flex:flex SonarSource/sonar-flex
org.sonarsource.github:github-api SonarSource/github-api
org.sonarsource.github:sonar-github-plugin SonarSource/sonar-github
org.sonarsource.graph:source-graph-viewer SonarSource/source-graph-viewer
org.sonarsource.java:java SonarSource/sonar-java
org.sonarsource.javascript:javascript SonarSource/SonarJS
org.sonarsource.java:sonar-java-debugging-rules-plugin SonarSource/java-debugging-rules
org.sonarsource.ldap:sonar-ldap SonarSource/sonar-ldap
org.sonarsource.orchestrator:orchestrator-parent SonarSource/orchestrator
org.sonarsource.php:php SonarSource/sonar-php
org.sonarsource.python:python SonarSource/sonar-python
org.sonarsource.scanner.ant:ant SonarSource/sonar-scanner-ant
org.sonarsource.scanner.api:sonar-scanner-api-parent SonarSource/sonar-scanner-api
org.sonarsource.scanner.cli:sonar-scanner-cli SonarSource/sonar-scanner-cli
org.sonarsource.scanner.gradle:sonarqube-gradle-plugin SonarSource/sonar-scanner-gradle
org.sonarsource.scanner.maven:sonar-maven-plugin SonarSource/sonar-scanner-maven
org.sonarsource.scanner.vsts:sonar-scanner-vsts SonarSource/sonar-scanner-vsts
org.sonarsource.scm.cvs:sonar-scm-cvs-plugin SonarSource/sonar-scm-cvs
org.sonarsource.scm.git:sonar-scm-git SonarSource/sonar-scm-git
org.sonarsource.scm.svn:svn SonarSource/sonar-scm-svn
org.sonarsource.sonar-classloader:sonar-classloader SonarSource/sonar-classloader
org.sonarsource.sonarlint.core:sonarlint-core-parent SonarSource/sonarlint-core
org.sonarsource.sonarlint.eclipse:sonarlint-eclipse-parent SonarSource/sonarlint-eclipse
org.sonarsource.sonarlint.intellij:sonarlint-intellij SonarSource/sonarlint-intellij
org.sonarsource.sonarlint.vscode:sonarlint-vscode SonarSource/sonarlint-vscode
org.sonarsource.sonar-lits-plugin:lits SonarSource/sonar-lits
org.sonarsource.sonar-packaging-maven-plugin:sonar-packaging-maven-plugin SonarSource/sonar-packaging-maven-plugin
org.sonarsource:sonar-persistit SonarSource/sonar-persistit
org.sonarsource.sonarqube:sonarqube SonarSource/sonarqube
org.sonarsource.sslr-squid-bridge:sslr-squid-bridge SonarSource/sslr-squid-bridge
org.sonarsource.sslr:sslr SonarSource/sslr
org.sonarsource.update-center:sonar-update-center SonarSource/sonar-update-center
org.sonarsource.web:web SonarSource/sonar-web
org.sonarsource.xml:xml SonarSource/sonar-xml
sonaranalyzer-csharp-vbnet SonarSource/sonar-csharp
sonarlint-visualstudio SonarSource/sonarlint-visualstudio
sonarqube-roslyn-sdk SonarSource/sonarqube-roslyn-sdk
sonar-scanner-msbuild SonarSource/sonar-scanner-msbuild
sonarts SonarSource/SonarTS
EOF

    # private projects
    # TODO enter here before running. Do not commit to SCM.
    cat << EOF
EOF
}

projects_test() {
    cat <<EOF
sample SonarSource/sonarqube
sample bar
foo bar
foo SonarSource/sonarqube
sample SonarSource/sonar-java
EOF
}

check_repo() {
    curl -u "$github_auth" -s https://api.github.com/repos/$repo -I | head -n1 | grep -q 200
}

echo "Verifying that all specified projects exist on GitHub..."
all_ok=yes
while read key repo; do
    check_repo || {
        all_ok=no
        echo "Could not find GitHub repo: $repo for $key" >&2
        continue
    }
done < <(projects)

if [ "$all_ok" != yes ]; then
    echo "Validation failed, aborting." >&2
    exit 1
fi

while read key repo; do
    echo "Updating project $key at $repo ..."
    curl -u "$sonarqube_auth" "$sonarqube_url/api/settings/set?component=$key&key=sonar.pullrequest.token.secured&value=$github_token" -X POST
    curl -u "$sonarqube_auth" "$sonarqube_url/api/settings/set?component=$key&key=sonar.pullrequest.repository&value=$repo" -X POST
done < <(projects)
