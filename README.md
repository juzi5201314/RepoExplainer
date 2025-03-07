## RepoExplainer

RepoExplainer is an AI tool designed to generate explanations for each file in a project, aiming to assist individuals in quickly learning and understanding open-source projects. It leverages large language models (LLMs) and the LangChain library to produce explanations and summaries for code files within a specified directory.

* Supports any OpenAI-compatible API endpoint.
* Allows customization and additional prompts, such as instructing the LLM to output in Chinese.
* Embeddings support acceleration with Intel GPUs (NVIDIA GPU support is presumably enabled by default, but I am unable to confirm this as I do not have an NVIDIA GPU for testing).
* Implements API rate limiting to avoid being rate-limited by third-party endpoints.

### Example
I generated some explanations for [Tokio](https://github.com/tokio-rs/tokio) using multiple models:
* Gemini2.0 Flash Lite. (Chinese) [example](./examples/tokio-gemini/)
* Qwen QwQ 32B. (Chinese) [example](./examples/tokio-qwq/)
* DeepSeek R1. (English, k=20) [example](./examples/tokio-r1/)

Tokio is a very large project with approximately `114,541` lines of Rust code.

I skipped files such as tests, examples, and benchmarks, retrieve 10 related documents, instructed the model to output in Chinese, and limited requests to one every two seconds.
```bash
uv run --frozen main.py --extra-prompt "Output Chinese." -m gemini-2.0-flash-lite -e "tests-*/*" -e "examples/*" -e benches/*  /project/tokio/ -k 10 --limit 0.5
```

On QwQ 32b, the number of tokens used is:
input: `1,190,991 tokens (1.19M)`
output: `578,622 tokens (0.57M)`

On DeepSeek R1, the number of tokens used is:
input: `1,448,047 tokens (1.44M)`
output: `445,289 tokens (0.44M)`

Token consumption is not fixed, even for the same file, different models, temperatures, and even each call will have differences.

### Todo
* Provides improved default prompts.
* New feature: Generates comments directly within the source code.

### Known issue
* Large individual files may exceed the model's context limit.
* Unable to implement rate limiting based on TPM (Tokens per Minute).

### Usage
`python == 3.11`

**Large projects can quickly consume your tokens; please monitor your balance.**
**Be mindful of your API rate limit; set the `--limit` to avoid failures due to rate limiting.**

In theory, the context size used for each request is approximately: `token(file size + prompt_template + (k * chunk_size) + llm output)`.
Pay attention to the context size of the model you use, do not exceed the maximum size.

Currently, the way `list.md` works is to have llm generate a summary sentence on the last line in the prompt. This is very unstable and needs to be fixed.

1. setup your openai api key
```bash
# if you are using third-party openai api endpoint
export OPENAI_API_BASE=https://your_api_base
export OPENAI_API_KEY=your_api_key
```
or write into `.env` file

2. install dependencies and run
```bash
pip install -r requirements.txt

python main.py -m model_name /path/to/your/project
```

#### if using uv
1. setup venv (only new)
```bash
uv venv --python 3.11`
```

2. install dependencies
```bash
uv pip sync requirements.txt --index-strategy unsafe-best-match
```

3. run
```bash
uv run --frozen main.py -m model_name /path/to/your/project
```

#### if using intel GPUs
use `requirements-ipex.txt` instead of `requirements.txt`.
add `--ipex` to the command line.

#### Usage Help
```
usage: RepoExplainer [-h] [--extra-prompt EXTRA_PROMPT] [--ipex] [-t TEMPERATURE] -m MODEL [-e EXCLUDE]
                     [--prompt-template PROMPT_TEMPLATE] [--system SYSTEM] [--max-retries MAX_RETRIES] [--max-tokens MAX_TOKENS] [-k K]
                     [--chunk-overlap CHUNK_OVERLAP] [--chunk-size CHUNK_SIZE] [--suffixes SUFFIXES] [-l LIMIT]
                     [--embeddings-model EMBEDDINGS_MODEL]
                     [path]

positional arguments:
  path                  path to you project

options:
  -h, --help            show this help message and exit
  --extra-prompt EXTRA_PROMPT
                        extra prompt to add to the prompt
  --ipex                use ipex
  -t TEMPERATURE, --temperature TEMPERATURE, --temp TEMPERATURE
                        default: 0.2
  -m MODEL, --model MODEL
  -e EXCLUDE, --exclude EXCLUDE
                        exclude files matching the regex
  --prompt-template PROMPT_TEMPLATE
  --system SYSTEM
  --max-retries MAX_RETRIES
  --max-tokens MAX_TOKENS
  -k K                  number of similar documents to retrieve. default: 5
  --chunk-overlap CHUNK_OVERLAP
                        The size of the overlap between the split codes. Usually set to 10%-20% of chunk-size. default: 20
  --chunk-size CHUNK_SIZE
                        Split the code into specified sizes. Larger sizes mean more information to retrieve and require greater
                        context. default: 200
  --suffixes SUFFIXES   file extensions to include. default includes a set of common programming languages; if this option is set, the
                        defaults *will not* be included.
  -l LIMIT, --limit LIMIT
                        limit requests per second. default: 3
  --embeddings-model EMBEDDINGS_MODEL
```

### Speed
Usually, there are two speed bottlenecks: embedding and text generation.

The former can use GPU acceleration. The latter is usually limited by the rate limit of the third-party API you use.

Network io is not a problem, because API calls are asynchronous and concurrent.

