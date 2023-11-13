import glob
import os
import sys

from jinja2 import Environment, FileSystemLoader, meta

TEMPLATE_PATH = "~/Templates/"

file_loader = FileSystemLoader(os.path.expanduser(TEMPLATE_PATH))

env = Environment(loader=file_loader)


def get_all_files(directory):
    directory = os.path.expanduser(directory)
    return [
        (
            os.path.relpath(file, os.path.expanduser(TEMPLATE_PATH)),
            os.path.relpath(file, directory),
        )
        for file in glob.glob(directory + "/**/*", recursive=True)
        + glob.glob(directory + "/**/.*", recursive=True)
        if os.path.isfile(file)
    ]


def list_available_tempalate():
    print("Available templates:")
    for file in glob.glob(os.path.expanduser(TEMPLATE_PATH) + "*", recursive=True):
        if not os.path.isdir(file):
            continue
        print(f"  - {os.path.basename(file)}")
        files = get_all_files(file)
        for file in files:
            print(f"    - {file[1]}")
            if env.loader == None:
                continue
            template_source = env.loader.get_source(env, file[0])
            parsed_content = env.parse(template_source)  # type: ignore
            for i in list(meta.find_undeclared_variables(parsed_content)):
                print(f"      var: {i}")


def main():
    if len(sys.argv) < 2:
        print("Please specify the template name")
        list_available_tempalate()
        return

    args = sys.argv[2:]
    template_args = {}
    for arg in args:
        arg = arg.split("=")
        template_args.update({arg[0]: arg[1]})

    files = get_all_files(f"{TEMPLATE_PATH}/{sys.argv[1]}")

    if sys.argv[1] == "--list":
        list_available_tempalate()
        return

    if len(files) == 0:
        print("No Such template")
        list_available_tempalate()
        return

    for file in files:
        if os.path.dirname(file[1]) != "":
            os.makedirs(os.path.dirname(file[1]), exist_ok=True)

        t = env.get_template(file[0])
        with open(file[1], "w+") as f:
            f.write(t.render(**template_args))


if __name__ == "__main__":
    main()
