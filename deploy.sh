#!/usr/bin/env bash
# deploy.sh — Server-side deployment script for snapreeldownload.com
# Place this file at /opt/downloader/deploy.sh on the server.
# Run: bash deploy.sh
#
# This script verifies Docker compatibility before deploying to prevent
# "client version X.XX is too old" API mismatch errors.

set -euo pipefail

APP_DIR="/opt/downloader"
REQUIRED_DOCKER_API="1.44"
REQUIRED_COMPOSE_MAJOR=2

# ── Helpers ───────────────────────────────────────────────────────────────
log()   { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
error() { echo "[ERROR] $*" >&2; exit 1; }

# ── Pre-flight: Docker daemon ─────────────────────────────────────────────
log "Checking Docker daemon is running..."
docker info > /dev/null 2>&1 || error "Docker daemon is not running. Fix: sudo systemctl start docker"

# ── Pre-flight: Docker API version ───────────────────────────────────────
log "Checking Docker API version compatibility..."

CLIENT_API=$(docker version --format '{{.Client.APIVersion}}' 2>/dev/null || echo "0.0")
SERVER_API=$(docker version --format '{{.Server.APIVersion}}' 2>/dev/null || echo "0.0")

log "  Docker Client API : $CLIENT_API"
log "  Docker Server API : $SERVER_API"

python3 - <<PYEOF
import sys

def parse_ver(v):
    try:
        return tuple(int(x) for x in v.split('.'))
    except ValueError:
        return (0, 0)

client  = parse_ver("$CLIENT_API")
server  = parse_ver("$SERVER_API")
required = parse_ver("$REQUIRED_DOCKER_API")

ok = True
if client < required:
    print(f"FAIL: Docker client API $CLIENT_API < required $REQUIRED_DOCKER_API")
    ok = False
if server < required:
    print(f"FAIL: Docker server API $SERVER_API < required $REQUIRED_DOCKER_API")
    ok = False

if not ok:
    print("")
    print("Run the following on the server to upgrade Docker:")
    print("  sudo apt-get update")
    print("  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")
    sys.exit(1)

print(f"OK: Docker API versions are compatible (client=$CLIENT_API, server=$SERVER_API)")
PYEOF

# ── Pre-flight: Docker Compose Plugin (must be v2+) ───────────────────────
log "Checking Docker Compose Plugin version..."
COMPOSE_VERSION=$(docker compose version --short 2>/dev/null || echo "0.0.0")
COMPOSE_MAJOR=$(echo "$COMPOSE_VERSION" | cut -d. -f1)

if [ "$COMPOSE_MAJOR" -lt "$REQUIRED_COMPOSE_MAJOR" ]; then
    error "Docker Compose v$COMPOSE_VERSION is too old (need v2+). Fix: sudo apt-get install docker-compose-plugin"
fi
log "  Docker Compose    : v$COMPOSE_VERSION (OK)"

# ── Nginx config ──────────────────────────────────────────────────────────
log "Updating nginx configuration..."
sudo cp nginx/snapreeldownload.conf /etc/nginx/sites-available/snapreeldownload.conf
sudo nginx -t && sudo systemctl reload nginx
log "  nginx reloaded OK"

# ── Docker deploy ─────────────────────────────────────────────────────────
log "Rebuilding and restarting containers..."
docker compose up -d --build --force-recreate

# ── Cleanup ───────────────────────────────────────────────────────────────
log "Pruning dangling images..."
docker image prune -f

# ── Status report ─────────────────────────────────────────────────────────
log "✅ Deployment complete!"
echo ""
docker compose ps
