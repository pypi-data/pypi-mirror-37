

class Install():
    """Installation class for pipeline dependenciesself.
        This class does its best job to detect if dependencies are already installed
        in the provided path, and if not, to install them.
    """

    def verify_installation(options):
        """ Veryify the installation without trying to install any missing packages
            currently not supported.

            Keyword Arguments:
                options -- argparse opject containing the command line arguments
        """
        print('veryifying the install is currently not supported')





    def perform_installation(options):
        """ Install the required tools for the pipeline to a certain directory
            Any missing tools or dependencies will be installed automatically.


            Keyword Arguments:
                options -- argparse opject containing the command line arguments
        """
        import subprocess as sp

        print('Performing installation in {} '.format(options.install_dir))

        out_file = open("{}/out.log".format(options.install_dir), 'w') # logging standard output
        err_file = open("{}/err.log".format(options.install_dir), 'w') # Logging standeard error

        def RepeatModeler():
            print_pass("Installing RepeatModeler")

            def RECON():
                # Check first if already installed
                if verify_installation('edgeredef', 'usage'):
                    print('    Skipping RECON (already installed)...')
                    return

                print("    Installing RECON...")
                recon_url = 'http://www.repeatmasker.org/RepeatModeler/RECON-1.08.tar.gz'
                download_cmd = 'wget {0} -O {1}/recon.tar.gz; cd {1}; tar xf recon.tar.gz;'.format(
                recon_url, options.install_dir
                )
                # Download and extract
                sp.call(download_cmd, shell=True, stdout=out_file, stderr = err_file)

                # Building
                sp.call('cd {}/RECON-1.08/src; make; make install'.format(options.install_dir), shell = True,
                     stdout=out_file, stderr = err_file)
                # Modify the REcon scrip to use the right paths
                sed_cmd = "sed -i 's+$path = \"\";+$path = {0}/RECON-1.08/bin+g' {0}/RECON-1.08/scripts/recon.pl".format(
                    options.install_dir)

                sp.call(sed_cmd,
                    shell=True,  stdout=out_file, stderr = err_file)
                    # Cleanup
                sp.call('rm {}/recon.tar.gz'.format(options.install_dir),
                    shell=True, stdout=out_file, stderr = err_file)

                #Add files to path
                sp.call("echo \'# RECON-1.08 installation dir\' >> ~/.bashrc; echo \'export PATH=$PATH:{0}/RECON-1.08/bin\' >> ~/.bashrc".format(options.install_dir),
                    shell = True,  stdout=out_file, stderr = err_file)

            def RepeatScout():
                if verify_installation('build_lmer_table', "Usage"):
                    print('    Skipping RepeatScout (already installed)...')
                    return

                print("    Installing RepeatScout")

                recon_url = 'http://www.repeatmasker.org/RepeatScout-1.0.5.tar.gz'
                download_cmd = 'wget {0} -O {1}/RepeatScout.tar.gz; cd {1}; tar xf RepeatScout.tar.gz;'.format(
                    recon_url, options.install_dir )

                # Download and extract
                sp.call(download_cmd,
                    shell = True,  stdout=out_file, stderr = err_file)
                # Building
                sp.call('cd {}/RepeatScout-1/ ; make'.format(options.install_dir),
                    shell = True,  stdout=out_file, stderr = err_file)

                # Cleanup
                sp.call('rm {}/RepeatScout.tar.gz'.format(options.install_dir),
                    shell=True,  stdout=out_file, stderr = err_file)

                bashrc = "echo \'# RepeatScout 1.0.5 installation dir\'; echo \'export PATH=$PATH:{}/RepeatScout-1/ \' >> ~/.bashrc".format(options.install_dir)

                sp.call(bashrc,
                    shell = True,  stdout=out_file, stderr = err_file)

            def TandenRepeatFinder():
                if verify_installation('trf409.linux64', 'Please use:'):
                    print('    Skipping TandemRepeatFinder (already installed)')
                    return

                conda_channel = "conda config --add channels {}"
                sp.call(conda_channel.format('bioconda'),
                        shell = True,  stdout=out_file, stderr = err_file)
                sp.call(conda_channel.format('conda-forge'),
                        shell = True,  stdout=out_file, stderr = err_file)
                sp.call(conda_channel.format('WURnematology'),
                        shell = True,  stdout=out_file, stderr = err_file)
                sp.call("conda install -y tandemrepeatfinder",
                        shell = True,  stdout=out_file, stderr = err_file)

                print("    TendemRepeatFinder installation complete")

            def RMBlast():

                path_check = verify_installation('{0}/ncbi-blast-2.6.0+-src/bin/blastn'.format(options.install_dir), 'BLAST query/options error')

                if path_check:
                    print("    Skipping RMBlast (already installed)")
                    return

                sp.call("conda install -y gnutls",
                    shell = True, stdout = out_file, stderr = err_file)

                cmd = "wget -c ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.6.0/ncbi-blast-2.6.0+-src.tar.gz -O {}/ncbi-blast.tar.gz".format(
                    options.install_dir)
                sp.call(cmd,
                    shell = True,  stdout=out_file, stderr = err_file)
                sp.call('cd {}; tar xf ncbi-blast.tar.gz'.format(options.install_dir),
                    shell = True,  stdout=out_file, stderr = err_file)
                sp.call('wget -c http://www.repeatmasker.org/isb-2.6.0+-changes-vers2.patch.gz -O {}/isb-2.6.0+-changes-vers2.patch.gz'.format(
                options.install_dir),
                    shell = True,  stdout=out_file, stderr = err_file)
                sp.call('gunzip -f {}/isb-2.6.0+-changes-vers2.patch.gz'.format(options.install_dir),
                    shell = True,  stdout=out_file, stderr = err_file)
                sp.call("cd {}/ncbi-blast-2.6.0+-src ; patch -p1 < ../isb-2.6.0+-changes-vers2.patch".format(options.install_dir),
                    shell = True,  stdout=out_file, stderr = err_file)
                sp.call('cd {0}/ncbi-blast-2.6.0+-src/c++; ./configure --with-mt --prefix={0}/ncbi-blast-2.6.0+-src/ --without-debug'.format(
                  options.install_dir),
                       shell = True,  stdout=out_file, stderr = err_file)
                print("        compiling ncbi blast (this takes at least an hour)")
                sp.call('cd {0}/ncbi-blast-2.6.0+-src/c++; make; make install'.format(options.install_dir),
                       shell = True,  stdout=out_file, stderr = err_file)

                path = "{0}/ncbi-blast-2.6.0+-src/bin".format(options.install_dir)


                sp.call("conda install -y blast -c bioconda", shell = True,
                    stdout = out_file, stderr = err_file)
                # Probably should not be added to the path
                #sp.call("echo \'# RMBlast installation dir\' >> ~/.bashrc; echo \'export PATH={}:$PATH\' >> ~/.bashrc".format(
                #    path
                #), shell = True,  stdout=out_file, stderr = err_file)



            def RepeatMasker():
                if verify_installation('RepeatMasker', 'RepeatMasker version'):
                    print("    Skipping RepeatMasker (Already installed)")
                    return


                print("    Installing RepeatMasker")
                sp.call('wget -c http://www.repeatmasker.org/RepeatMasker-open-4-0-7.tar.gz -O {}/RepeatMasker-open-4-0-7.tar.gz'.format(
                        options.install_dir),
                        shell = True,  stdout=out_file, stderr = err_file)
                sp.call('cd {}; tar xf RepeatMasker-open-4-0-7.tar.gz'.format(options.install_dir),
                        shell = True,  stdout=out_file, stderr = err_file)

                # By default, the configure script requires manual input for different configuration steps,
                # This is annoying in a headless installation (such as this one) therefore I modified the original
                # one so it doesn't require the manual input.
                # Download that now:
                sp.call(["wget", "http://www.bioinformatics.nl/~steen176/repeatmask_config", # Rreplace with actual URL
                "-O", "{}/RepeatMasker_CONFIG".format(options.install_dir)
                        ],  stdout=out_file, stderr = err_file)

                # Now we need to update all the paths required relative to the installation directory
                repeat_mask_cmd = "sed -i 's+ACTUALINSTALLDIR+{0}+g' {0}/RepeatMasker_CONFIG".format(
                    options.install_dir
                )
                sp.call(repeat_mask_cmd, shell = True,  stdout=out_file, stderr = err_file)

                sp.call('cd {}/RepeatMasker;cp ../RepeatMasker_CONFIG ./configure; perl configure '.format(options.install_dir),
                        shell = True,  stdout=out_file, stderr = err_file)

                sp.call("echo \'# RepeatMasker install dir\' >> ~/.bashrc ; echo \'export PATH={}/RepeatMasker:$PATH\' >> ~/.bashrc".format(
                    options.install_dir
                ),
                    shell = True,  stdout=out_file, stderr = err_file)


                sp.call("wget -O- http://cpanmin.us | perl - -l ~/perl5 App::cpanminus local::lib", shell = True)
                sp.call("eval `perl -I ~/perl5/lib/perl5 -Mlocal::lib`", shell = True)
                sp.call("echo 'eval `perl -I ~/perl5/lib/perl5 -Mlocal::lib`' >> ~/.bashrc", shell = True)
                sp.call("perl -MCPAN -Mlocal::lib -e 'CPAN::install(Text::Soundex)'", shell = True)
                sp.call("perl -MCPAN -Mlocal::lib -e 'CPAN::install(JSON)'", shell = True)
                sp.call("perl -MCPAN -Mlocal::lib -e 'CPAN::install(Module::Util)'", shell = True)

            def NSEG():
                if verify_installation('nseg', "Usage:"):
                    print("    Skipping NSEG (Already installed)")
                    return

                sp.call("mkdir {0}/nseg; cd {0}/nseg; wget ftp://ftp.ncbi.nih.gov/pub/seg/nseg/*".format(options.install_dir),
                    shell = True,  stdout=out_file, stderr = err_file)
                sp.call("cd {}/nseg; make".format(options.install_dir), shell = True,  stdout=out_file, stderr = err_file)
                sp.call("echo \'# NSEG installation dir\' >> ~/.bashrc; echo \'export PATH={}/nseg:$PATH\' >> ~/.bashrc".format(
                    options.install_dir
                ),
                    shell = True,  stdout=out_file, stderr = err_file)

            RECON()
            RepeatScout()
            TandenRepeatFinder()
            RMBlast()
            RepeatMasker()
            NSEG()


            # Actual RepeatModeler installation
            # Download the RELEASE

            if verify_installation('RepeatModeler', " RepeatModeler - Model repetitive DNA"):
                print("    RepeatModeler Already Installed")
                return


            sp.call("wget -c http://www.repeatmasker.org/RepeatModeler/RepeatModeler-open-1.0.11.tar.gz -O {}/RepeatModeler-open-1.0.11.tar.gz".format(options.install_dir),
                shell = True,  stdout=out_file, stderr = err_file)

            sp.call('cd {}; tar xf RepeatModeler-open-1.0.11.tar.gz'.format(options.install_dir),
                    shell = True,  stdout=out_file, stderr = err_file)

            # By default, the configure script requires manual input for different configuration steps,
            # This is annoying in a headless installation (such as this one) therefore I modified the original
            # one so it doesn't require the manual input.
            # Download that now:
            sp.call(["wget", "http://www.bioinformatics.nl/~steen176/repeatmodeler_config", # Rreplace with actual URL
            "-O", "{}/RepeatModeler_CONFIG".format(options.install_dir)
                    ],  stdout=out_file, stderr = err_file)

            # Now we need to update all the paths required relative to the installation directory
            repeat_mask_cmd = "sed -i 's+ACTUALINSTALLDIR+{0}+g' {0}/RepeatModeler_CONFIG; sed -i \"s+TRFBINLOCATION+$(which trf409.linux64)+g\" {0}/RepeatModeler_CONFIG".format(
                options.install_dir
            )
            sp.call(repeat_mask_cmd, shell = True,  stdout=out_file, stderr = err_file)

            sp.call('cd {}/RepeatModeler-open-1.0.11;cp ../RepeatModeler_CONFIG RepModelConfig.pm'.format(options.install_dir),
                    shell = True,  stdout=out_file, stderr = err_file)

            sp.call('sed -i "s,\#\!/u1/local/bin/perl,\#\!$(which perl),g" {}/RepeatModeler-open-1.0.11/RepeatModeler'.format(options.install_dir),
                    shell = True,  stdout=out_file, stderr = err_file) # replace the perl shebang line

            sp.call('cd {}/RepeatModeler-open-1.0.11 ; for i in *; do sed -i "s,\#\!/u1/local/bin/perl,\#\!$(which perl),g" $i; done'.format(options.install_dir),
                shell = True, stdout = out_file, stderr = err_file)

            sp.call("echo \'# RepeatModeler installation dir\' >> ~/.bashrc; echo \'export PATH={}/RepeatModeler-open-1.0.11:$PATH\' >> ~/.bashrc".format(
                options.install_dir
            ),
                shell = True,  stdout=out_file, stderr = err_file)

        def RNAmmer():
            """This will only install on one of the bioinformatics servers, as therefore
            software is only deployable within the institution. Othewise you have
            to download a copy manually
            """
            if verify_installation('rnammer -v', "This rnammer 1.2"):
                print ("Skipping RNAmmer (Already installed)")
                retur

            print_pass("Installing RNAmmer")

            sp.call("cp /home/steen176/tools/dontmove/rnammer.tar.gz {0}; cd {0}; tar xf rnammer.tar.gz".format(options.install_dir),
                shell = True, stdout = out_file, stderr = err_file)


            #sed_cmd = "sed -i 's+$path = \"\";+$path = {0}/RECON-1.08/bin+g' {0}/RECON-1.08/scripts/recon.pl".format(
            #    options.install_dir)

            sp.call("cd {0}/rnammer; sed -i \"s+INSTALLDIR+{0}/rnammer+g\" {0}/rnammer/rnammer ".format(options.install_dir),
                shell = True)


            sp.call("echo \'# rnammer installation dir\' >> ~/.bashrc; echo \'export PATH={}/rnammer:$PATH\' >> ~/.bashrc".format(
                options.install_dir
            ),
                shell = True,  stdout=out_file, stderr = err_file)

        def Maker2():
            if verify_installation('maker', 'ERROR: Control files not found'):
                print("Skipping Maker (Already installed)")
                return

            print_pass("Installing Maker2")

            conda_channel = "conda config --add channels {}"
            sp.call(conda_channel.format('bioconda'),
                    shell = True,  stdout=out_file, stderr = err_file)
            sp.call(conda_channel.format('conda-forge'),
                    shell = True,  stdout=out_file, stderr = err_file)
            sp.call(conda_channel.format('WURnematology'),
                    shell = True,  stdout=out_file, stderr = err_file)
            sp.call("conda install -y maker",
                    shell = True,  stdout=out_file, stderr = err_file)


        def Braker2():
            print_pass("Install Braker2")

            def GeneMark():
                if verify_installation('get_sequence_from_GTF.pl', 'Usage:  <gene coordinates in GTF>  <sequence in FASTA>'):
                    print("    Skipping GeneMark (Already Installed)")
                    return


                print("    Installing GeneMark")
                sp.call("cp /home/steen176/tools/dontmove/genemark/gm_et_linux_64 {}/genemark".format(options.install_dir),
                    shell = True)
                sp.call("echo \'# GeneMark ET installation dir\' >> ~/.bashrc; echo \'export PATH={}/genemark:$PATH\' >> ~/.bashrc".format(options.install_dir),
                    shell = True)

            GeneMark()

            if verify_installation("braker.pl", "Pipeline for predicting genes with GeneMark-ET and AUGUSTUS"):
                print("    Skipping Braker (Already installed)")

            #Actual installation
            sp.call("wget http://exon.gatech.edu/Braker/BRAKER2.tar.gz -O {0}/BRAKER2.tar.gz; cd {0} tar xf BRAKER2.tar.gz".format(options.install_dir),
                shell = True)


            sp.call("perl -MCPAN -Mlocal::lib -e 'CPAN::install(Scalar::Util::Numeric)'", shell = True)
            sp.call("perl -MCPAN -Mlocal::lib -e 'CPAN::install(File::Spec::FUnctions)'", shell = True)
            sp.call("perl -MCPAN -Mlocal::lib -e 'CPAN::install(Hash::Merge)'", shell = True)
            sp.call("perl -MCPAN -Mlocal::lib -e 'CPAN::install(List::Util)'", shell = True)
            sp.call("perl -MCPAN -Mlocal::lib -e 'CPAN::install(Logger::Simple)'", shell = True)
            sp.call("perl -MCPAN -Mlocal::lib -e 'CPAN::install(Module::Load::Conditional)'", shell = True)
            sp.call("perl -MCPAN -Mlocal::lib -e 'CPAN::install(Parallel::ForkManager)'", shell = True)
            sp.call("perl -MCPAN -Mlocal::lib -e 'CPAN::install(POSIX)'", shell = True)
            sp.call("perl -MCPAN -Mlocal::lib -e 'CPAN::install(YAML)'", shell = True)
            sp.call("perl -MCPAN -Mlocal::lib -e 'CPAN::install(File::Which module)'", shell = True)


            sp.call("echo \'# BRAKER2 Installation dir\' >> ~/.bashrc; echo \'export PATH=$PATH:{}/BRAKER_v2.1.0\' >>  ~/.bashrc".format(options.install_dir),
                shell = True)

        RepeatModeler()
        RNAmmer()
        Maker2()
        Braker2()



def verify_installation(command, required_out):
    import subprocess as sp

    required_out = required_out.encode()
    try:
        out, err = sp.Popen(command, stdout = sp.PIPE, stderr = sp.PIPE, shell = True).communicate()
        if required_out in out or required_out in err: # This check is only to be safe, it will not reach the else
            return True
        else:
            return False
    except FileNotFoundError:
        return False


import sys
def print_pass(message, end = '\n'):
    sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)
