from pathlib import Path


def parse_config() -> dict:
    # Each section maps to the list of commands RunOnGPU should run in Colab.
    config = {
        "setup": [],
        "build": [],
        "test": [],
        "run": [],
    }

    current_section = None

    # Path("runongpu.txt") looks for the file in the current terminal directory.
    # Users should run RunOnGPU from the project folder that contains runongpu.txt.
    txt_path = Path("runongpu.txt")

    for line in txt_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        # Ignore spacing and documentation inside runongpu.txt.
        if not line:
            continue

        if line.startswith("#"):
            continue

        # Section headers decide where the following commands should be stored.
        # Example: [build] makes current_section equal to "build".
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].lower()

            if section not in config:
                raise ValueError(f"Unknown section: {section}")

            current_section = section
            continue

        # Commands must appear under a valid section so RunOnGPU knows when to run them.
        if current_section is None:
            raise ValueError("Command found before any section header.")

        config[current_section].append(line)

    return config