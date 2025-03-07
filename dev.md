### export requirements-ipex.txt
`uv pip compile pyproject.toml --override overrides.txt -o requirements-ipex.txt --index-strategy unsafe-best-match --extra ipex --pre --index https://download.pytorch.org/whl/test/xpu`

### export requirements.txt
`uv pip compile pyproject.toml -o requirements.txt`