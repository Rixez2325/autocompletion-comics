CHARATERS_FILE_PATH = "datasets/prompts/characters.txt"
ACTIONS_FILE_PATH = "datasets/prompts/actions.txt"
BACKGROUND_FILE_PATH = "datasets/prompts/background.txt"

characters_file = open(CHARATERS_FILE_PATH, "r")
actions_file = open(ACTIONS_FILE_PATH, "r")
background_file = open(BACKGROUND_FILE_PATH, "r")


characters_lines = characters_file.read().splitlines()
actions_lines = actions_file.read().splitlines()
background_lines = background_file.read().splitlines()

# print(characters_lines)
# print(background_lines)

result = []

for character in characters_lines:
    for action in actions_lines:
        for background in background_lines:
            result.append(
                f"{character} {action.lower()}, {background.lower()} in background"
            )

with open("datasets/prompts/prompts.txt", "w") as f:
    for line in result:
        f.write(f"{line}\n")
