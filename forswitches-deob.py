r"""

Be careful, some obfuscation may have things like:

for (x = 0; x < 2; x += 1) {
    switch (x) {
        case 1: {
            ...
        }
        break
        case 0:
            ...
    }
}

and the program will match the wrong content

"""
import re
import argparse
from colorama import init, Fore
init()

indent_level = 4
debug_mode = False
total = 0

PATTERN = r"\n( +)for \((.+?) = 0; \2 < \d+; \2 \+= 1\) {\n\1    switch \(\2\) {\n\1        case ([\S\s]+?)\n\1            break;\n\1    }\n\1}"
TAB = ' '


def simplify(m):
    global total

    total += 1
    indent, varname, content = m.groups()
    new_content = '\n'
    if debug_mode:
        new_content += indent + '// REPLACED: ' + varname + '\n'
    lines_count = 0
    for n, lines in sorted(map(lambda x: x.split(':', maxsplit=1), content.split('\n' + indent + TAB * indent_level * 3 + 'break;\n' + indent + TAB * indent_level * 2 + 'case ')), key=lambda x: int(x[0])):
        for line in lines.strip('\n').split('\n'):
            new_content += line[indent_level * 3:] + '\n'
            lines_count += 1
    if debug_mode:
        print(f"indent={Fore.CYAN}{len(indent)}{Fore.RESET};varname={Fore.GREEN}{varname}{Fore.RESET};blocks={Fore.MAGENTA}{n}{Fore.RESET};lines={Fore.CYAN}{lines_count}{Fore.RESET}")
    return new_content


def main():
    global indent_level, debug_mode

    parser = argparse.ArgumentParser(description="Deobfuscates useless javascript forswitches.")
    parser.add_argument("input_file", type=str, help="The input file to process.")
    parser.add_argument("-o", "--output", required=True, type=str, help="The output file to write to.")
    parser.add_argument("-v", "--version", action="version", version="0.0.1", help="Show script version and exit.")
    parser.add_argument("-d", "--debug", action="store_true", help="Starts the script in debug mode.")
    parser.add_argument("-i", "--indent", type=int, default=4, help="Set the indentation level (default is 4 spaces).")
    args = parser.parse_args()
    indent_level = args.indent
    debug_mode = args.debug

    try:
        with open(args.input_file, "r") as infile:
            data = infile.read()
    except FileNotFoundError:
        print(f"Error: The file '{args.input_file}' does not exist.")
        return

    iteration = 1
    totalold = -1
    while totalold != total:
        totalold = total
        if debug_mode:
            print(f"iteration={Fore.LIGHTYELLOW_EX}{iteration}{Fore.RESET}")
        called = False
        data = re.sub(PATTERN, simplify, data)
        iteration += 1

    if debug_mode:
        print(f"total={Fore.LIGHTGREEN_EX}{total}{Fore.RESET}")
    print("Done !")

    try:
        with open(args.output, "w") as outfile:
            outfile.write(data)
    except IOError as e:
        print(f"Error: Could not write to the file '{args.output}'. {e}")


if __name__ == "__main__":
    main()
