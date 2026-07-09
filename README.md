# RunOnGPU

RunOnGPU is a CLI tool that helps you run GitHub projects on a GPU with minimal setup.

It is useful if you want to test CUDA, PyTorch, or other GPU code but do not have a local NVIDIA GPU.

## Requirements

* Windows
* Python 3.12.13+
* Git
* Google Chrome
* Google account for Colab

## Install
Example video: https://www.loom.com/share/79d5dfd3cba4401fb2fd5967a8438391
1. Install anaconda with Python >= 3.12.13 for smooth performance
2. Publish your code in a public GitHub repo. You will use the GitHub repo URL
3. Create conda environment. You can use any name you like but for following example, we used test_env.
```bash
conda create --name test_env "python>3.12"
conda activate test_env
```
4. Run following commands in your conda enviroment
```bash
pip install runongpu
````
Check setup:
```bash
runongpu doctor
```
5. Make sure you do not touch chrome or move around your cursor as the program runs the code.
6. Be prepared to sign in to your google account once. Your profile will be saved for future sessions.
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


RunOnGPU will open Colab, copy the starter notebook, clone your repo, set the runtime to a T4 GPU, and run your commands. If for some reason, it doesn't work on the first try, press enter in your command line interface to restart the program. 

## runongpu.txt
You need this to run neccesary commands. You must edit this file to ensure your program runs smoothly.

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

Examples of RunOnGPU use:
https://github.com/MashrafeeAryan/runongpu-examples

## Run Tests

```bash
python -m pytest
```
