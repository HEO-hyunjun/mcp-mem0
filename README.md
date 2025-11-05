<h1 align="center">MCP-Mem0: Long-Term Memory for AI Agents</h1>

<p align="center">
  <img src="public/Mem0AndMCP.png" alt="Mem0 and MCP Integration" width="600">
</p>

> 🚩 This repository is a modified fork of [coleam00/mcp-mem0](https://github.com/coleam00/mcp-mem0).

A template implementation of the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server integrated with [Mem0](https://mem0.ai) for providing AI agents with persistent memory capabilities.

Use this as a reference point to build your MCP servers yourself, or give this as an example to an AI coding assistant and tell it to follow this example for structure and code correctness!

## Overview

This project demonstrates how to build an MCP server that enables AI agents to store, retrieve, and search memories using semantic search. It serves as a practical template for creating your own MCP servers, simply using Mem0 and a practical example.

The implementation follows the best practices laid out by Anthropic for building MCP servers, allowing seamless integration with any MCP-compatible client.

## Features

The server provides three essential memory management tools:

1. **`save_memory`**: Store any information in long-term memory with semantic indexing
2. **`get_all_memories`**: Retrieve all stored memories for comprehensive context
3. **`search_memories`**: Find relevant memories using semantic search

## Prerequisites

- Python 3.12+
- Docker and Docker Compose (recommended for easy setup)
- API keys for your chosen LLM provider (OpenAI, Anthropic, Azure OpenAI, Google AI, etc.)

The project includes:

- **Qdrant** for vector storage (included in docker-compose)
- **Neo4j** for graph memory (optional, see Configuration section)

## Installation

### Using Docker Compose (Recommended)

1. Clone this repository:

   ```bash
   git clone https://github.com/HEO-hyunjun/mcp-mem0.git
   cd mcp-mem0
   ```

2. Create a `.env` file based on `.env.example`:

   ```bash
   cp .env.example .env
   ```

3. Configure your environment variables in the `.env` file (see Configuration section)

4. Create a `mem0_config.yml` file based on `mem0_config.example.yml`:

   ```bash
   cp mem0_config.example.yml mem0_config.yml
   ```

5. Configure your Mem0 settings in `mem0_config.yml` (see [Mem0 Configuration](https://docs.mem0.ai/open-source/configuration#config-yaml))

### Using uv (Advanced)

If you prefer to run without Docker:

1. Install uv if you don't have it:

   ```bash
   pip install uv
   ```

2. Clone and install dependencies:

   ```bash
   git clone https://github.com/HEO-hyunjun/mcp-mem0.git
   cd mcp-mem0
   uv sync
   ```

3. Set up external services (Qdrant, Neo4j) manually or use docker-compose for just the databases

## Configuration

### Environment Variables

Configure these variables in your `.env` file:

#### Core Settings

| Variable    | Description                                                  | Default | Required                            |
| ----------- | ------------------------------------------------------------ | ------- | ----------------------------------- |
| `TRANSPORT` | Transport protocol (sse, stdio, or streamable-http)          | `sse`   | Yes                                 |
| `PORT`      | Port to listen on when using SSE or streamable-http transport | `8000`  | Yes (SSE/streamable-http only) |

#### Graph Store (Neo4j)

The project supports **optional graph memory** for advanced relationship tracking. This feature uses Neo4j but can be disabled for a lighter deployment.

| Variable             | Description                        | Default         | Required              |
| -------------------- | ---------------------------------- | --------------- | --------------------- |
| `ENABLE_GRAPH_STORE` | Enable Neo4j graph memory features | `false`         | No                    |
| `NEO4J_USERNAME`     | Neo4j username                     | `neo4juser`     | Only if graph enabled |
| `NEO4J_PASSWORD`     | Neo4j password                     | `neo4jpassword` | Only if graph enabled |

**Graph Store Philosophy:**

- **Disabled** (default): Lightweight deployment with just vector search (Qdrant only)
- **Enabled**: Advanced memory relationships and entity graphs (adds Neo4j container)

To enable graph memory:

```bash
# In .env
ENABLE_GRAPH_STORE=true

# Run with graph profile
docker-compose --profile graph up
```

#### LLM Provider

Configure your LLM provider in `mem0_config.yml`. Supported providers include:

- OpenAI (`OPENAI_API_KEY`)
- Anthropic (`ANTHROPIC_API_KEY`)
- Azure OpenAI (`LLM_AZURE_OPENAI_API_KEY`, `LLM_AZURE_DEPLOYMENT`, `LLM_AZURE_ENDPOINT`, `LLM_AZURE_API_VERSION`)
- Google AI (`GOOGLE_API_KEY`)
- And more (see [Mem0 LLM docs](https://docs.mem0.ai/components/llms/config))

Set API keys in `.env` and reference them in `mem0_config.yml` using `${VARIABLE_NAME}` syntax.

## Running the Server

### Using Docker Compose (Recommended)

#### Lightweight Mode (Vector Search Only)

For a minimal deployment without graph memory:

```bash
# In .env, set ENABLE_GRAPH_STORE=false (or leave it default)
docker-compose up
```

This starts:

- Qdrant (vector database)
- MCP-Mem0 server

#### Full Mode (With Graph Memory)

For advanced memory relationships using Neo4j:

```bash
# In .env, set ENABLE_GRAPH_STORE=true
docker-compose --profile graph up
```

This starts:

- Qdrant (vector database)
- Neo4j (graph database)
- MCP-Mem0 server

**Note:** Neo4j takes ~90 seconds to fully initialize. The server will wait for Neo4j to be healthy before starting.

#### Using Specific Services

```bash
# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f mem0

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build
```

### Using uv (Without Docker)

If running without Docker, you'll need to set up Qdrant and optionally Neo4j separately.

#### SSE Transport

```bash
# Set TRANSPORT=sse in .env then:
uv run src/main.py
```

#### Streamable HTTP Transport

```bash
# Set TRANSPORT=streamable-http in .env then:
uv run src/main.py
```

#### Stdio Transport

With stdio, the MCP client itself can spin up the MCP server, so nothing needs to be run manually.

## Integration with MCP Clients

### Streamable HTTP Configuration

Streamable HTTP is the modern transport protocol (released March 26, 2025) that provides bidirectional communication through a single endpoint. Once you have the server running with streamable-http transport, you can connect to it using this configuration:

```json
{
  "mcpServers": {
    "mem0": {
      "transport": "streamable-http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

**Key features:**
- Single endpoint architecture for all MCP interactions
- Bidirectional communication (servers can send notifications and requests back to clients)
- Session management support via `Mcp-Session-Id` header
- Recommended for new deployments

Make sure to update the port if you are using a value other than the default 8000.

### SSE Configuration

Once you have the server running with SSE transport, you can connect to it using this configuration:

```json
{
  "mcpServers": {
    "mem0": {
      "transport": "sse",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

> **Note for Windsurf users**: Use `serverUrl` instead of `url` in your configuration:
>
> ```json
> {
>   "mcpServers": {
>     "mem0": {
>       "transport": "sse",
>       "serverUrl": "http://localhost:8000/sse"
>     }
>   }
> }
> ```

> **Note for n8n users**: Use host.docker.internal instead of localhost since n8n has to reach outside of it's own container to the host machine:
>
> So the full URL in the MCP node would be: http://host.docker.internal:8000/sse

Make sure to update the port if you are using a value other than the default 8000.

### Stdio with Docker Compose Configuration

With stdio transport, configure your MCP client to connect to the running Docker Compose stack:

```json
{
  "mcpServers": {
    "mem0": {
      "command": "docker",
      "args": ["exec", "-i", "mcp_mem0", "python", "/app/src/main.py"],
      "env": {
        "TRANSPORT": "stdio"
      }
    }
  }
}
```

**Prerequisites:** The Docker Compose stack must be running (`docker-compose up -d`) before connecting with stdio.

### Python with Stdio Configuration (Without Docker)

If running with uv directly:

```json
{
  "mcpServers": {
    "mem0": {
      "command": "your/path/to/mcp-mem0/.venv/Scripts/python.exe",
      "args": ["your/path/to/mcp-mem0/src/main.py"],
      "env": {
        "TRANSPORT": "stdio",
        "ENABLE_GRAPH_STORE": "false",
        "OPENAI_API_KEY": "YOUR-API-KEY"
      }
    }
  }
}
```

Add other required environment variables as needed (see Configuration section).

## Building Your Own Server

This template provides a foundation for building more complex MCP servers. To build your own:

1. Add your own tools by creating methods with the `@mcp.tool()` decorator
2. Create your own lifespan function to add your own dependencies (clients, database connections, etc.)
3. Modify the `utils.py` file for any helper functions you need for your MCP server
4. Feel free to add prompts and resources as well with `@mcp.resource()` and `@mcp.prompt()`
