# coding: utf-8
import os
from ruamel import yaml
from safirpy.func import safir_mc_host


def run(path_yaml_app_param=None):
    # ==========
    # DEFINITION
    # ==========

    path_project_root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    # App input file path
    if path_yaml_app_param is None:
        from tkinter import filedialog, Tk, StringVar
        root = Tk()
        root.withdraw()
        str_app_param = filedialog.askopenfile().read()
        dict_app_param = yaml.load(str_app_param, Loader=yaml.Loader)

    else:
        with open(path_yaml_app_param, 'r') as f:
            dict_app_param = yaml.load(f, Loader=yaml.Loader)

    # Derived

    dict_setting_param = dict_app_param['setting_parameters']
    safir_parameters = dict_app_param['safir_parameters']

    list_dir_structure = (1, dict_setting_param['n_simulations'])

    dict_setting_param['dict_str_safir_files'] = dict()

    for key, val in dict_setting_param['path_safir_files'].items():
        with open(val, 'r') as f:
            dict_setting_param['dict_str_safir_files'][key] = f.read()

    # ==========
    # GAME START
    # ==========

    safir_mc_host(
        n_proc=dict_setting_param['n_proc'],
        n_rv=dict_setting_param['n_simulations'],
        path_safir_exe=dict_setting_param['path_safir_exe'],
        path_work_root_dir=dict_setting_param['path_work_root_dir'],
        list_dir_structure=list_dir_structure,
        dict_str_safir_files=dict_setting_param['dict_str_safir_files'],
        seek_time_convergence_target=dict_setting_param['seek_time_convergence_target'],
        seek_time_convergence_target_tol=dict_setting_param['seek_time_convergence_target_tol'],
        seek_load_lbound=dict_setting_param['seek_load_lbound'],
        seek_load_ubound=dict_setting_param['seek_load_ubound'],
        seek_load_sign=dict_setting_param['seek_load_sign'],
        seek_delta_load_target=dict_setting_param['seek_delta_load_target'],
        dict_safir_params=safir_parameters,
    )


if __name__ == '__main__':
    run()
