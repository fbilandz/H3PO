from condor.paths import *

if __name__ == '__main__':

    datasets = ["QCD2000", "QCD1000", "QCD1500", "QCD700", "TTbarHadronic", "TTbarSemileptonic"]

    # for file in dataset:
    #     f_test2 = ROOT.TFile(file)
    
    from os import listdir, system
    from os.path import join, isfile
    from combine_histograms import combine_histograms
    
    num_of_jobs = {}
    
    for dataset in datasets:
        dataset_path = join(SKIM_DIR, '2017', dataset)
        with open('args-' + dataset + '.txt', 'w') as args_file:
            num_of_jobs[dataset] = 0
            for file in listdir(dataset_path):
                file_path = join(dataset_path, file)
                if not isfile(file_path):
                    continue
                args_file.write('-s={0} -f={1} -fp={2}\n'.format(dataset, file, file_path))
                num_of_jobs[dataset] += 1
                
        with open('job_desc' + dataset + '.txt', 'w') as job_file:
            job_file.write('executable = run.sh\n')
            job_file.write('universe    =  vanilla\n')
            job_file.write('initialdir  =  /users/fbilandzija/H3PO/Analysis\n')
            job_file.write('getenv = True\n')

            job_file.write('log = log' + dataset + '.log\n')
            job_file.write('Arguments = "$(args)" \n')
            job_file.write('Output = tmp' + '-' + dataset + '.out\n')
            job_file.write('error =  tmp.err\n')
            job_file.write('Queue args from {0}\n'.format('args-' + dataset + '.txt'))
            job_file.write('queue\n\n')
        system('condor_submit job_desc' + dataset + '.txt')
        
    print("Waiting for all jobs to finish...")
    for dataset in datasets:
        system('condor_wait log' + dataset + '.log')
        combine_histograms(dataset, "2b-tagged_jets")
        
    print("All jobs finished.")

