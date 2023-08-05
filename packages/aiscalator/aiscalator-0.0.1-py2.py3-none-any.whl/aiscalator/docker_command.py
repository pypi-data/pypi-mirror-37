from logging import info, debug
from os import chdir, getcwd
from os.path import dirname, basename, abspath
from re import search
from shutil import copy
from tempfile import TemporaryDirectory
from time import sleep
import webbrowser

from .utils import copy_replace, subprocess_run


class DockerLogAnalyzer(object):

    def __init__(self, pattern=None):
        self.artifact = "latest"
        self.pattern = pattern

# https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
    def log_docker_build(self, pipe):
        for line in iter(pipe.readline, b''):  # b'\n'-separated lines
            # TODO improve logging in its own subprocess log file?
            info(line)
            if self.pattern is not None:
                m = search(self.pattern, line)
                if m:
                    self.artifact = m.group(1).decode("utf-8")


# TODO this should be done in the config class instead
def extract_file_path(string):
    # TODO if string is url/git repo, download file locally first
    return abspath(string)


def extract_parameters(step):
    result = []
    for p in step["parameters"]:
        for k in p:
            result += ["-p", k, p[k]]
    return result


def notebook_output_path(notebook):
    return "/home/jovyan/work/notebook/" + \
           basename(notebook).replace(".ipynb", "") + "_out.ipynb"


def docker_build(step):
    # Retrieve configuration parameters
    dockerfile = extract_file_path(step['dockerfile'])
    docker_image_name = step['dockerImageName']
    if 'requirements' in step:
        requirements = extract_file_path(step['requirements'])
    else:
        requirements = None

    cwd = getcwd()
    try:
        # Prepare a temp folder to build docker image
        with TemporaryDirectory(prefix="aiscalator_") as tmp:
            # copy the dockerfile
            if requirements is not None:
                copy_replace(dockerfile, tmp + '/Dockerfile',
                             '#requirements.txt#', """
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt"""
                             )
                copy(requirements, tmp + '/requirements.txt')
            else:
                copy(dockerfile, tmp + '/Dockerfile')
            chdir(tmp)
            debug("Running...: docker build --rm -t " +
                  docker_image_name + " .")
            logger = DockerLogAnalyzer(b'Successfully built (\w+)\n')
            subprocess_run([
                "docker", "build", "--rm", "-t", docker_image_name, "."
            ], log_function=logger.log_docker_build)
            result = logger.artifact
    finally:
        chdir(cwd)
    return result


def prepare_docker_run_notebook(step, program):
    commands = [
        "docker", "run", "--name", step["type"] + "_" + step["name"], "--rm",
        "-p", "10000:8888",
     ]
    # TODO improve port publishing
    commands += [
        "-v", extract_file_path(dirname(step['path'])) +
        ":/home/jovyan/work/notebook/"
    ]
    for v in step["volume"]:
        for i in v:
            # TODO check if v[i] is relative path?
            # everything is mounted in the same folder
            # we can mount only local directories
            commands += [
                "-v", abspath(i) + ":/home/jovyan/work/" + v[i]
            ]
    commands += program
    debug("Running...: " + " ".join(commands))
    return commands


def docker_run_papermill(step, prepare_only=False):
    docker_image = docker_build(step)
    notebook = "/home/jovyan/work/notebook/" + \
               basename(extract_file_path(step['path']))
    notebook_output = notebook_output_path(notebook)
    parameters = extract_parameters(step)
    commands = prepare_docker_run_notebook(step, [
            docker_image, "start.sh", "papermill",
            notebook, notebook_output
    ])
    if prepare_only:
        commands.append("--prepare-only")
    commands += parameters
    logger = DockerLogAnalyzer()
    # TODO output log in its own execution log file
    subprocess_run(commands, log_function=logger.log_docker_build)
    # TODO handle notebook_output execution history and latest successful run
    return notebook_output


def docker_run_lab(step):
    docker_image = docker_build(step)
    # TODO: shutdown other jupyter lab still running
    notebook = basename(step['path'])
    if len(extract_parameters(step)) > 0:
        notebook = basename(docker_run_papermill(step, prepare_only=True))
    commands = prepare_docker_run_notebook(step, [
            docker_image, "start.sh", 'jupyter', 'lab'
    ])
    logger = DockerLogAnalyzer(b'http://.*:8888/\?token=(\w+)\n')
    subprocess_run(commands, log_function=logger.log_docker_build, wait=False)
    for i in range(5):
        sleep(2)
        if logger.artifact != "latest":
            break
        info("docker run does not seem to be up yet... retrying ("
             + str(i) + "/5)")
    # TODO handle url better (not always localhost)
    url = ("http://localhost:10000/lab/tree/work/notebook/" +
           notebook + "?token=" +
           logger.artifact)
    info(url + " is up and running.")
    # TODO --no-browser option
    webbrowser.open(url)
    return url
