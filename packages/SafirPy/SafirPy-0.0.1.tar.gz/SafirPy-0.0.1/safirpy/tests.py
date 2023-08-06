import os
from safirpy.func import preprocess_distribute_files
from safirpy.func import preprocess_structured_directories
from safirpy.func import preprocess_safir_mc_parameters
from safirpy.func import safir_process
from safirpy.func import safir_seek_convergence
from safirpy.func import safir_problem_definition_protobuf


def _preprocess_structured_directories():
    path_work_dir = os.path.dirname('root')
    list_dir_structure = (1, 3, 2)
    list_path = preprocess_structured_directories(path_work_dir, list_dir_structure)
    for i in list_path:

        if not os.path.exists(i):
            os.makedirs(i)

        print(i)


def _safir_seek_convergence():
    path_work_directory = r'C:\safirpy_test\test_safir_seek_convergence'
    path_temp_problem_definition = r'C:\safirpy_test\template.in'
    path_safir_exe = r'C:\safirpy_test\SAFIR2016c0_proba.exe'
    seek_time_convergence_target = 1 * 60 * 60
    seek_time_convergence_target_tol = 5 * 60
    n_iteration_max = 20

    safir_seek_convergence(
        path_work_directory,
        path_temp_problem_definition,
        path_safir_exe,
        seek_time_convergence_target,
        seek_time_convergence_target_tol,
        n_iteration_max
    )


def _safir_process():
    input_file = r'C:\safirpy_test\test_safir_process\0'
    exe = r'C:\safirpy_test\SAFIR2016c0_proba.exe'
    safir_process(input_file, exe)


def _safir_problem_definition_protobuf():
    path_temp_problem_definition = r'C:\safirpy_test\template.in'
    kwargs = {'load': '-100000'}
    safir_problem_definition_protobuf(path_temp_problem_definition, **kwargs)


def _preprocess_distribute_files():
    list_path = preprocess_structured_directories(r'C:\t\misc', (1, 10))

    # for i in list_path:
    #     if not os.path.exists(i):
    #         os.makedirs(i)

    preprocess_distribute_files([r'C:\t\misc\0.tem', r'C:\t\misc\0.in'], list_path)


def _preprocess_safir_mc_parameters():
    n_rv = 10000
    dict_distribution_params = {
        'test_safir_variable': {
            'dist_name': 'norm',
            'ubound': -7,
            'lbound': 7,
            'loc': 0,
            'scale': 1,
            'kwargs': {},
            'n_rv': None
        }
    }
    dist = preprocess_safir_mc_parameters(n_rv, dict_distribution_params)
    print(dist)
    # import matplotlib.pyplot as plt
    # plt.hist(dist['test_safir_variable'], bins=100, normed=True, cumulative=True)
    # plt.show()


if __name__ == '__main__':
    print(_preprocess_safir_mc_parameters())
