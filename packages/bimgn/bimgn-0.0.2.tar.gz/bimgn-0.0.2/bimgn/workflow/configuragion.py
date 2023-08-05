import os
import glob


class Configuration:
    def __init__(self):
        self.version = version

        job = postdata['job']
        indir = postdata['input_dir']
        sampleid = postdata['sampleid']
        outfolder = os.path.join(postdata['output_dir'], sampleid + '_IMGJ' + str(postdata['job']))
        self.stid = postdata['stid']
        url = postdata['url']
        panel = postdata['panel']

        self.r1_files = ",".join(glob.glob(os.path.join(indir, str(sampleid) + '*_R1_*')))
        self.r2_files = ",".join(glob.glob(os.path.join(indir, str(sampleid) + '*_R2_*')))

        if self.r1_files == "" or self.r2_files == "":
            raise Exception(f"FASTQ files couldn't been found in the provided directory - " +
                            f"{os.path.join(indir, str(sampleid) + '*_R1_*')}")

        self.r1_trimmed = ",".join([os.path.join(outfolder, 'raw', fastq.split('/')[-1]).replace(
            'fastq.gz', 'trimmed.fastq.gz') for fastq in self.r1_files.split(',')])
        self.r2_trimmed = ",".join([os.path.join(outfolder, 'raw', fastq.split('/')[-1]).replace(
            'fastq.gz', 'trimmed.fastq.gz') for fastq in self.r2_files.split(',')])

        self.maxthreads = os.environ['THREADS']
        self.options = self.set_options(postdata)

        if self.maxthreads is None:
            self.maxthreads = "2"

        self.DEBUG = True
        self.TESTING = False
        self.DRY_RUN = False
        self.sampleID = str(sampleid)
        self.outfolder = outfolder
        self.url = url
        self.ALU = self.options['options_process_alu']
        self.log_files = [os.path.join(outfolder, "logs", str(sampleid) + '.log')]
        self.NM_path = "/DATA/biodata/exome/nm_list.txt"
        self.process_conf = {
            "jobID": str(job),
            "build": "GRCh37",
            "threads": self.maxthreads,
            "tmp_folder": f"/tmp/{job}",
            "main_pipeline": "Exome",
            "sample": {
                "modality": 'Exoma',
                "sampleID": str(sampleid),
                "panel": panel
            }
        }

        self.tools_conf = {}