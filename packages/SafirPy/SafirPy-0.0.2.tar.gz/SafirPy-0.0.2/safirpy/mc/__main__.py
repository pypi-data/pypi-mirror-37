import os
from ruamel import yaml
from safirpy.func import safir_mc_host
from tkinter import filedialog, Tk, StringVar


def run(path_yaml_app_param=None):
    # ==========
    # DEFINITION
    # ==========

    # App input file path
    if path_yaml_app_param is None:
        root = Tk()
        root.withdraw()
        text_io = filedialog.askopenfile()
        path_yaml_app_param = text_io.name
        if path_yaml_app_param == '':
            return -1
        else:
            dict_app_param = yaml.load(text_io.read(), Loader=yaml.Loader)

    else:
        with open(path_yaml_app_param, 'r') as f:
            dict_app_param = yaml.load(f, Loader=yaml.Loader)

    # Derived
    path_work_dir = os.path.dirname(path_yaml_app_param)

    dict_setting_param = dict_app_param['setting_parameters']
    dict_safir_param = dict_app_param['safir_parameters']

    list_dir_structure = (1, dict_setting_param['n_simulations'])

    dict_setting_param['dict_str_safir_files'] = dict()

    # read template input files and store the strings
    for key, val in dict_setting_param['path_safir_files'].items():
        val = os.path.join(path_work_dir, val) if not os.path.isabs(val) else val
        with open(val, 'r') as f:
            dict_setting_param['dict_str_safir_files'][key] = f.read()

    # check and change to absolute path
    if not os.path.isabs(dict_setting_param['path_safir_exe']):
        dict_setting_param['path_safir_exe'] = os.path.join(path_work_dir, dict_setting_param['path_safir_exe'])

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
        dict_safir_params=dict_safir_param,
    )


if __name__ == '__main__':
    run()
