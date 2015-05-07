#!/usr/bin/env bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <mirror path> <cache path>"
    exit 1
fi

# set -x # echo executing statements (debug)
set -e # exit on subcommand errors
set -u # exit on unassigned variables

mirror_path="$1"
[ -d $mirror_path ] || { echo "ERROR: unable to find mirror path $mirror_path."; exit 1; }

cache_path="$2"
[ -d $cache_path ] || mkdir -p $cache_path

pushd $mirror_path &>/dev/null
for repo in $(ls -d *); do
    create_repo=0

    [ -d $repo/repodata ] || create_repo=1
    repodata_time=$(/usr/bin/stat --print='%Y' $repo/repodata)

    if [ $create_repo -eq 0 ]; then
        repo_dir=$repo
        [ -d "$repo/Packages" ] && repo_dir="$repo/Packages"
        repo_time=$(/usr/bin/stat --print='%Y' $repo_dir)
        [ $repo_time -gt $repodata_time ] && create_repo=1
    fi

    if [ $create_repo -ne 0 ]; then
        pushd $repo &>/dev/null
        /usr/bin/createrepo --verbose --database --update --cachedir=$cache_path $(pwd)
        popd &>/dev/null
    fi
done
popd &>/dev/null

# END