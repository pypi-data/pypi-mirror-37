repeatmodeler_dir = ""
progress_file_path = ""
class Run():

    def run_all(options):


        sequence = [RepeatModeler, blastPrep, blastNR]
        entry_point = lookup_progress(options)

        for i in range(entry_point, len(sequence)):
            print(repeatmodeler_dir)
            func = sequence[i]
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
                    "blastRFAM"     : 4,
                   }

    global progress_file_path
    progress_file_path = "{}/.progress_file".format(options.workdir)

    try:
        with open(progress_file_path) as progress_file:
            global repeatmodeler_dir
            file_content = [line.rstrip("\n") for line in progress_file]

            # currently a hack
            repeatmodeler_dir = file_content[0].split()[1]
            return 2
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
    prepare_cmd = "cp {} {}".format(options.assembly, options.workdir)
    build_cmd = "cd {}; BuildDatabase -engine ncbi -n \"genome_db\" {}".format(options.workdir,
                                                                               options.assembly)
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
    """Blast the entries in the  RepeatModler fasta file to the NCBI nr database.
    The results are written to a file named blast output
    """
    fasta_file = "{}/consensi.fa.classified".format(repeatmodeler_dir)
    out_dir    = "{}/blastResults/NR".format(options.workdir)
    Blaster.blastFasta(fasta_file = fasta_file,
                       blast_type = 'blastn',
                       n_threads  = 6,
                       out_dir    = out_dir,
                       database   = "nr")
