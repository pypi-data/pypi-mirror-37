#!/usr/bin/env python

from Bio import SeqIO
from joblib import Parallel, delayed
import multiprocessing
import subprocess as sp
import random
import time


class Blaster():

    def blastFasta(fasta_file, blast_type, n_threads, out_dir, database = 'nr', remote = '-remote'):
        """Blast all records in a fasta fileself.
        Blasting can be done parallelized, to reduce execution times (recommended is not to use to many threads).

            Keyword Arguments:
                fasta_file -- str, filepath
                blast_type -- str, blast type to use. E.g. blastn, blastp, blastx, etc.
                n_threads  -- int, number of parallel blast threads to use.
                database   -- str, blast database to use, may either be a standard (remote) database or a local one.
                remote     -- str, argument to indicate if the blast database is remote. Argument should either be "-remote" or ""
        """
        # Parse the fast file
        records = list(SeqIO.parse(fasta_file, 'fasta'))

        # Parallel execution
        #results = Parallel(n_jobs = n_threads)(delayed(blast) (i, blast_type, database) for i in records)
        results = [blast(record, 'blastn', database) for record in records]

        # Output all results to a file single-threaded
        with open('{}/blast{}_output.txt'.format(out_dir, database), 'w') as out_file:
            for result in results:
                print(result)
                print("\nJORIS TIME\n")
                 # TODO: FIgure out what I want to do with the outputs
                 # Do we store them in memory / in file/ both?
                # out_file.write(result)
                # out_file.write("\n")



def blast(record, blast_type, database = 'nr', remote = "-remote"):
    """Do a blast search and return wether a significant hit was found

    """
    if remote == '-remote':
        wait_time = random.randint(1, 10)
        time.sleep(wait_time) # Make sure we don't spam the NCBI servers all at once


    blast_cmd = "{0} -db {1} {2} -query - ".format(blast_type, database, remote)

    p = sp.Popen(blast_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE, shell = True)
    blast_out, err = p.communicate(input=str(record.seq).encode())

    blast_out = blast.out.decode()
    if "Sequences producing significant alignments:" in blast_out:
        print("SIGNIFICANT RESULT FOUND FOR {}".format(record.id))
        return (record.id, 1)
    elif "***** No hits found *****":
        print("NO HITS FOR {}".format(record.id))
        return (record.id, 0)
    else:
        return (record.id, 0)



    return blast_out
