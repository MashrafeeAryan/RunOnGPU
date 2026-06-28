# RunOnGPU

RunOnGPU is a CLI tool that helps you run GitHub projects on a Google Colab GPU.

It is useful if you want to test CUDA, PyTorch, or other GPU code but do not have a local NVIDIA GPU.

## Requirements

* Windows
* Python 3.10+
* Git
* Google Chrome
* Google account for Colab

## Install

Clone the repo:

```bash
git clone https://github.com/MashrafeeAryan/RunOnGPU.git
cd RunOnGPU
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install RunOnGPU:

```bash
python -m pip install -e .
```

Install Playwright:

```bash
python -m playwright install
```

Check setup:

```bash
runongpu doctor
```

## Quick Start

Go to the project you want to run and initialize RunOnGPU:

```bash
runongpu init
```

Enter your GitHub repo URL when asked.

This creates a `runongpu.txt` file. Edit this file to tell RunOnGPU how to set up, build, test, and run your project.

Then run:

```bash
runongpu run
```

RunOnGPU will open Colab, copy the starter notebook, clone your repo, set the runtime to a T4 GPU, and run your commands.

## runongpu.txt

`runongpu.txt` controls what happens inside Colab.

It has four sections:

```text
[setup]
# install dependencies here

[build]
# compile or build the project here

[test]
# run tests here

[run]
# run the final program here
```

Add one command per line.

## Example: CUDA

If your repo has this structure:

```text
my-cuda-project/
├── main.cu
└── runongpu.txt
```

Use:

```text
[setup]

[build]
nvcc main.cu -o vector_add

[test]

[run]
./vector_add
```

## Example: CUDA in a Subfolder

If your repo has this structure:

```text
runongpu-examples/
├── cuda/
│   └── vector-add/
│       └── main.cu
└── runongpu.txt
```

Use:

```text
[setup]

[build]
cd cuda/vector-add && nvcc main.cu -o vector_add

[test]

[run]
cd cuda/vector-add && ./vector_add
```

## Example: Python

```text
[setup]
pip install -r requirements.txt

[build]

[test]
pytest

[run]
python main.py
```

## Example: CMake

```text
[setup]

[build]
cmake -S . -B build
cmake --build build

[test]
ctest --test-dir build --output-on-failure

[run]
./build/my_program
```

## Notes

On the first run, you may need to sign into Google Colab. RunOnGPU saves the copied notebook URL and reuses it on future runs.

Do not interact with the Colab window while RunOnGPU is setting it up.

## Run Tests

```bash
python -m pytest
```
