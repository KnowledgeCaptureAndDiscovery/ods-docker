#!/bin/bash

SERVER=$1
USERNAME=$2
PASSWORD=$3
ONTURL=$4

API=$SERVER/api.php
INDEX=$SERVER/index.php
COOKIE="/tmp/cookies.txt"

echo "Logging into the Wiki.."
TOKEN=`curl -c $COOKIE "$API?action=query&meta=tokens&type=login" 2>/dev/null| grep "logintoken" | cut -f 4 -d '"' | cut -f 1 -d '+'`
RESPONSE=`curl -b $COOKIE -c $COOKIE -X POST -d "action=clientlogin&loginreturnurl=$INDEX&logintoken=$TOKEN%2B%5C&username=$USERNAME&password=$PASSWORD" $API 2>/dev/null | grep "status" | cut -f 4 -d '"'`

echo "Loading the ontology from $ONTURL.."
curl -b $COOKIE -X POST -d "op=bootstrap&onturl=$ONTURL" "$INDEX/Special:WTBootstrap" >/dev/null
