import os


class Software:
    def __init__(self):
        pass

    def get_init_var(self):
        """
        Docstring
        """

        ngs_software_bin = os.getenv('BIN_BIOTOOLS')
        refgenomes = os.getenv('REFGENOMES')
        output_dir = os.getenv('OUTPUT_DIR')
        plasmid_ref = os.getenv('PLASMID_REF')
        vep_cache = os.getenv('VEPCACHE')
        biodata = os.getenv('BIODATA')
        mode = os.getenv('MODE')

        init_conf = {
            'BIN_BIOTOOLS': ngs_software_bin,
            'REFGENOMES': refgenomes,
            'OUTPUT_DIR': output_dir,
            'PLASMID_REF': plasmid_ref,
            'VEPCACHE': vep_cache,
            'BIODATA': biodata,
            'MODE': mode
        }

        if any(a is None for a in [ngs_software_bin, refgenomes, output_dir, plasmid_ref]):
            for key in init_conf:
                print(key + ' -> "' + str(init_conf[key]) + '"')
            raise Exception('#[ERR]: One of the variables is not set')

        return init_conf

    def return_software(self):
        init_conf = self.get_init_var()
        ngs_software_bin = init_conf['BIN_BIOTOOLS']
        plasmid_ref = init_conf['PLASMID_REF']
        vep_cache = init_conf['VEPCACHE']

        config = dict()

        config['ref'] = {
            # Ref Genomes
            "GRCh38": os.path.join(init_conf['REFGENOMES'], 'hs38', 'hs38.fa'),
            "GRCh37": os.path.join(init_conf['REFGENOMES'], 'hs37d5', 'hs37d5.fa')
        }

        software = {
            "bwa-mem": {
                "v0.7.15": {
                    "bwa-mem": os.path.join(ngs_software_bin, 'bwa')
                }
            },

            "samtools": {
                "v1.7": {
                    "samtools": os.path.join(ngs_software_bin, 'samtools'),
                }
            },

            "htslib": {
                "v1.7": {
                    "bgzip": os.path.join(ngs_software_bin, 'bgzip'),
                    "tabix": os.path.join(ngs_software_bin, 'tabix'),
                }
            },

            "freebayes": {
                "v1.1.0": {
                    "freebayes": os.path.join(ngs_software_bin, 'freebayes'),
                }
            },

            "annovar": {
                "v20160205": {
                    "ANNOVAR": os.path.join(ngs_software_bin, 'table_annovar.pl'),
                }
            },

            "bedtools": {
                "v2.26.0": {
                    "bedtools": os.path.join(ngs_software_bin, 'bedtools'),
                }
            },
            "picard": {
                "v2.9.0": {
                    "picard": os.path.join(ngs_software_bin, 'picard.jar')
                }
            },
            "snpsift": {
                "v4.3k": {
                    "snpsift": os.path.join(ngs_software_bin, 'SnpSift.jar'),
                    "snpeff": os.path.join(ngs_software_bin, 'snpEff.jar'),
                }
            },

            "fastQC": {
                "v0.11.5": {
                    "fastQC": os.path.join(ngs_software_bin, 'fastqc'),
                }
            },

            "bbduk": {
                "v37.56": {
                    "bbduk": os.path.join(ngs_software_bin, 'bbduk.sh'),
                }
            },

            "RTG": {
                "v3.8.4": {
                    "RTG": os.path.join(ngs_software_bin, 'RTG.jar')
                }
            },

            "vcfallelicprim": {
                "v0.0": {
                    "vcfallelicprim": os.path.join(ngs_software_bin, 'vcfallelicprimitives'),
                }
            },

            "vt": {
                "v0.1": {
                    "VT": os.path.join(ngs_software_bin, 'vt'),
                }
            },
            "sort_bed": {
                "v0.1": {
                    "sort_bed": os.path.join(ngs_software_bin, 'sort_bed'),
                }
            },

            "gemini": {
                "v0.20.1": {
                    "gemini": os.path.join(ngs_software_bin, 'gemini'),
                }
            },

            "vep": {
                "v92.1": {
                    "vep": os.path.join(ngs_software_bin, 'vep'),
                }
            },

            "vardict": {
                "v1.5.1": {
                    "vardict": os.path.join(ngs_software_bin, 'VarDict_1.5.1')
                },
                "v1.5.2": {
                    "vardict": os.path.join(ngs_software_bin, 'VarDict_1.5.2')
                },
                "v1.5.3": {
                    "vardict": os.path.join(ngs_software_bin, 'VarDict_1.5.3')
                },

            },
            "vardict-script": {
                "v1.5.1": {
                    "vardictsomatic": os.path.join(ngs_software_bin, 'testsomatic.R'),
                    "vardictpaired": os.path.join(ngs_software_bin, 'var2vcf_paired.pl'),
                    "vardictsb": os.path.join(ngs_software_bin, 'teststrandbias.R'),
                    "vardictvar2vcf": os.path.join(ngs_software_bin, 'var2vcf_valid.pl'),
                }
            },

            "igvtools": {
                "v2.3.98": {
                    "igvtools": os.path.join(ngs_software_bin, 'igvtools.jar'),
                }
            },

            "bamclipper": {
                "v1.0.0": {
                    "bamclipper": os.path.join(ngs_software_bin, 'bamclipper.sh'),
                }
            },

            "cutprimers": {
                "v1.2": {
                    "cutprimers": os.path.join(ngs_software_bin, 'cutPrimers.py'),
                }
            },
            "bcl2fastq": {
                "v0.0.0": {
                    "bcl2fastq": os.path.join(ngs_software_bin, 'bcl2fastq'),
                }
            },

            "agent": {
                "v4.0.1": {
                    "agent": os.path.join(ngs_software_bin, 'LocatIt_v4.0.1.jar'),
                }
            },
            "lumpy": {
                "v0.2.12": {
                    "lumpy": os.path.join(ngs_software_bin, 'lumpy'),
                    "lumpy_paired": os.path.join(ngs_software_bin, 'pairend_distro.py'),
                    "lumpy_splitreads": os.path.join(ngs_software_bin, 'extractSplitReads_BwaMem'),
                },
            },
            "samblaster": {
                "v0.1.24": {
                    "samblaster": os.path.join(ngs_software_bin, 'samblaster'),
                }
            },
            "imegen": {
                "v0.0": {
                    "imegen": ""
                }
            },
            "qualimap": {
                "v2.2.1": {
                    "qualimap": os.path.join(ngs_software_bin, 'qualimap')
                }
            },

            "additional_data": {
                "v0.0": {
                    "REFERENCE_GENOME": "/DATA/biodata/refGenomes/hs37d5/hs37d5.fa",
                    "HUMANDB": os.path.join(ngs_software_bin, 'annov_humandb'),
                    "NEXTERAPE": os.path.join("/DATA/biodata/NexteraPE-PE.fa"),
                    "VEPCACHE": vep_cache,
                    "VEPDB": os.path.join('/DATA/biodata/vep/'),
                    "PLASMID_REF": os.path.join(plasmid_ref, 'plasm_stidk_seq.fa'),
                    "PLASMID_IDX": os.path.join(plasmid_ref, 'indexes.tsv'),
                    "PLASMID_BED": os.path.join(plasmid_ref, 'regions_stidk.bed'),
                    "IMEGENDB": os.path.join(ngs_software_bin, 'test.db'),
                    "BUILD": "GRCh37"
                }
            }
        }

        return software

    @staticmethod
    def check_config_paths(config):
        """
        Docstring
        """
        for software in config['software']['paths']:
            path = config['software']['paths'][software]
            if isinstance(path, str) and not os.path.lexists(path):
                print("Software " + software + " does not exists -> " + path)
                print("Exiting...")
                exit(1)

        for reference in config['ref']:
            path = config['ref'][reference]
            if isinstance(path, str) and not os.path.exists(path):
                print("#[WARN]: Reference " + reference + " does not exists -> " + path)

        for db in config['dbs']:
            path = config['dbs'][db]
            if isinstance(path, str) and not os.path.exists(path) and db != 'IMEGENDB':
                print("Database " + db + " does not exists -> " + path)
                print("Exiting...")
                exit(1)

        for data in config['software']['data']:
            path = config['software']['data'][data]
            if isinstance(path, str) and not os.path.exists(path):
                print("Data " + data + " does not exists -> " + path)
                print("Exiting...")
                exit(1)

    @staticmethod
    def default_versions():
        using_software = {
            'fastQC': {"name": "fastQC", "version": "v0.11.5"},
            'bbduk': {"name": "bbduk", "version": "v37.56"},
            'qualimap': {"name": "qualimap", "version": "v2.2.1"},
            'bwa-mem': {"name": "bwa-mem", "version": "v0.7.15"},
            'samtools': {"name": "samtools", "version": "v1.7"},
            'cutprimers': {"name": "cutprimers", "version": "v1.2"},
            'bedtools': {"name": "bedtools", "version": "v2.26.0"},
            'picard': {"name": "picard", "version": "v2.9.0"},
            'igvtools': {"name": "igvtools", "version": "v2.3.98"},
            'vardict': {"name": "vardict", "version": "v1.5.1"},
            'vardict-script': {"name": "vardict-script", "version": "v1.5.1"},
            'RTG': {"name": "RTG", "version": "v3.8.4"},
            'sort_bed': {"name": "sort_bed", "version": "v0.1"},
            'snpsift': {"name": "snpsift", "version": "v4.3k"},
            'vep': {"name": "vep", "version": "v92.1"},
            'lumpy': {"name": "lumpy", "version": "v0.2.12"},
            'imegen': {"name": "imegen", "version": "v0.0"},
            'samblaster': {'name': "samblaster", "version": "v0.1.24"},
            'agent': {'name': 'agent', 'version': 'v4.0.1'},
            'additional_data': {'name': 'additional_data', 'version': 'v0.0'}
        }

        return using_software
