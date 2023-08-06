import subprocess

def run_cmd_get_output(cmd):
    process = subprocess.Popen(cmd, shell=True, executable='/bin/bash',
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out = None
    err = None
    lines = []

    while out != "" or err != "":
        out = process.stdout.readline()
        err = process.stderr.readline()
        out = out.decode("utf-8").strip('\n')
        err = err.decode("utf-8").strip('\n')
        lines.append(out)

    return lines
