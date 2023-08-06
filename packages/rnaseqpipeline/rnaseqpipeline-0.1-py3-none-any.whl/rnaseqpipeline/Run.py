class Run():

    def run_all(options):

        repeatmodeler_dir = RepeatModeler(options)
        blastPrep(options, repeatmodeler_dir)

        blastNR(options)


import subprocess as sp
# out_file = open("{}/out.log".format(options.install_dir), 'w') # logging standard output
# err_file = open("{}/err.log".format(options.install_dir), 'w') # Logging standeard error

def call_sp(command):
    sp.call(command, shell = True)#, stdout = out_file, stderr = err_file)

def call_sp_retrieve(command):
    out, err = sp.Popen(command, shell = True, stdout = sp.PIPE).communicate()
    return out.decode()

def RepeatModeler(options):

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

    return repeatmodeler_dir

def blastPrep(options, repeatmodeler_dir):
     # Create folder structure
    create_folders_cmd  = "cd {}; mkdir blastResults; cd blastResults; mkdir NR; mkdir RFAM; mkdir Retrotransposon".format(options.workdir)
    cp_repeatmodel_file = "cd {}; cp {}/consensi.fa.classified blastResults".format(
        options.workdir, repeatmodeler_dir)
    call_sp(create_folders_cmd)

    fasta_split_cmd = "cd {}/blastResults; fastaSplitter -i {}/consensi.fa.classified -n {}".format(
        options.workdir, repeatmodeler_dir, options.n_threads)

def blastNR(options):
    blastNR_cmd = "cd {}/blastResults/NR; for file in ../consensi_*; do  blastx -db nr -remote -query $file -evalue 10e-5 -out $(basename $file .fa).blastx.out & done".format(
        options.workdir)
    call_sp(blastNR)
