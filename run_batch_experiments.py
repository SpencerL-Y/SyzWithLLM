import os
import sys
import subprocess
import signal
import random as rnd
from multiprocessing import active_children



target_functions_list = []
target_functions_list_file_path = "./target_functions_list.txt"
target_functions_file_path = "./target_functions.txt"

func_step_sorted_path = "./syscall_func_steps_sorted.txt"
def parse_target_functions_list():
    flist_file = open(target_functions_list_file_path, "r")
    final_result = []
    curr_target_functions = []
    for line in flist_file.readlines():
        print(line)
        if "----- target functions" in line:
            if len(curr_target_functions) != 0:
                final_result.append(curr_target_functions)
            curr_target_functions = []
        else:
            curr_target_functions.append(line.replace("\n", "").strip())
    if len(curr_target_functions) != 0:
        final_result.append(curr_target_functions)
    flist_file.close()
    return final_result

def sifting_target_functions_with_depth():
    sorted_file = open(func_step_sorted_path, "r")
    result_dict = dict()
    for line in sorted_file.readlines():
        stripped_line = line.strip().replace("\n", "")
        splitted_line = stripped_line.split(",")
        target_function = splitted_line[1].strip()
        target_function_steps_str = splitted_line[2].strip()
        target_function_steps = int(target_function_steps_str)
        if target_function_steps in result_dict:
            result_dict[target_function_steps].add(target_function)
        else:
            map_set = set()
            map_set.add(target_function)
            result_dict[target_function_steps] = map_set
    sorted_file.close()
    return result_dict

def generate_random_target_functions_list(sifted_dict):
    final_result = []
    for item in sifted_dict:
        map_set = sifted_dict[item]
        random_selection = []
        if len(map_set) > 5:
            random_selection = rnd.sample(sorted(map_set), 5)
        else:
            for set_item in map_set:
                random_selection.append(set_item)
        for target_func in random_selection:
            final_result.append([target_func])
    # write to target_functions_list.txt
    flist_file = open(target_functions_list_file_path, "w")
    for target_functions in final_result:
        if len(target_functions) > 0:
            flist_file.write("----- target functions\n")
            for target_function in target_functions:
                flist_file.write(target_function + "\n")
    flist_file.close()
    return final_result


if __name__ == "__main__":
    print("START EXP")
    target_functions_list = parse_target_functions_list()
    # sifted_dict = sifting_target_functions_with_depth()
    # target_functions_list = generate_random_target_functions_list(sifted_dict)
    print("is llm enable: " + sys.argv[1])
    print("close range: " + sys.argv[2])
    root_cwd = os.getcwd()
    
    folder_index = 0
    for functions in target_functions_list:
        print(str(folder_index) + " CURRENT TARGET FUNCTIONS: ")
        for func in functions:
            print(func)
        os.truncate(target_functions_file_path, 0)
        print("write target_functions.txt")
        target_functions_file = open(target_functions_file_path, "w")
        for function in functions:
            target_functions_file.write(function + "\n")
        target_functions_file.close()
        
        running_command_compenent = ["python3", "./run_experiment.py", "run", sys.argv[1], sys.argv[2]]
        # run experiment process
        experiment_process = subprocess.run(running_command_compenent, cwd=root_cwd)
        # copy experiment result
        copy_command_component = ["python3", "./run_experiment.py", "copy", str(folder_index)]
        print(" ".join(copy_command_component))
        result = subprocess.run(copy_command_component, cwd=root_cwd)
        
        folder_index += 1
            
        