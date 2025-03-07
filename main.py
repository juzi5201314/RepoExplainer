import argparse
import asyncio
import dotenv
import tqdm
import os
import local_file_loader

from pathlib import Path
from openai import RateLimitError, BadRequestError

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_openai import ChatOpenAI

import logging

logging.basicConfig(level=logging.WARNING)

dotenv.load_dotenv(override=True)

programming_language_extensions = [
    ".py",  # Python
    ".java",  # Java
    ".js",  # JavaScript
    ".ts",  # TypeScript
    ".c",  # C
    ".cpp",  # C++
    ".h",  # C/C++ Header file
    ".cs",  # C#
    ".go",  # Go
    ".rs",  # Rust
    ".rb",  # Ruby
    ".php",  # PHP
    ".swift",  # Swift
    ".kt",  # Kotlin
    ".m",  # Objective-C
    ".mm",  # Objective-C++
    ".html",  # HTML
    ".css",  # CSS
    ".sql",  # SQL
    ".sh",  # Shell Script (Bash, etc.)
    ".bat",  # Batch file (Windows)
    ".ps1",  # PowerShell (Windows)
    ".lua",  # Lua
    ".pl",  # Perl
    ".r",  # R
    ".dart",  # Dart
    ".scala",  # Scala
    ".groovy",  # Groovy
    ".vb",  # Visual Basic
    ".vbs",  # VBScript
    ".asm",  # Assembly
    ".f",  # Fortran
    ".f90",  # Fortran 90
    ".pas",  # Pascal
    ".d",  # D
    ".hs",  # Haskell
    ".ex",  # Elixir
    ".exs",  # Elixir Script
    ".erl",  # Erlang
    ".hrl",  # Erlang Header
    ".jl",  # Julia
    ".ml",  # ML (OCaml, Standard ML, etc.)
    ".mli",  # ML Interface
    ".fs",  # F#
    ".fsx",  # F# Script
    ".clj",  # Clojure
    ".cljs",  # ClojureScript
    ".coffee",  # CoffeeScript
]


async def retrieve_context(file_path: str, vectorstore, text_splitter, embeddings, k):
    with open(file_path, "r") as f:
        content = f.read()

    # file_splits = text_splitter.split_text(content)
    file_embeddings = await embeddings.aembed_documents([content])
    similar_docs = []
    for emb in file_embeddings:
        docs = await vectorstore.asimilarity_search_by_vector(
            emb,
            k=k,
            filter=lambda metadata: metadata["source"] != Path(file_path).name,
        )
        similar_docs.extend(docs)

    return similar_docs


async def generate_explanation(
    file_path: Path, vectorstore, text_splitter, embeddings, chain, k
):
    # print("Generating an explanation for `%s`" % file_path)
    with open(file_path, "r") as f:
        file_content = f.read()

    # print("Retrieving the context of `%s`" % file_path)
    similar_docs = await retrieve_context(
        file_path, vectorstore, text_splitter, embeddings, k
    )
    context = "\n\n".join([doc.page_content for doc in similar_docs])

    while True:
        try:
            explanation = await chain.ainvoke(
                {
                    "file_content": file_content,
                    "context": context,
                    "file_path": file_path,
                }
            )
            break
        except RateLimitError:
            print("Rate limit reached, waiting for 30 seconds...")
            await asyncio.sleep(30)
            continue
        except BadRequestError as e:
            if e.code == "RequestTimeOut":
                continue
    return explanation


async def generate_explanations(
    base_path, blob_loader, vector_store, text_splitter, embeddings, chain, k
):
    out_dir = Path(base_path.joinpath("explanations"))
    out_dir.mkdir(exist_ok=True)

    list_page = open(out_dir.joinpath("list.md"), "w")
    list_page.write("## List\n")

    bar = tqdm.tqdm(total=blob_loader.count_matching_files())
    bar.update(0)
    outputs = []

    async with asyncio.TaskGroup() as group:
        for path in blob_loader._yield_paths():
            try:
                output = group.create_task(
                    generate_explanation(
                        path, vector_store, text_splitter, embeddings, chain, k
                    )
                )
                output.add_done_callback(lambda _: bar.update())
                outputs.append((path, output))
            except Exception as e:
                print(e)
                print("Failed to generate an explanation for `%s`" % path)
                continue

    for path, output in outputs:
        try:
            res = output.result()
        except Exception as e:
            print(e)
            print("Failed to generate an explanation for `%s`" % path)
            continue
        (content, _, summary) = (
            res.content.split("</think>", 1)[-1]
            .strip()
            .removeprefix("```markdown")
            .strip("`")
            .strip()
            .rpartition("\n")
        )
        list_page.write("`%s`: %s\n" % (path, summary))

        md = out_dir.joinpath(path.relative_to(base_path))
        md.parent.mkdir(parents=True, exist_ok=True)
        with open(md.with_suffix(".md"), "w") as f:
            f.write(content)
            f.flush()
    list_page.flush()
    list_page.close()
    bar.close()


async def main():
    args_parser = argparse.ArgumentParser(prog="RepoExplainer")
    args_parser.add_argument(
        "path", type=Path, nargs="?", default=Path("."), help="path to you project"
    )
    args_parser.add_argument(
        "--extra-prompt", type=str, default="", help="extra prompt to add to the prompt"
    )
    args_parser.add_argument("--ipex", action="store_true", help="use ipex")
    args_parser.add_argument(
        "-t", "--temperature", "--temp", type=float, default=0.2, help="default: 0.2"
    )
    args_parser.add_argument("-m", "--model", type=str, required=True)
    args_parser.add_argument(
        "-e",
        "--exclude",
        type=str,
        action="append",
        default=[],
        help="exclude files matching the regex",
    )
    args_parser.add_argument("--prompt-template", type=str)
    args_parser.add_argument("--system", type=str)
    args_parser.add_argument("--max-retries", type=int, default=3)
    args_parser.add_argument("--max-tokens", type=int)
    args_parser.add_argument(
        "-k",
        type=int,
        default=5,
        help="number of similar documents to retrieve. default: 5",
    )
    args_parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=20,
        help="The size of the overlap between the split codes. Usually set to 10%-20% of chunk-size. default: 20",
    )
    args_parser.add_argument(
        "--chunk-size",
        type=int,
        default=200,
        help="Split the code into specified sizes. Larger sizes mean more information to retrieve and require greater context. default: 200",
    )
    args_parser.add_argument(
        "--suffixes",
        type=str,
        action="append",
        default=programming_language_extensions,
        help="file extensions to include. default includes a set of common programming languages; if this option is set, the defaults *will not* be included.",
    )
    args_parser.add_argument(
        "-l",
        "--limit",
        type=float,
        default=3,
        help="limit requests per second. default: 3",
    )
    args_parser.add_argument(
        "--embeddings-model",
        type=str,
        default="sentence-transformers/all-mpnet-base-v2",
    )

    args = args_parser.parse_args()

    prompt_message = [
        (
            "user",
            args.prompt_template
            or """
                    You are an AI assistant tasked with explaining code files.
                    Below is the content of a code file and some related context from the repository.
                    Please provide a detailed explanation of the code file in Markdown format, including its purpose, key components, and how it fits into the overall project.
                    Do not repeat questions.
                    The last line of the output must be a brief description of the role of this file in the project.
                    %s

                    ### Code File Path
                    {file_path}
                    ### Code File Content
                    {file_content}

                    ### Related Context
                    {context}

                    ### Explanation
                    """
            % args.extra_prompt,
        )
    ]
    if args.system:
        prompt_message.insert(0, ("system", args.system))
    prompt_template = ChatPromptTemplate.from_messages(prompt_message)

    base_path = args.path

    print("Use %s" % os.environ["OPENAI_API_BASE"])

    print("Loading embeddings model")
    if args.ipex:
        from langchain_community.embeddings import IpexLLMBgeEmbeddings

        os.environ["SYCL_CACHE_PERSISTENT"] = "1"
        # if Intel Core Ultra
        # os.environ["BIGDL_LLM_XMX_DISABLED"] = "1"
        embeddings = IpexLLMBgeEmbeddings(
            model_name=args.embeddings_model,
            model_kwargs={"device": "xpu"},
            encode_kwargs={"normalize_embeddings": True, "show_progress_bar": True},
        )
    else:
        embeddings = HuggingFaceEmbeddings(
            model_name=args.embeddings_model,
            show_progress=True,
        )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap
    )

    print("Loading project")
    blob_loader = local_file_loader.FileSystemBlobLoader(
        base_path,
        glob="**/*",
        exclude=[
            "venv",
            "node_modules",
            ".git",
            ".idea",
            ".vscode",
        ]
        + args.exclude,
        suffixes=args.suffixes,
        show_progress=True,
    )
    loader = GenericLoader(blob_loader, LanguageParser())
    docs = await loader.aload()

    print("Splitting the document")
    split_docs = text_splitter.split_documents(docs)

    print("Embedding the document")
    vector_store = await FAISS.afrom_documents(split_docs, embeddings)
    embeddings.encode_kwargs.__delitem__("show_progress_bar")

    llm = ChatOpenAI(
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        max_retries=args.max_retries,
        rate_limiter=InMemoryRateLimiter(requests_per_second=args.limit),
    )

    await generate_explanations(
        base_path,
        blob_loader,
        vector_store,
        text_splitter,
        embeddings,
        chain=prompt_template | llm,
        k=args.k,
    )


if __name__ == "__main__":
    asyncio.run(main())
