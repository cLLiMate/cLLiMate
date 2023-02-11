#!/usr/bin/env bash
# read keys from the sops file relative to this script and export then as env vars

set -e

# get the directory of this script
cd $(dirname $0)/..

secrets=$(sops -d conf/secrets/tokens.json)
keys=$(echo $secrets | jq -r 'keys[]')
for key in $keys; do
    export $key=$(echo $secrets | jq -r ".$key")
done

echo "exported secrets:"
for key in $keys; do
    echo $key
done
