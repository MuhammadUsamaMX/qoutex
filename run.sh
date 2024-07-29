curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && 

sudo dpkg -i cloudflared.deb && 

sudo cloudflared service install eyJhIjoiMTUzYWMyZjczZjNhMGM3NjJjZjE1MThhYzBlZDM1MTEiLCJ0IjoiYmQ5NWJkNDEtNTc2My00N2U4LTgwYTYtNDU1NWNmODY5ZDM3IiwicyI6Ik1qRTNaR1ZtWW1JdFltRmpOQzAwTXpZeUxUaG1PR1F0Tmpnek5XVmtNVE5pTUdRNCJ9 &&

curl -sS https://installer.cloudpanel.io/ce/v2/install.sh -o install.sh; \
echo "2aefee646f988877a31198e0d84ed30e2ef7a454857b606608a1f0b8eb6ec6b6 install.sh" | \
sha256sum -c && sudo DB_ENGINE=MARIADB_10.6 bash install.sh
