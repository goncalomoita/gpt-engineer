import re

# Amount of lines within the code block to consider for filename discovery
N_CODELINES_FOR_FILENAME_TA = 5

<<<<<<< HEAD
# Default path to use if no filename is found
DEFAULT_PATH = 'unknown.txt'

=======
def parse_chat(chat):  # -> List[Tuple[str, str]]:
    # Get all ``` blocks and preceding filenames
    regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
    matches = re.finditer(regex, chat, re.DOTALL)
>>>>>>> ac03a24027bb72c3d969f2bf98e52fda6b4d72b4

def parse_chat(chat: str, verbose: bool = False) -> List[Tuple[str, str]]:
    '''
    Parses a chat message and returns a list of tuples containing
    the file path and the code content for each file.
    '''
    code_regex = r'```(.*?)```'
    filename_regex = r'\b[\w-]+\.[\w]{1,6}\b'

    # Get all ``` (code) blocks
    code_matches = re.finditer(code_regex, chat, re.DOTALL)
    
    prev_code_y_end = 0
    files = []
<<<<<<< HEAD
    for match in code_matches:
        lines = match.group(1).split('\n')
        code_y_start = match.start()
        code_y_end = match.end()

        # Now, we need to get the filename associated with this code block.
        # We will look for the filename somewhere near the code block start.
        #
        # This "somewhere near" is referred to as the "filename_ta", to
        # resemble a sort-of target area (ta).
        #
        # The target area includes the text preceding the code block that
        # does not belong to previous code blocks ("no_code").
        # Additionally, as sometimes the filename is defined within
        # the code block itself, we will also include the first few lines
        # of the code block in the filename_ta.
        #
        # Example:
        # ```python
        # # File: entrypoint.py
        # import pygame
        # ```
        #
        # The amount of lines to consider within the code block is set by
        # the constant 'N_CODELINES_FOR_FILENAME_TA'.
        #
        # Get the "preceding" text, which is located between codeblocks
        no_code = chat[prev_code_y_end:code_y_start].strip()
        within_code = '\n'.join(lines[:N_CODELINES_FOR_FILENAME_TA])
        filename_ta = no_code + '\n' + within_code
        
        # The path is the filename itself which we greedily match
        filename = re.search(filename_regex, filename_ta)
        path = filename.group(0) if filename else DEFAULT_PATH

        # Visualize the filename_ta if verbose
        if verbose:
            print('-' * 20)
            print(f'Path: {path}')
            print('-' * 20)
            print(filename_ta)
            print('-' * 20)
        
        # Check if its not a false positive
        #
        # For instance, the match with ```main.py``` should not be considered.
        # ```main.py```
        # ```python
        # ...
        # ```
        if not re.fullmatch(filename_regex, '\n'.join(lines)):
            # Update the previous code block end
            prev_code_y_end = code_y_end

            # File and code have been matched, add them to the list
            files.append((path, '\n'.join(lines[1:])))
=======
    for match in matches:
        # Strip the filename of any non-allowed characters and convert / to \
        path = re.sub(r'[<>"|?*]', "", match.group(1))

        # Remove leading and trailing brackets
        path = re.sub(r"^\[(.*)\]$", r"\1", path)

        # Remove leading and trailing backticks
        path = re.sub(r"^`(.*)`$", r"\1", path)

        # Remove trailing ]
        path = re.sub(r"\]$", "", path)

        # Get the code
        code = match.group(2)

        # Add the file to the list
        files.append((path, code))
>>>>>>> ac03a24027bb72c3d969f2bf98e52fda6b4d72b4

    # Get all the text before the first ``` block
    readme = chat.split("```")[0]
    files.append(("README.md", readme))

    # Return the files
    return files


def to_files(chat, workspace):
    workspace["all_output.txt"] = chat

    files = parse_chat(chat)
    for file_name, file_content in files:
        workspace[file_name] = file_content
