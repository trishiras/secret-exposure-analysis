# Guide for Secret Exposure Analysis Tool

This guide provides detailed instructions on how to build, run, and use the Secret Exposure Analysis Tool designed to scan for exposed secrets in repositories, file systems, and Git repositories. The tool is designed to generate reports using Gitleaks.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Building the Docker Image](#building-the-docker-image)
4. [Running the Docker Container](#running-the-docker-container)
5. [Tool Usage](#tool-usage)
6. [Troubleshooting](#troubleshooting)
7. [Additional Information](#additional-information)

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Git (optional, for cloning the repository)

## Project Structure

```
secret-exposure-analysis/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── GUIDE.md
├── README.md
├── requirements.txt
├── setup.py
├── config/
|   └── config.toml
|
└── secret_exposure_analysis/
    ├── __init__.py
    ├── __version__.py
    ├── main.py
    |
    ├── core/
    |   ├── __init__.py
    |   ├── input.py
    |   ├── logger.py
    |   └── models.py
    |
    ├── service/
    |   ├── __init__.py
    |   └── gitleaks.py
    |
    └── support/
        ├── __init__.py
        └── enums.py
```

## Building the Docker Image

1. Open a terminal and navigate to the project directory:

   ```bash
   cd path/to/secret-exposure-analysis
   ```

2. Build the Docker image using the following command:

   ```bash
   sudo docker build --no-cache . -f Dockerfile -t secret-exposure-analysis:latest
   ```

   This command builds a Docker image named `secret-exposure-analysis` based on the instructions in the Dockerfile.

## Running the Docker Container

To run the Secret Exposure Analysis Tool inside a Docker container, use the following command structure:

```bash
sudo docker run --rm -it -v $(pwd)/output:/output secret-exposure-analysis [arguments]
```

Replace `[arguments]` with the actual arguments for the tool.

### Explanation of Docker run options:

- `--rm`: Automatically remove the container when it exits.
- `-it`: Run container in interactive mode.
- `-v $(pwd)/output:/output`: Mount the local `output` directory to `/output` in the container.
- `secret-exposure-analysis`: The name of the Docker image to run.

## Tool Usage

The Secret Exposure Analysis Tool accepts several command-line arguments:

- `-t, --target`: (Required) Target as path to scan.
- `-ov, --output-via`: (Required) Specify output method: "file" or "webhook".
- `-w, --webhook`: Webhook URL (required if output_via is "webhook").
- `-o, --output`: File path for output (required if output_via is "file").
- `-l, --log`: Log level (DEBUG or ERROR, default is DEBUG).

### Example Commands:

1. Scan a local directory and output to a file:
   ```bash
   sudo docker run --rm -it -v $(pwd)/output:/output -v /path/to/scan:/scan secret-exposure-analysis -t /scan -ov file -o /output/results.json
   ```

2. Scan a local directory and send results to a webhook:
   ```bash
   sudo docker run --rm -it -v /path/to/scan:/scan secret-exposure-analysis -t /scan -ov webhook -w https://webhook.site/your-unique-url
   ```


Note: When using file output or scanning local directories, you need to mount volumes to access the results or scan targets from your host machine.

## Troubleshooting

1. **Permission Issues**: If you encounter permission problems when writing to mounted volumes, you may need to adjust the permissions or use a named volume.

2. **Network Issues**: Ensure your Docker network settings allow the container to access the target network or webhook URL.

3. **Missing Requirements**: If the build fails due to missing requirements, check that your `requirements.txt` file is up to date and includes all necessary dependencies.

4. **Git Safe Directory**: The Dockerfile configures Git to treat `/scan` as a safe directory. If you're scanning a different directory, you may need to adjust this configuration.

## Additional Information

- The tool uses Python 3.12 as specified in the Dockerfile.
- The tool integrates Gitleaks for secret scanning. For detailed information about Gitleaks' capabilities, refer to its documentation or use the `gitleaks --help` command inside the container.
- The Secret Exposure Analysis Tool supports various output formats including JSON, CSV, JUnit, and SARIF.

### Gitleaks Command Options

Gitleaks provides several commands and options:

- `dir`: Scan directories or files for secrets
- `git`: Scan git repositories for secrets
- `stdin`: Detect secrets from stdin
- `version`: Display gitleaks version

Common flags:

- `--config`: Specify a config file path
- `--baseline-path`: Path to baseline with issues that can be ignored
- `--enable-rule`: Only enable specific rules by id
- `--exit-code`: Set exit code when leaks have been encountered
- `--redact`: Redact secrets from logs and stdout
- `--report-format`: Output format (json, csv, junit, sarif)
- `--report-path`: Report file path

For a complete list of options, use `gitleaks --help` inside the container.

```
Gitleaks scans code, past or present, for secrets

Usage:
  gitleaks [command]

Available Commands:
  completion  generate the autocompletion script for the specified shell
  dir         scan directories or files for secrets
  git         scan git repositories for secrets
  help        Help about any command
  stdin       detect secrets from stdin
  version     display gitleaks version

Flags:
  -b, --baseline-path string          path to baseline with issues that can be ignored
  -c, --config string                 config file path
                                      order of precedence:
                                      1. --config/-c
                                      2. env var GITLEAKS_CONFIG
                                      3. (target path)/.gitleaks.toml
                                      If none of the three options are used, then gitleaks will use the default config
      --enable-rule strings           only enable specific rules by id
      --exit-code int                 exit code when leaks have been encountered (default 1)
  -i, --gitleaks-ignore-path string   path to .gitleaksignore file or folder containing one (default ".")
  -h, --help                          help for gitleaks
      --ignore-gitleaks-allow         ignore gitleaks:allow comments
  -l, --log-level string              log level (trace, debug, info, warn, error, fatal) (default "info")
      --max-decode-depth int          allow recursive decoding up to this depth (default "0", no decoding is done)
      --max-target-megabytes int      files larger than this will be skipped
      --no-banner                     suppress banner
      --no-color                      turn off color for verbose output
      --redact uint[=100]             redact secrets from logs and stdout. To redact only parts of the secret just apply a percent value from 0..100. For example --redact=20 (default 100%)
  -f, --report-format string          output format (json, csv, junit, sarif) (default "json")
  -r, --report-path string            report file
  -v, --verbose                       show verbose output from scan
      --version                       version for gitleaks

Use "gitleaks [command] --help" for more information about a command.
```

For more information or to report issues, please refer to the project's documentation or repository.