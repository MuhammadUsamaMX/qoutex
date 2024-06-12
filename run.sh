docker run -d \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /var/lib/docker/volumes:/var/lib/docker/volumes \
  -v /:/host \
  -v portainer_agent_data:/data \
  --restart always \
  -e EDGE=1 \
  -e EDGE_ID=0353397f-6fb7-458d-855a-2741952f1686 \
  -e EDGE_KEY=aHR0cHM6Ly9wb3J0YWluZXIuc2VydmVyLmFtdWl6LmNvbS98MTQxLjE0Ny43My41Nzo4MDAwfERFWnVyY3dLWWZTUFlBa3pzNGRkZ1hwaDg2QlhYM0g4Vk9FdDg0K2NJQ3c9fDM \
  -e EDGE_INSECURE_POLL=1 \
  --name portainer_edge_agent \
  portainer/agent:2.19.5
  
