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
        results = [blast(record, 'blastn', database, remote = remote) for record in records]
        print("Results: ")
        print(results)
        no_hit_ids = [result[0] for result in results if result[1] == 0 ]
        print("Hit ids")
        print(no_hit_ids)

        records_keep = filter_records(no_hit_ids, records)

        # Write the remaining (unaligned records) back to the file
        SeqIO.write(records_keep, fasta_file, 'fasta')



def filter_records(no_hit_ids, records):

    for record in records:
        if record.id in no_hit_ids:
            yield record
        else:
            print(record.id)


def blast(record, blast_type, database = 'nr', remote = "-remote"):
    """Do a blast search and return wether a significant hit was found

    """
    if remote == '-remote':
        wait_time = random.randint(1, 10)
        time.sleep(wait_time) # Make sure we don't spam the NCBI servers all at once


    blast_cmd = "{0} -db {1} {2} -query - ".format(blast_type, database, remote)
    print(blast_cmd)
    p = sp.Popen(blast_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE, shell = True)
    blast_out, err = p.communicate(input=str(record.seq).encode())

    blast_out = blast_out.decode()
    if "Sequences producing significant alignments:" in blast_out:
        return (record.id, 1)
    elif "***** No hits found *****":
        return (record.id, 0)
    else:
        return (record.id, 0)



    return blast_out
