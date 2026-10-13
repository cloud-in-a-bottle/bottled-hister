#!/bin/sh
set -eu

: "${BOTTLE_APP_DATA_DIR:?Cloud in a Bottle must provide persistent app data}"
: "${BOTTLE_APP_NAME:?Cloud in a Bottle must provide the app name}"
: "${BOTTLE_ZONE_DOMAIN:?Cloud in a Bottle must provide the zone domain}"

export HISTER_DATA_DIR="$BOTTLE_APP_DATA_DIR"
export HISTER_CONFIG="$BOTTLE_APP_DATA_DIR/config.yml"
export HISTER__SERVER__ADDRESS="0.0.0.0:4433"
export HISTER__SERVER__BASE_URL="https://$BOTTLE_APP_NAME.$BOTTLE_ZONE_DOMAIN"

# The router authenticates the owner on every application route. Hister uses
# its single-user mode so the owner never sees a second login or signup form.
export HISTER__APP__ACCESS_TOKEN=""
export HISTER__APP__USER_HANDLING=false
export HISTER__APP__PUBLIC=false

exec /hister/hister "$@"
