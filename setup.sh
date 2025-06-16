
#!/bin/bash

# Create logs directory for container mounting
mkdir -p logs

# Run the test suite
docker-compose up --abort-on-container-exit