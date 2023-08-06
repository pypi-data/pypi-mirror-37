repeatmodeler_dir = ""
progress_file_path = ""

class Run():

    def run_all(options):


        func_sequence = [RepeatModeler, blastPrep, blastNR, blastRFAM,
                         blastRetro, RepeatMasker, rnammer]
        entry_point = lookup_progress(options)

        for i in range(entry_point, len(func_sequence)):
            print(repeatmodeler_dir)
            func = func_sequence[i]
            func(options)




import subprocess as sp
from rnaseqpipeline.Blast import Blaster
# out_file = open("{}/out.log".format(options.install_dir), 'w') # logging standard output
# err_file = open("{}/err.log".format(options.install_dir), 'w') # Logging standeard error

def lookup_progress(options):
    """Look up if a previous run was partially finished and continue where it left of.
    This method looks for the `.progress_file` in the working directory. If absent,
    it is created, otherwise the progress is returned by this function.
    """

    return_table = {"RepeatModeler" : 1,
                    "blastPrep"     : 2,
                    "BlastNR"       : 3,
                    "BlastRFAM"     : 4,
                    "BlastRetro"    : 5,
                    "RepeatMasker"  : 6,
                    "rnammer"       : 7,
                   }

    global progress_file_path
    progress_file_path = "{}/.progress_file".format(options.workdir)

    try:
        with open(progress_file_path) as progress_file:
            global repeatmodeler_dir
            file_content = [line.rstrip("\n").split() for line in progress_file]
            names        = [line[0] for line in file_content]

            if 'RepeatModeler' in names:
                print("IN THERE")
                repeatmodeler_dir = file_content[0][1]
            else: # RepeatModeler was not finished running
                return 0

            return return_table[file_content[-1][0]]

    except FileNotFoundError:
        # TODO: Create the file
        open(progress_file_path, 'w')
        return 0

def call_sp(command):
    sp.call(command, shell = True)#, stdout = out_file, stderr = err_file)

def call_sp_retrieve(command):
    out, err = sp.Popen(command, shell = True, stdout = sp.PIPE).communicate()
    return out.decode()

def RepeatModeler(options):
    global repeatmodeler_dir
    # Prepare and Build Genome database
    prepare_cmd = "cp {} {}/genome.fa".format(options.assembly, options.workdir)
    build_cmd = "cd {}; BuildDatabase -engine ncbi -n \"genome_db\" genome.fa".format(options.workdir)
    call_sp(prepare_cmd)
    call_sp(build_cmd)


    # Run RepeatModeler
    repeatModeler_cmd = "cd {}; RepeatModeler -pa {} -database genome_db 2>&1 | tee RepeatModeler.stdout".format(
        options.workdir, options.n_threads)
    call_sp(repeatModeler_cmd)

    # Retrieve the workdir from RepeatModeler
    repeatModeler_workdir_cmd = "cd {}; cat RepeatModeler.stdout | egrep \"Working directory:  .+\"".format(
        options.workdir)

    repeatmodeler_dir = call_sp_retrieve(repeatModeler_workdir_cmd).split("  ")[1].strip("\n")

    # write progress report
    with open(progress_file_path, 'a') as progress_file:
        progress_file.write("RepeatModeler\t{}\n".format(repeatmodeler_dir))


def blastPrep(options):
     # Create folder structure
    create_folders_cmd  = "cd {}; mkdir -p blastResults; cd blastResults; mkdir -p NR; mkdir -p RFAM; mkdir -p Retrotransposon".format(options.workdir)
    cp_repeatmodel_file = "cd {}; cp {}/consensi.fa.classified blastResults".format(
        options.workdir, repeatmodeler_dir)
    call_sp(create_folders_cmd)

    # write progress report
    with open(progress_file_path, 'a') as progress_file:
        progress_file.write("blastPrep\t1\n")

def blastNR(options):
    """Blast the entries in the  RepeatModeler fasta file to the NCBI nr database.
    The results are written to a file named blast output
    """
    print("Blast NR")
    fasta_file = "{}/consensi.fa.classified".format(repeatmodeler_dir)
    out_dir    = "{}/blastResults/NR".format(options.workdir)
    n_threads  = 6 if options.n_threads > 6 else options.n_threads

    Blaster.blastFasta(fasta_file = fasta_file,
                       blast_type = 'blastn',
                       n_threads  = n_threads,
                       out_dir    = out_dir,
                       database   = "nr")
    # write progress report
    with open(progress_file_path, 'a') as progress_file:
        progress_file.write("BlastNR\t1\n")

def blastRFAM(options):
    """Blast the entries in the  RepeatModeler fasta file to the NCBI nr database.
    The results are written to a file named blast output
    """
    print("Blast RFAM")
    fasta_file = "{}/consensi.fa.classified".format(repeatmodeler_dir)
    db         = "{}/rfamDB/rfamDB.fa".format(options.workdir)
    out_dir    = "{}/blastResults/RFAM".format(options.workdir)
    n_threads  = 6 if options.n_threads > 6 else options.n_threads


    try:
        open("{}/rfamDB/rfamDB.fa".format(options.workdir))
    except FileNotFoundError:
        # we have to download the database....
        call_sp('cd {}; mkdir rfamDB; cd rfamDB; wget -c ftp://ftp.ebi.ac.uk/pub/databases/Rfam/14.0/fasta_files/*'.format(
            options.workdir))
        call_sp("cd {}/rfamDB; gunzip *; cat *.fa > rfamDB.fa; makeblastdb -dbtype nucl -in rfamDB.fa".format(options.workdir))

    Blaster.blastFasta(fasta_file = fasta_file,
                       blast_type = 'blastn',
                       n_threads  = n_threads,
                       out_dir    = out_dir,
                       database   = db,
                       remote     = "")
    print("RFAM done")

    # write progress report
    with open(progress_file_path, 'a') as progress_file:
        progress_file.write("BlastRFAM\t1\n")

def blastRetro(options):
    """Blast the entries in the  RepeatModeler fasta file to the NCBI nr database.
    The results are written to a file named blast output
    """

    fasta_file = "{}/consensi.fa.classified".format(repeatmodeler_dir)
    out_dir    = "{}/blastResults/retroDB".format(options.workdir)
    n_threads  = 6 if options.n_threads > 6 else options.n_threads



    # We have to download the database..
    call_sp("cd {0}; mkdir retroDB; cd retroDB; wget -c http://botserv2.uzh.ch/kelldata/trep-db/downloads/trep-db_complete_Rel-16.fasta.gz -O retroDB.fa.gz; gunzip retroDB.fa.gz".format(
        options.workdir))
    call_sp("cd {}/retroDB; makeblastdb -in retroDB.fa -dbtype nucl".format(options.workdir))

    db = "{}/retroDB/retroDB.fa".format(options.workdir)

    Blaster.blastFasta(fasta_file = fasta_file,
                       blast_type = 'tblastx',
                       n_threads  = n_threads,
                       out_dir    = out_dir,
                       database   = db,
                       remote     = "")
    # write progress report
    with open(progress_file_path, 'a') as progress_file:
        progress_file.write("BlastRetro\t1\n")


def RepeatMasker(options):
    """Mask repeat sequences without blast hits
    """

    mask_cmd = "cd {0}; RepeatMasker -lib {1}/consensi.fa.classified -pa {2} -gff -xsmall genome.fa".format(
        options.workdir, repeatmodeler_dir, options.n_threads)

    call_sp(mask_cmd)

    # write progress report
    with open(progress_file_path, 'a') as progress_file:
        progress_file.write("RepeatMasker\t1\n")

def rnammer(options):
    """Run rnammer
    """
    prep_cmd = "cd {}; mkdir rnammer; cp genome.fa.masked rnammer/genome.fa.masked".format(options.workdir)
    rnammer_cmd = "cd {}/rnammer; rnammer -S euk -m lsu,ssu,tsu -gff genome.masked.rnammer.gff -h genome.masked.rnammer.hmmreport -f genome.masked.rnammer.fa genome.fa.masked ".format(options.workdir)


    call_sp(prep_cmd)
    sp.call(rnammer_cmd)
