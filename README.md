./setup.sh

## MCP server getup
uv run flight-mcp.py

## api client
python3 app.py


curl --location 'http://localhost:5110/api/chat' \
--header 'Content-Type: application/json' \
--data '{
    "query": "Find flights from LAX to JFK on April 26, 2025",
    "context_id": "user123"
}'