from pathlib import Path


def parse_config() -> dict:
    config = {
        "setup": [],
        "build": [],
        "test": [],
        "run": [],
    }

    current_section = None

    txt_path = Path("runongpu.txt")

    for line in txt_path.read_text(encoding="utf-8").splitlines():

        # Remove spaces from beginning/end
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip comments
        if line.startswith("#"):
            continue

        # Detect section headers
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].lower()
                
            #Detects if user added an unknown section
            if section not in config:
                raise ValueError(f"Unknown section: {section}")

            current_section = section
            continue

        #If user puts commands before any section
        if current_section is None:
            raise ValueError("Command found before any section header.")
        
        # Add command to current section
        config[current_section].append(line)

    return config
    