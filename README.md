# Grok-MCP

MCP server for xAI's Grok API with agentic tool calling, image generation, vision, and reasoning models.


<a href="https://glama.ai/mcp/servers/@merterbak/Grok-MCP">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@merterbak/Grok-MCP/badge" />
</a>

## Features

- **Agentic Tool Calling**: Web search, X search, and code execution with multi-step reasoning
- **Multiple Grok Models**: Access to Grok-4.1-Fast-Reasoning, Grok-4.1-Fast-Non-Reasoning, Grok-4-Fast, Grok-3-Mini, and more
- **Image Generation**: Create images using Grok's image generation model
- **Vision Capabilities**: Analyze images with Grok's vision models
- **Reasoning Models**: Advanced reasoning with extended thinking models (Grok-4.1-Fast-Reasoning, Grok-3-Mini, Grok-4)
- **Stateful Conversations**: Use this newly released feature to maintain conversation context as id across multiple requests

## Prerequisites

- Python 3.11 or higher
- xAI API key ([Get one here](https://console.x.ai))
- [Astral UV](https://docs.astral.sh/uv/getting-started/installation/)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/merterbak/Grok-MCP.git
cd Grok-MCP
```

2. Create a venv environment:
```bash
uv venv
source .venv/bin/activate # macOS/Linux or .venv\Scripts\activate on Windows
```

3. Install dependencies:

```bash
uv sync
```


## Configuration

### Claude Desktop Integration

Add this to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "grok": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/Grok-MCP",
        "run",
        "python",
        "main.py"
      ],
      "env": {
        "XAI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Filesystem MCP (Optional)

Claude Desktop can't send uploaded images in the chat to an MCP tool.
The easiest way to give access to files directly from your computer is official Filesystem MCP server.
After setting it up you’ll be able to just write the image’s file path (such as /Users/mert/Desktop/image.png) in chat and Claude can use it with any vision chat tool.

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/<your-username>/Desktop",
        "/Users/<your-username>/Downloads"
      ]
    }
  }
}

```

---

For stdio:

```bash
uv run python main.py
```
Docker:

```bash
docker compose up --build
```
Mcp Inspector:

```bash
mcp dev main.py
```


# Available Tools


### `list_models`
List all available Grok models.

---

### `chat`
Standard chat completion.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | required | Your message |
| `model` | str | `grok-4` | Model to use |
| `system_prompt` | str | None | System instruction |
| `store_messages` | bool | False | Enable conversation history |

---

### `chat_with_vision`
Analyze images with text.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | required | Question about the image |
| `image_paths` | List[str] | None | Local image file paths |
| `image_urls` | List[str] | None | Image URLs |
| `detail` | str | `auto` | `auto`, `low`, or `high` |
| `model` | str | `grok-4` | Vision model |

**Returns:** Content + usage with `prompt_image_tokens`

---

### `chat_with_reasoning`
Get detailed reasoning with the response.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | required | Your question |
| `model` | str | `grok-3-mini` | Reasoning model |
| `reasoning_effort` | str | None | `low` or `high` |

**Returns:** Content, reasoning_content, usage (with reasoning_tokens)

---

### `generate_image`
Create images from text.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | required | Image description |
| `n` | int | 1 | Number of images |
| `image_format` | str | `url` | `url` or `b64_json` |
| `model` | str | `grok-2-image-1212` | Image model |

---

### `web_search`
Agentic web search with autonomous research.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | required | Search query |
| `model` | str | `grok-4-1-fast` | Model |
| `allowed_domains` | List[str] | None | Restrict to domains (max 5) |
| `excluded_domains` | List[str] | None | Exclude domains (max 5) |
| `enable_image_understanding` | bool | False | Analyze images in results |
| `include_inline_citations` | bool | False | Embed citations in text |
| `max_turns` | int | None | Limit reasoning turns |

**Returns:** Content, citations, tool_calls, usage

---

### `x_search`
Agentic X (Twitter) search.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | required | Search query |
| `model` | str | `grok-4-1-fast` | Model |
| `allowed_x_handles` | List[str] | None | Only these handles (max 10) |
| `excluded_x_handles` | List[str] | None | Exclude handles (max 10) |
| `from_date` | str | None | Start date (DD-MM-YYYY) |
| `to_date` | str | None | End date (DD-MM-YYYY) |
| `enable_image_understanding` | bool | False | Analyze images |
| `enable_video_understanding` | bool | False | Analyze videos |
| `include_inline_citations` | bool | False | Embed citations |
| `max_turns` | int | None | Limit turns |

**Returns:** Content, citations, tool_calls, usage

---

### `agentic_search`
Combined agentic search with web, X, and code execution.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | required | Query |
| `use_web_search` | bool | True | Enable web search |
| `use_x_search` | bool | True | Enable X search |
| `use_code_execution` | bool | False | Enable Python code |
| + all web_search and x_search params | | | |

---

### `code_executor`
Execute Python code for calculations and analysis.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | required | Task description |
| `model` | str | `grok-4-1-fast` | Model |
| `include_code_output` | bool | True | Return execution output |
| `max_turns` | int | None | Limit turns |

**Returns:** Content, tool_calls, code_outputs, usage

---

### `stateful_chat`
Maintain conversation state across requests.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | required | Your message |
| `response_id` | str | None | Previous response ID |
| `model` | str | `grok-4` | Model |
| `system_prompt` | str | None | System instruction |

**Returns:** Content, response_id, usage

---

### `retrieve_stateful_response`
Retrieve a stored conversation.

### `delete_stateful_response`
Delete a stored conversation.

---

  
## License

This project is open source and available under the MIT License.
