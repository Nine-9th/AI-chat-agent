# Bootdev AI Agent

A command-line AI coding agent that can list files, read file contents, execute Python files, and write/overwrite files inside a sandboxed working directory — all driven by natural-language prompts.

> Built while following along with the [Boot.dev](https://www.boot.dev/) "Build an AI Agent" course.

## How it works

The agent runs a loop: your prompt is sent to an LLM (via [OpenRouter](https://openrouter.ai/)) along with a system prompt and a set of available tools. If the model decides it needs to call a tool (list files, read a file, run a Python file, or write a file), the agent executes it and feeds the result back to the model. This repeats — up to a configured maximum number of iterations — until the model responds with a final answer instead of another tool call.

All file operations are restricted to a working directory that's injected automatically, so the model can't read or write outside the sandbox.

### Available tools

- **List files and directories**
- **Read file contents**
- **Execute Python files** (with optional arguments)
- **Write or overwrite files**

### Sandbox

The `calculator/` directory is the sample sandboxed project the agent operates on — a working target for the agent to inspect, run, and modify.

## Requirements

- Python 3.13+
- An [OpenRouter](https://openrouter.ai/) API key

## Installation

This project is managed with [uv](https://docs.astral.sh/uv/), and includes a `uv.lock` file.

```bash
git clone https://github.com/Nine-9th/AI-chat-agent.git
cd AI-chat-agent
uv sync
```

Or with plain `pip`:

```bash
git clone https://github.com/Nine-9th/AI-chat-agent.git
cd AI-chat-agent
python -m venv venv
source venv/bin/activate
pip install openai==2.44.0 python-dotenv==1.1.0
```

## Configuration

Create a `.env` file in the project root with your OpenRouter API key:

```
OPENROUTER_API_KEY=your-api-key-here
```

## Usage

```bash
uv run main.py "your prompt here"
```

Or with an activated virtual environment:

```bash
python main.py "your prompt here"
```

Add `--verbose` to see token usage and tool call results as they happen:

```bash
python main.py "list the files in the calculator directory" --verbose
```

## Running in Docker (recommended)

The agent executes Python code written by an LLM. The path checks stop it from *choosing* files outside `calculator/`, but a script it writes would still run with your user's full permissions. Running it in a container makes the sandbox real:

- The container only sees `calculator/`, mounted from your machine; the rest of your filesystem is invisible
- It runs as a non-root user, with a read-only filesystem apart from `calculator/` and `/tmp`
- All Linux capabilities are dropped and privilege escalation is blocked
- Memory, CPU and process count are capped, so a runaway script can't hog your machine
- Scripts the agent runs don't receive your `OPENROUTER_API_KEY`

With your `.env` file in place:

```bash
docker compose build
docker compose run --rm agent "list the files in the calculator directory" --verbose
```

Changes the agent makes show up in your local `calculator/` folder.

> The container still has network access (the agent needs it to reach OpenRouter), so code it runs could make outbound requests.

## Project structure

```
AI-chat-agent/
├── main.py         # CLI entry point, agent loop
├── config.py         # MAX_CHARS, MAX_ITERS settings
├── prompts.py        # System prompt
├── functions/        # Tool implementations (list, read, run, write)
├── calculator/        # Sample sandboxed project for the agent to operate on
├── test_*.py         # Unit tests for the tool functions
└── pyproject.toml      # Project metadata and dependencies
```

## Testing

```bash
uv run pytest
```

## License

No license specified.
