#!/usr/bin/env bash
set -euo pipefail

: "${DEPLOYED_URL:=https://daily-ninja-app.azurewebsites.net}"

curl -fsS "$DEPLOYED_URL/health"
curl -fsS "$DEPLOYED_URL/"

export DAILY_NINJA_BASE_URL="$DEPLOYED_URL"
python -m pytest daily_ninja_python/tests/integration/test_post_deploy.py -q

echo "Deployment verification passed for $DEPLOYED_URL"
