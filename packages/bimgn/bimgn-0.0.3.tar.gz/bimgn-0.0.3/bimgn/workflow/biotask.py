import os
import subprocess
import time
from bimgn.utils.logs import Log
from bimgn.utils.softwares import Software
from bimgn.workflow.it_api import LoggerApi


class BioTask:

    def __init__(self, config=None, tool_name=None):
        """Creation of the class

        The basic configuration of the class must be set.
        """

        # Launch the methods that are going to build the entire class
        # configuration

        log = Log()
        self.mode = self.get_mode()
        if config is not None:
            self.log = log.set_log(type(self).__name__, config['log_files'])
        else:
            self.log = log.set_log(type(self).__name__)

        try:
            self.log.debug(config['tools_conf'][tool_name])
        except:
            self.log.warn("#[WARN] -> Could not write config info")

        self.pid = 0
        self.max_ram_memory = self.set_memory()
        self.exec_softwares = {}

        if config is not None:
            self.config = config

            self.tool_name = tool_name
            self.execution_time = None

            if tool_name is not None:
                self.tool_config = self.config['tools_conf'][tool_name]
                if self.tool_config != {}:
                    pass

            self.tool_software = self.assign_softwares()
            if self.tool_config['software'] != {}:
                self.call_change_software_version(self.tool_config['software'])

            self.logger = self.set_api_logger(config)

            self.log.info(f"Created {type(self).__name__} class")
            self.log.debug(f"{type(self).__name__} - {self.tool_config}")

            self.threads = self.set_threads()

            self.tmp_folder = self.set_tmp_folder()

            self.cmd, self.rm_cmd = "", ""

    def get_mode(self):
        mode = os.environ['MODE']
        return mode

    def set_api_logger(self, config):

        if self.mode != 'TEST':
            logger = LoggerApi(config['url'], type(self).__name__)
        else:
            logger = None

        return logger

    def assign_softwares(self):

        software = Software()
        software_data = software.return_software()

        software_default = software.default_versions()

        softwares = {}

        for soft in software_default:
            soft = software_default[soft]
            for name in software_data[soft['name']][soft['version']].keys():
                softwares[name] = {
                    'path': software_data[soft['name']][soft['version']][name],
                    'version': soft['version']
                }

        for key in software_data['additional_data'].keys():

            softwares[key] = software_data['additional_data'][key]

        self.check_software(softwares)

        return softwares

    def use_software(self, software):
        software_path = self.tool_software[software]['path']
        version = self.tool_software[software]['version']
        self.log.info(f"#[INFO][SOFTWARE] - {software},{version},{software_path}")
        return software_path

    @staticmethod
    def check_software(softwares):
        for software in softwares.keys():
            if software in ["REFERENCE_GENOME", "HUMANDB", "NEXTERAPE", "VEPCACHE", "VEPDB", "PLASMID_REF",
                            "PLASMID_IDX", "PLASMID_BED", "IMEGENDB", "BUILD", 'imegen', 'additional_data', 'v0.0']:
                continue
            if not os.path.exists(softwares[software]['path']):
                raise Exception(f"Software {softwares[software]['path']} not found in path")

    def call_change_software_version(self, software_dict):

        tool_softwares = self.assign_softwares()

        for key_software in software_dict.keys():
            software = software_dict[key_software]

            if 'version' in software:
                old_software_version = tool_softwares[software['name']]['version']
                new_software_version = software['version']

                if old_software_version != new_software_version:
                    self.log.warn(f"Using different version for software {software['name']} " +
                                  f"({old_software_version} -> {new_software_version})")
                else:
                    self.log.info(f"Using same version for software {software['name']} " +
                                  f"({old_software_version} -> {new_software_version})")

                try:
                    software_builtin = Software()
                    software_data = software_builtin.return_software()

                    return software_data[software['main_name']][new_software_version][software['name']]

                except KeyError:
                    self.log.error(f"#[ERR]: There is no version for the indicated software ({software['name']})")
                    raise Exception(f"#[ERR]: There is no version for the indicated software ({software['name']})")

        return tool_softwares


    def set_sample_id(self):
        """Method to return the id of the analyzed case"""

        if "sampleID" in self.config['process_conf']['sample'].keys():
            sample_id = self.config['process_conf']['sample']['sampleID']
        else:
            sample_id = self.config['process_conf']['sample']['trioID']

        return sample_id

    def set_tmp_folder(self):
        """Method to set a temporal folder"""
        if 'tmp_folder' in self.config['process_conf']:
            tmp_folder = self.config['process_conf']['tmp_folder']
        else:
            tmp_folder = "/tmp/"

        return tmp_folder

    def set_threads(self):
        """Method to set the threads used by the tool. Number of threads should be"""
        if 'threads' in self.tool_config['tool_conf']:
            threads = self.tool_config['tool_conf']['threads']
        elif 'threads' in self.config['process_conf']:
            threads = self.config['process_conf']['threads']
        else:
            threads = "1"

        try:
            int(threads)
        except ValueError:
            raise Exception("Number of threads could not be converted to integer")

        try:
            assert(int(threads) <= 0)
        except AssertionError as ass_err:
            print(ass_err)
        else:
            pass
        finally:
            pass

        return threads

    def set_memory(self):
        memory = os.getenv("MAX_MEMORY")
        # todo validate memory
        if memory is None:
            # return "-Xmx5g"
            return ""
        else:
            return "-Xmx" + memory

    def set_pid(self, pid):
        self.pid = pid

    def run(self):
        import time
        init_time = time.time()

        if self.config['process_conf']['sample']['modality'] == 'Trios':
            if 'sample' in self.tool_config['tool_conf'].keys():
                name = type(self).__name__ + ' - ' + self.tool_config['tool_conf']['sample']
            else:
                name = type(self).__name__
        else:
            name = type(self).__name__

        # Only talk to the API when a logger exists
        if self.logger is not None:
            self.logger.iniciar_paso(name, self.config['process_conf']['sample']['modality'], self.log)

        # Execute the tool
        self.run_process()

        # Finalyze process and calculate time
        end_time = time.time()
        self.execution_time = str(round(end_time - init_time, 2))
        self.log.debug(f'__time__ - {name} - {self.execution_time} s')

        # Only talk to the API when a logger exists
        if self.logger is not None:
            self.logger.finalizar_paso(name, self.config['process_conf']['sample']['modality'], self.log)
            self.logger.informar(f"{name} result")

    @staticmethod
    def build_rm_cmd():
        return ''

    def build_cmd(self):
        raise Exception("Method 'build_cmd' is  not set.")

    def get_task_options(self):
        return self.tool_config

    def cmd_run(self, mode=3):

        cmd = self.build_cmd()
        rm_cmd = self.build_rm_cmd()
        print(cmd)

        # If dry_run, don't run the process, just print it
        if self.config['DRY_RUN'] is True:
            self.log.info('Generating CLI command...')
            self.log.info(cmd)

        else:
            if mode == 1:
                self.log.info('Running command...')
                process = subprocess.Popen(cmd, shell=True, executable='/bin/bash',
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)

                self.log.info(f"Initializing process {type(self).__name__} - PID: {process.pid}")
                self.set_pid(process.pid)

                out = None
                err = None
                lines = []

                self.log.debug("Printing software log:")
                while out != "" or err != "":
                    out = process.stdout.readline()
                    err = process.stderr.readline()
                    out = out.decode("utf-8").strip('\n')
                    err = err.decode("utf-8").strip('\n')
                    self.log.debug(err)
                    lines.append(out)

                return lines

            elif mode == 2:
                os.system(cmd)

            elif mode == 3:
                f_stdout = open("/tmp/full.stdout.log", "w+")
                f_stderr = open("/tmp/full.stderr.log", "w+")
                # Using pipe in command could block the stdout, see this post:
                # https://thraxil.org/users/anders/posts/2008/03/13/Subprocess-Hanging-PIPE-is-your-enemy/
                # https://www.reddit.com/r/Python/comments/1vbie0/subprocesspipe_will_hang_indefinitely_if_stdout/
                self.log.info('Running command...')
                process = subprocess.Popen(cmd, shell=True, executable='/bin/bash',
                                           stdout=f_stdout, stderr=f_stderr)
                self.log.info(f"Initializing process {type(self).__name__} - PID: {process.pid}")
                self.set_pid(process.pid)

                while process.poll() is None:
                    time.sleep(5)

                f_stdout.close()
                f_stderr.close()

                if process.returncode != 0:

                    # If a temporal folder has been used, try to retrieve a removing command
                    if rm_cmd != '':
                        self.log.debug(f"Process {type(self).__name__} failed. Command failed running")
                        self.log.debug(f"Activation of removal of temporal files...")
                        f_stdout = open("/tmp/full.stdout.log", "w+")
                        f_stderr = open("/tmp/full.stderr.log", "w+")
                        p = subprocess.Popen(rm_cmd, shell=True, executable='/bin/bash', stdout=f_stdout,
                                             stderr=f_stderr)
                        while process.poll() is None:
                            time.sleep(5)

                        f_stdout.close()
                        f_stderr.close()

                    raise Exception(f"Process {type(self).__name__} failed. Command failed running")

        self.log.info(f"Finished process {type(self).__name__} with exit status 0")

    def run_cmd_get_output(self, cmd):
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
