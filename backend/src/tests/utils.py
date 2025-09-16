def get_file_preview(file_path: str, max_lines: int = 5) -> str:
    try:
        with open(file_path, "r") as file:
            lines = []
            for i, line in enumerate(file):
                if i >= max_lines:
                    break
                lines.append(line.strip())
            return "\n".join(lines)
    except FileNotFoundError:
        return "[file missing]"
