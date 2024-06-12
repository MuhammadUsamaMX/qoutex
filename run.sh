docker run -d \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /var/lib/docker/volumes:/var/lib/docker/volumes \
  -v /:/host \
  -v portainer_agent_data:/data \
  --restart always \
  -e EDGE=1 \
  -e EDGE_ID=5f8fe041-b9c0-4d93-9453-45c78320cd25 \
  -e EDGE_KEY=aHR0cHM6Ly9wb3J0YWluZXIuc2VydmVyLmFtdWl6LmNvbXxwb3J0YWluZXIuc2VydmVyLmFtdWl6LmNvbTo4MDAwfERFWnVyY3dLWWZTUFlBa3pzNGRkZ1hwaDg2QlhYM0g4Vk9FdDg0K2NJQ3c9fDQ \
  -e EDGE_INSECURE_POLL=1 \
  -e EDGE_ASYNC=1 \
  --name portainer_edge_agent \
  portainer/agent:2.19.5
  
