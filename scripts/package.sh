#!/bin/sh
# Build the zip to upload to claude.ai (Plugins in the left sidebar > Add > Upload plugin).
# It holds only what the plugin needs: the manifest, the skills, the README, the
# changelog and the licence (LICENSE and NOTICE).
# docs/, tests/ and scripts/ stay out, since everyone the plugin is shared with
# receives every file in the upload.
#
# scripts/package.sh                    the release in .claude-plugin/plugin.json
# scripts/package.sh --dev 0.3.1-dev.1  a test build: the same files, with that
#                                       pre-release version in the zip's manifest
#                                       only, so it can be told apart once synced
set -eu

root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"

dev=
if [ "${1:-}" = --dev ]; then
  dev=${2:-}
  case $dev in
    [0-9]*.[0-9]*.[0-9]*-?*) ;;
    *) echo "--dev needs a pre-release version, such as 0.3.1-dev.1" >&2; exit 2 ;;
  esac
fi

src=$root
if [ -n "$dev" ]; then
  src=$(mktemp -d)
  trap 'rm -rf "$src"' EXIT
  cp -R .claude-plugin skills README.md CHANGELOG.md LICENSE NOTICE "$src"
  python3 -I - "$src/.claude-plugin/plugin.json" "$dev" <<'EOF'
import json, sys
path, version = sys.argv[1], sys.argv[2]
with open(path, encoding='utf-8') as f:
    manifest = json.load(f)
manifest['version'] = version
with open(path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
    f.write('\n')
EOF
fi

version=$(python3 -I -c 'import json, sys; print(json.load(open(sys.argv[1]))["version"])' "$src/.claude-plugin/plugin.json")
out="$root/dist/github-curator-$version.zip"

if command -v claude >/dev/null 2>&1; then
  claude plugin validate "$src"
else
  echo "claude CLI not found: the manifest was not validated" >&2
fi

mkdir -p dist
rm -f "$out"
cd "$src"
# The zip is the plugin alone: marketplace.json serves Claude Code's marketplace from GitHub.
zip -r -X -q "$out" .claude-plugin skills README.md CHANGELOG.md LICENSE NOTICE -x '*.DS_Store' -x '.claude-plugin/marketplace.json'
echo "Built $out"
unzip -l "$out"
