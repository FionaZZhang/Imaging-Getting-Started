import sys
import ast
import subprocess

def extract_required_libraries(script):

    # Parse the script to extract import statements
    module = ast.parse(script)

    # Extract import statements
    imports = [node for node in module.body if isinstance(node, ast.Import)]
    import_froms = [node for node in module.body if isinstance(node, ast.ImportFrom)]

    # Get module names from import statements
    required_libraries = []
    for import_node in imports + import_froms:
        for alias in import_node.names:
            required_libraries.append(alias.name)

    return required_libraries

def install_libraries(libraries):
    for library in libraries:
        subprocess.check_call([sys.executable, "-m", "pip", "install", library])

def custom(script_path, input_data_path):

    with open(script_path, 'r') as file:
        script = file.read()
        print(script)

    # Extract required libraries from the script
    required_libraries = extract_required_libraries(script)

    # Install required libraries if any
    if required_libraries:
        install_libraries(required_libraries)

    # Create a dictionary to store the variables accessible within the script
    variables = {}

    # Execute the script
    exec(script, globals(), variables)
    result = variables.get("main", None)

    if result is None or not callable(result):
        raise ValueError("No callable 'main' function found in the script")

    return result(input_data_path)


if __name__ == "__main__":

    # Get the image path from the command-line arguments
    script_path = sys.argv[1]
    input_data_path = sys.argv[2]

    # Call the function with the provided image path
    custom(script_path, input_data_path)