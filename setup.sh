echo Installed
sudo systemctl enable ./systemd/lead_transfer.service
poetry install --without=dev
