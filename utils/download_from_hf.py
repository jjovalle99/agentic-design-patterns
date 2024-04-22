import argparse
import json
import os

from huggingface_hub import hf_hub_download


def parse_args():
    parser = argparse.ArgumentParser(description="Download and extract files from a Hugging Face repository.")
    parser.add_argument(
        "--repo_id", type=str, required=True, help="The repository ID in the format 'username/repo_name'."
    )
    parser.add_argument(
        "--filename", type=str, required=True, help="The name of the file to download from the repository."
    )
    parser.add_argument("--output_file", type=str, required=True, help="The path to save the file.")
    return parser.parse_args()


def download_and_extract_chat_template(repo_id: str, filename: str, output_file: str) -> None:
    """
    Download a file from a Hugging Face repository and extract the content of the 'chat_template' field.

    Args:
        repo_id (str): The repository ID in the format "username/repo_name".
        filename (str): The name of the file to download from the repository.
        output_file (str): The path to save the extracted chat template.

    Returns:
        None
    """
    # Download the file from the Hugging Face repository
    tokenizer_config_path = hf_hub_download(repo_id, filename, token=os.getenv("HF_TOKEN"))

    # Read the contents of the file
    with open(tokenizer_config_path, "r") as file:
        tokenizer_config = json.load(file)

    # Extract the content of the 'chat_template' field
    chat_template = tokenizer_config["chat_template"]

    # Save the chat template content into a .jinja file
    with open(output_file, "w") as file:
        file.write(chat_template)

    print(f"Chat template saved as {output_file}")


if __name__ == "__main__":
    args = parse_args()
    download_and_extract_chat_template(repo_id=args.repo_id, filename=args.filename, output_file=args.output_file)
