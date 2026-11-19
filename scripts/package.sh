#!/bin/sh
# Build the zip to upload to claude.ai (Customize > Plugins > Upload plugin).
# It holds only what the plugin needs: the manifest, the skills, the README and
# the licence (LICENSE and NOTICE).
# docs/, tests/ and scripts/ stay out, since everyone the plugin is shared with
# receives every file in the upload.
set -eu

root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"

version=$(python3 -I -c 'import json; print(json.load(open(".claude-plugin/plugin.json"))["version"])')
out="dist/github-curator-$version.zip"

if command -v claude >/dev/null 2>&1; then
  claude plugin validate "$root"
fi

mkdir -p dist
rm -f "$out"
zip -r -X -q "$out" .claude-plugin skills README.md LICENSE NOTICE -x '*.DS_Store'
echo "Built $out"
unzip -l "$out"
