import os
import sys
import subprocess



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
    


if __name__ == "__main__":
    print("START EXP")
    timeout_in_hours = 2  # 2小时
    timeout_in_seconds = timeout_in_hours * 3600  # 将小时转换为秒
    target_functions_list = parse_target_functions_list()
    print("is llm enable: " + sys.argv[1])
    print("close range: " + sys.argv[2])
    root_cwd = os.getcwd()
    
    for functions in target_functions_list:
        print("CURRENT TARGET FUNCTIONS: ")
        for func in functions:
            print(func)
        os.truncate(target_functions_file_path, 0)
        print("write target_functions.txt")
        for function in functions:
            target_functions_file = open(target_functions_file_path, "w")
            target_functions_file.write(function + "\n")
            target_functions_file.close()
            try:
                command_compenent = ["python3", "./run_experiment.py", "run", sys.argv[1], sys.argv[2]]
                # command = " ".join(command_compenent)
                result = subprocess.run(command_compenent, timeout=timeout_in_seconds, cwd=root_cwd)
            except subprocess.TimeoutExpired:
                print("TIME REACHED" + str(timeout_in_hours) + "h")

            
        