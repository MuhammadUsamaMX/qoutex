docker run -d \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /var/lib/docker/volumes:/var/lib/docker/volumes \
  -v /:/host \
  -v portainer_agent_data:/data \
  --restart always \
  -e EDGE=1 \
  -e EDGE_ID=67216eaf-bbbc-4052-8bde-ba6ee903e146 \
  -e EDGE_KEY=aHR0cHM6Ly9wb3J0YWluZXIuc2VydmVyLmFtdWl6LmNvbXxwb3J0YWluZXIuc2VydmVyLmFtdWl6LmNvbTo4MDAwfERFWnVyY3dLWWZTUFlBa3pzNGRkZ1hwaDg2QlhYM0g4Vk9FdDg0K2NJQ3c9fDU \
  -e EDGE_INSECURE_POLL=1 \
  --name portainer_edge_agent_2 \
  portainer/agent:2.19.5
  
