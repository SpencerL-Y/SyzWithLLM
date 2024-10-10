import re
import os
import sys
import matplotlib.pyplot as plt


target_functions = 'target_functions.txt'
input_functions = 'input_functions.txt'
experiment_output = 'experiment_output_llmenabled.txt'
output = 'exp_data_result.txt'

list_all = []

def extract_functions(file):
    with open(file, 'r') as file:
        functions = [line.strip() for line in file.readlines()]
    return functions

def extract_experiment_data(file):
    all_coverage_exec = []
    all_hit_times = []
    all_errors = []
    coverage_pattern = re.compile(r'coverage=(\d+) exec total=(\d+)')
    hit_times_pattern = re.compile(r'Hit times: (\d+)')
    error_1 = re.compile(r'close ask Output: ```plaintext')
    error_2 = re.compile(r'This model\'s maximum context length')

    with open(file, 'r') as file:
        content = file.read()

    coverage_execs = coverage_pattern.findall(content)
    for cover, exec in coverage_execs:
        coverage = int(cover)
        exec_total = int(exec)
        cover_exec = [coverage, exec_total]
        all_coverage_exec.append(cover_exec)
    hit_times = hit_times_pattern.findall(content)
    for time in hit_times:
        hit_time = int(time)
        all_hit_times.append(hit_time)
    errors_1 = error_1.findall(content)
    errors_2 = error_2.findall(content)
    error_1_count = len(errors_1)
    error_2_count = len(errors_2)
    return all_coverage_exec, all_hit_times, error_1_count, error_2_count

def process(target_functions_file, input_functions_file, experiment_output_file):
    list = []
    target_functions = extract_functions(target_functions_file)
    input_functions = extract_functions(input_functions_file)
    list.append(target_functions)
    list.append(input_functions)
    all_coverage_exec, all_hit_times, error1, error2 = extract_experiment_data(experiment_output_file)
    list.append(all_coverage_exec)
    list.append(all_hit_times)
    list.append([error1,error2])
    return list

def process_data(list):
    '''
    print(list)
    print(len(list))
    print("***************")
    '''
    cov_list = []
    exec_list = []
    for cov, exec in list:
        cov_list.append(cov)
        cov_list.append(cov)
        exec_list.append(exec)
        exec_list.append(exec)

    cov_list.pop(-1)
    exec_list.pop(0)
    '''
    print(cov_list)
    print(len(cov_list))
    print("***************")
    print(exec_list)
    print(len(exec_list))
    '''
    return exec_list, cov_list

def draw_chart(x_list, y_list, count):
    plt.figure()
    plt.plot(x_list, y_list, color='blue')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('test')
    plt.savefig('image' + str(count) + '.png')
    plt.clf()

def draw_compare_chart(enable_x_list, enable_y_list, disable_x_list, disable_y_list, count):
    plt.figure()
    plt.plot(enable_x_list, enable_y_list, color='blue')
    plt.plot(disable_x_list, disable_y_list, color='red')
    plt.xlabel('coverage')
    plt.ylabel('exec num')
    plt.title('Compare')
    plt.show()
    plt.savefig('image' + str(count) + '.png')
    plt.clf()


def main():
    # assume the script in the experiment_result folder.
    os.chdir("./temp")
    count = 0
    while os.path.isdir(os.getcwd()+"/"+ str(count)):
        os.chdir("./" + str(count))
        one_experiment_output = process(target_functions, input_functions, experiment_output)
        list_all.append(one_experiment_output)
        os.chdir("..")
        count += 1
    os.chdir("..")
    with open(output, "w") as file:
        file.write(repr(list_all))
    chart_number = 0
    for l in list_all:
        x_list, y_list = process_data(l[2])
        draw_chart(x_list, y_list, chart_number)
        chart_number += 1

def draw_compare_specific_count(specific_id):
    disable_list_all = []
    enable_list_all = []
    batch_id_bound = 2
    batch_id = 2
    while batch_id <= batch_id_bound:
        disable_dir_name = "./disable_batch_" + str(batch_id)
        enable_dir_name = "./enable_batch_" + str(batch_id)
        if not os.path.isdir(disable_dir_name + "/" + str(specific_id)) or not os.path.isdir(enable_dir_name + "/" + str(specific_id)):
            batch_id += 1
            continue

        print("curr id: " + str(specific_id))
        os.chdir(disable_dir_name + "/" + str(specific_id))
        disable_result_list = process(target_functions, input_functions,    experiment_output)
        disable_list_all.append(disable_result_list)
        os.chdir("../..")
        os.chdir(enable_dir_name + "/" + str(specific_id))
        enable_result_list = process(target_functions, input_functions,experiment_output)
        os.chdir("../..")
        batch_id += 1
        enable_list_all.append(enable_result_list)
        disable_list_all.append(disable_result_list)
        print(sum(enable_result_list[-2]))
        print(sum(disable_result_list[-2]))
        # print(range(len(enable_list_all)))

    for index in range(len(enable_list_all)):
        enable_x_list, enable_y_list = process_data(enable_list_all[index][2])
        disable_x_list, disable_y_list = process_data(disable_list_all[index][2])
        draw_compare_chart(enable_x_list, enable_y_list, disable_x_list, disable_y_list, 0)
    
def target_function_comparation():
    first_folder = sys.argv[1]
    second_folder = sys.argv[2]
    first_files = os.listdir(first_folder)
    second_files = os.listdir(second_folder)

    print(len(first_files))
    print(len(second_files))

    # Ensure both folders have the same number of files
    if len(first_files) != len(second_files):
        print("Warning: The number of files in both folders is not the same.")

    # Iterate through the files
    for file1 in first_files:
        # Construct full file paths
        file1_path = os.path.join(first_folder, file1, "target_functions.txt")
        file2_path = os.path.join(second_folder, file1, "target_functions.txt")

        # Check if both paths are files
        if os.path.isfile(file1_path) and os.path.isfile(file2_path):
            print(file1)
            print(file1)
            with open(file1_path) as f1, open(file2_path) as f2:
                first_content = f1.readlines()
                second_content = f2.readlines()
                print(first_content)
                print(second_content)
                f1.close()
                f2.close()
        else:
            print(f"Skipping {file1_path} or {file2_path} because it is not a file.")



if __name__ == "__main__":
    # main()
    # for id in range(40):
    #     draw_compare_specific_count(id)
    target_function_comparation()