#!/usr/bin/env bash

set -euo pipefail

featureBranch=$(git rev-parse --abbrev-ref HEAD)
dogfoodBranch=dogfood/$featureBranch

info() {
    echo "* $@"
}

branchExists() {
    git rev-parse -q --verify "$1" >/dev/null
}

createDogfoodBranch() {
    git branch "$dogfoodBranch"
}

rebaseDogfoodBranch() {
    git checkout "$dogfoodBranch"
    git rebase "$featureBranch"
    git checkout -
}

if [ "$featureBranch" = "master" ]; then
    echo "You are on master, this script is intended to use on a feature branch. Exit."
    exit 1
fi

if branchExists "$dogfoodBranch"; then
    info "dogfood branch '$dogfoodBranch' exists, rebasing ..."
    rebaseDogfoodBranch
else
    info "dogfood branch '$dogfoodBranch' does not exist, creating ..."
    createDogfoodBranch
fi

info "pushing dogfood branch '$dogfoodBranch' to origin ..."
git push origin "$dogfoodBranch" --force-with-lease
