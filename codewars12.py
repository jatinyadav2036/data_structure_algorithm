# Split Comments

def strip_comments(strng, markers):
    lines = strng.split('\n')
    cleaned = []

    for line in lines:
        for marker in markers:
            if marker in line:
                line = line.split(marker)[0]
        cleaned.append(line.rstrip())

    return '\n'.join(cleaned)