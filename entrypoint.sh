#!/bin/bash

set -e

if [[ $1 == "setup" ]]; then
    echo "Setting up cron..."
    CRON=${CRON:=0 * * * *}  # every hour
    echo "Cron used :: '${CRON}'"

    echo "${CRON} /app/entrypoint.sh run" >> /etc/crontabs/gungnir
    chmod 0644 /etc/crontabs/gungnir

    crontab /etc/crontabs/gungnir
    touch /var/log/cron.log

    echo "Setup complete!"

elif [[ $1 == "run" ]]; then
    echo "Running workload..."
    export PYTHONPATH=/app:/app/gungnir
    python -m gungnir --container

    exit 0
fi

echo "Waiting for cron to trigger..."
/usr/sbin/crond -f -l 8

