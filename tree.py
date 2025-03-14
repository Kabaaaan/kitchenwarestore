from pathlib import Path

def print_tree(directory, prefix=""):
    """Рекурсивно печатает структуру директории."""
    contents = list(directory.iterdir())
    for index, path in enumerate(contents):
        # Пропускаем скрытые файлы, папки и node_modules
        if (
            path.name.startswith(".")
            or path.name == "__pycache__"
            or path.name == "venv"
            or path.name == "node_modules"
            or path.name == 'tree.py'
        ):
            continue

        # Определяем, является ли текущий элемент последним в списке
        if index == len(contents) - 1:
            print(prefix + "└── " + path.name)
            if path.is_dir():
                print_tree(path, prefix + "    ")
        else:
            print(prefix + "├── " + path.name)
            if path.is_dir():
                print_tree(path, prefix + "│   ")

if __name__ == "__main__":
    project_root = Path(".")  # Укажите путь к корню проекта
    print_tree(project_root)