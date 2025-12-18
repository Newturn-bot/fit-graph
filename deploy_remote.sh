#!/usr/bin/env bash
# Small wrapper to copy repo files to a remote server and run the provided deploy.sh there.
# Usage: ./deploy_remote.sh user@host /remote/path

set -eu
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 user@host /remote/path [ssh-key-path]"
  exit 2
fi

REMOTE="$1"
REMOTE_PATH="$2"
SSH_KEY_ARG=""
if [ "$#" -ge 3 ]; then
  SSH_KEY="$3"
  if [ -f "$SSH_KEY" ]; then
    SSH_KEY_ARG="-i $SSH_KEY"
  else
    echo "Warning: SSH key $SSH_KEY not found; proceeding with default ssh agent/keys"
  fi
fi

FILES=(fitgraph_complete_integration.py requirements.txt Dockerfile docker-compose.yml deploy.sh deploy_remote.sh .env.example README.md)

echo "Copying files to ${REMOTE}:${REMOTE_PATH}..."
for f in "${FILES[@]}"; do
  scp $SSH_KEY_ARG "$f" "${REMOTE}:${REMOTE_PATH}/"
done

echo "Running deploy on remote host..."
ssh $SSH_KEY_ARG "$REMOTE" "mkdir -p ${REMOTE_PATH} && cd ${REMOTE_PATH} && chmod +x deploy.sh && ./deploy.sh"

echo "Remote deploy finished. Check logs on remote with: ssh ${REMOTE} 'cd ${REMOTE_PATH} && docker-compose logs -f'"
