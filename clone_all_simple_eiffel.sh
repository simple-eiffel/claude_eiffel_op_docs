#!/bin/bash
# Clone ALL simple-eiffel repositories from GitHub
# Run from: ~/simple_eiffel (will be created if doesn't exist)

set -e

TARGET_DIR="$HOME/simple_eiffel"
ORG="simple-eiffel"

echo "=== Cloning ALL Simple Eiffel Libraries to $TARGET_DIR ==="
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

# All repositories in the simple-eiffel organization
REPOS=(
    claude_tools
    eiffel_sqlite_2025
    simple_ai_client
    simple_alpine
    simple_app_api
    simple_archive
    simple_base64
    simple_cache
    simple_ci
    simple_cli
    simple_clipboard
    simple_codec
    simple_compression
    simple_config
    simple_console
    simple_cors
    simple_crypto
    simple_csv
    simple_datetime
    simple_decimal
    simple_docker
    simple_eiffel_parser
    simple_encryption
    simple_env
    simple_file
    simple_foundation_api
    simple_fraction
    simple_github_runner
    simple_graph
    simple_grpc
    simple_gui_designer
    simple_hash
    simple_HTMX
    simple_http
    simple_http_client
    simple_i18n
    simple_ipc
    simple_json
    simple_jwt
    simple_k8s
    simple_logger
    simple_lsp
    simple_markdown
    simple_math
    simple_mmap
    simple_mongo
    simple_mq
    simple_notebook
    simple_oracle
    simple_pdf
    simple_pkg
    simple_platform_api
    simple_process
    simple_randomizer
    simple_rate_limiter
    simple_regex
    simple_registry
    simple_scheduler
    simple_service_api
    simple_setup
    simple_showcase
    simple_smtp
    simple_sql
    simple_system
    simple_telemetry
    simple_template
    simple_testing
    simple_toml
    simple_toon
    simple_ucf
    simple_uuid
    simple_validation
    simple_watcher
    simple_web
    simple_websocket
    simple_win32_api
    simple_xml
    simple_yaml
)

echo "Found ${#REPOS[@]} repositories to clone"
echo ""

SUCCESS=0
SKIPPED=0
FAILED=0

for repo in "${REPOS[@]}"; do
    if [ -d "$repo/.git" ]; then
        echo "[$repo] Already cloned, pulling latest..."
        cd "$repo"
        git pull --quiet && echo "  Updated." || echo "  Pull failed (maybe offline)"
        cd ..
        ((SKIPPED++))
    elif [ -d "$repo" ]; then
        echo "[$repo] Directory exists but not a git repo - removing and cloning fresh..."
        rm -rf "$repo"
        if git clone --quiet "https://github.com/$ORG/$repo.git"; then
            echo "  Cloned."
            ((SUCCESS++))
        else
            echo "  FAILED to clone!"
            ((FAILED++))
        fi
    else
        echo "[$repo] Cloning..."
        if git clone --quiet "https://github.com/$ORG/$repo.git"; then
            echo "  Cloned."
            ((SUCCESS++))
        else
            echo "  FAILED to clone!"
            ((FAILED++))
        fi
    fi
done

echo ""
echo "=== SUMMARY ==="
echo "New clones: $SUCCESS"
echo "Already existed (pulled): $SKIPPED"
echo "Failed: $FAILED"
echo ""
echo "Total libraries in $TARGET_DIR:"
ls -d */ 2>/dev/null | wc -l
