import re
import os
import matplotlib.pyplot as plt
import csv


target_functions = 'target_functions.txt'
input_functions = 'input_functions.txt'
experiment_output = 'experiment_output_llmenabled.txt'
latex_table = 'latex_table.txt'
syscall_func_steps_sorted = 'syscall_func_steps_sorted.txt'
output = 'result.txt'

list_all = []

def extract_functions(file):
    if os.path.exists(file):
        with open(file, 'r') as file:
            functions = [line.strip() for line in file.readlines()]
        return functions
    return None

# abolished
def extract_sample_count(file):
    hit_times_list = []
    sample_count_list = []
    unreached_pattern = re.compile(r'\d{4}/\d{2}/\d{2}.* candidates=\d+ corpus=\d+ coverage=\d+ exec total=\d+')
    reached_pattern  = re.compile(r'\d{4}/\d{2}/\d{2}.* XXXXX REACH')
    hit_times_pattern = re.compile(r'Hit times:\s*(\d+)')
    with open(file, 'r') as file:
        hit_times_count = 0
        sample_count = 0
        for line in file:
            if unreached_pattern.match(line) or reached_pattern.match(line):
                sample_count += 1
            hit_match = hit_times_pattern.search(line)
            if hit_match:
                hit_times_count = int(hit_match.group(1))
                hit_times_list.append(hit_times_count)
                sample_count_list.append(sample_count)
                sample_count = 0
    return sample_count_list, hit_times_list
# abolished
def draw_sample_hittimes_chart(sample_list, hittimes_list, id):
    plt.figure()
    plt.plot(sample_list, hittimes_list, marker = 'o', linestyle = 'None', color = 'b')
    plt.xlabel('sample count')
    plt.ylabel('hit times')
    plt.savefig('sample_hittimes_chart' + str(id) + '.svg')
    plt.clf()
    return 

def extract_experiment_data(file):
    all_coverage_exec = []
    all_hit_times = []
    coverage_exec_list = []
    error_1 = []
    error_2 = []
    coverage_exec_pattern = re.compile(r'coverage=(\d+) exec total=(\d+)')
    hit_times_pattern = re.compile(r'Hit times: (\d+)')
    error_1_pattern = re.compile(r'close ask Output: ```plaintext')
    error_2_pattern = re.compile(r'This model\'s maximum context length')
    error_1_count = -1
    error_2_count = -1
    if os.path.exists(file):
        with open(file, 'r') as file:
            for line in file:
                coverage_exec = coverage_exec_pattern.search(line)
                if coverage_exec:
                    coverage = int(coverage_exec.group(1))
                    exec = int(coverage_exec.group(2))
                    coverage_exec_list.append((coverage,exec))
                hit_times_match = hit_times_pattern.search(line)
                if hit_times_match:
                    hit_times = int(hit_times_match.group(1))
                    all_hit_times.append(hit_times)
                    all_coverage_exec.append(coverage_exec_list)
                    coverage_exec_list = []
                error_1_match = error_1_pattern.search(line)
                if error_1_match:
                    error_1.append(error_1_match)
                error_1_count = len(error_1)
                error_2_match = error_2_pattern.search(line)
                if error_2_match:
                    error_2.append(error_2_match)
                error_2_count = len(error_2)
            all_coverage_exec.append(coverage_exec_list)
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

def process_data(lists):
    cov_list = []
    exec_list = []
    if len(lists) > 0:
        for list in lists:
            for cov, exec in list:
                cov_list.append(cov)
                cov_list.append(cov)
                exec_list.append(exec)
                exec_list.append(exec)
        cov_list.pop(-1)
        exec_list.pop(0)
    return exec_list, cov_list

def draw_id_hittimes_chart(enable_x_list_1, enable_y_list_1, enable_x_list_2, enable_y_list_2, enable_x_list_3, enable_y_list_3, disable_x_list_1, disable_y_list_1, disable_x_list_2, disable_y_list_2, disable_x_list_3, disable_y_list_3, id):
    plt.figure()
    plt.plot(enable_x_list_1, enable_y_list_1, color='blue')
    plt.plot(enable_x_list_2, enable_y_list_2, color='blue')
    plt.plot(enable_x_list_3, enable_y_list_3, color='blue')
    plt.plot(disable_x_list_1, disable_y_list_1, color='red')
    plt.plot(disable_x_list_2, disable_y_list_2, color='red')
    plt.plot(disable_x_list_3, disable_y_list_3, color='red')
    plt.xlabel('id')
    plt.ylabel('hit times')
    plt.show()
    plt.savefig('./feedback_images/feedback' + str(id) + '.svg')
    plt.clf()

def draw_compare_chart(enable_x_list, enable_y_list, disable_x_list, disable_y_list, count):
    plt.figure()
    plt.plot(enable_x_list, enable_y_list, color='blue')
    plt.plot(disable_x_list, disable_y_list, color='red')
    plt.xlabel('coverage')
    plt.ylabel('exec num')
    plt.title('Compare')
    plt.show()
    plt.savefig('image' + str(count) + '.svg')
    plt.clf()

def draw_compare_chart2(enable_x_list_1, enable_y_list_1, enable_x_list_2, enable_y_list_2, enable_x_list_3, enable_y_list_3, disable_x_list_1, disable_y_list_1, disable_x_list_2, disable_y_list_2, disable_x_list_3, disable_y_list_3, count):
    plt.figure()
    plt.plot(enable_x_list_1, enable_y_list_1, color='blue')
    plt.plot(enable_x_list_2, enable_y_list_2, color='blue')
    plt.plot(enable_x_list_3, enable_y_list_3, color='blue')
    plt.plot(disable_x_list_1, disable_y_list_1, color='red')
    plt.plot(disable_x_list_2, disable_y_list_2, color='red')
    plt.plot(disable_x_list_3, disable_y_list_3, color='red')
    plt.xlabel('exec num')
    plt.ylabel('coverage')
    plt.show()
    plt.savefig('./images_result/image' + str(count) + '.svg')
    plt.clf()


def draw_compare_specific_count(specific_id):
    disable_list_all = []
    enable_list_all = []
    batch_id_bound = 3
    batch_id = 1
    while batch_id <= batch_id_bound:
        disable_dir_name = "./disable_batch_" + str(batch_id)
        enable_dir_name = "./enable_batch_" + str(batch_id)
        if not os.path.isdir(disable_dir_name + "/" + str(specific_id)) or not os.path.isdir(enable_dir_name + "/" + str(specific_id)):
            batch_id += 1
            continue

        # print("curr id = " + str(specific_id))
        os.chdir(disable_dir_name + "/" + str(specific_id))
        disable_result_list = process(target_functions, input_functions, experiment_output)
        # disable_list_all.append(disable_result_list)
        os.chdir("../..")
        os.chdir(enable_dir_name + "/" + str(specific_id))
        enable_result_list = process(target_functions, input_functions, experiment_output)
        os.chdir("../..")
        batch_id += 1
        enable_list_all.append(enable_result_list)
        disable_list_all.append(disable_result_list)

    for index in range(len(enable_list_all) - 2):
        enable_x_list_1, enable_y_list_1 = process_data(enable_list_all[index][2])
        enable_x_list_2, enable_y_list_2 = process_data(enable_list_all[index+1][2])
        enable_x_list_3, enable_y_list_3 = process_data(enable_list_all[index+2][2])
        disable_x_list_1, disable_y_list_1 = process_data(disable_list_all[index][2])
        disable_x_list_2, disable_y_list_2 = process_data(disable_list_all[index+1][2])
        disable_x_list_3, disable_y_list_3 = process_data(disable_list_all[index+2][2])
        draw_compare_chart2(enable_x_list_1, enable_y_list_1, enable_x_list_2, enable_y_list_2, enable_x_list_3, enable_y_list_3, disable_x_list_1, disable_y_list_1, disable_x_list_2, disable_y_list_2, disable_x_list_3, disable_y_list_3, specific_id)


def extract_distance(target_function):
    # print(target_function)
    with open(syscall_func_steps_sorted, 'r') as file:
        for line in file:
            sys_tar_dis = line.strip().split(', ')
            sys, tar, dis = sys_tar_dis
            if tar == target_function:
                # print(dis)
                return int(dis)
    return -1

def compute_hittimes_rate(hittimes_list):
    list = []
    rate = -1
    list.append(hittimes_list)
    list.append(sum(hittimes_list))
    list.append(len(hittimes_list))
    if len(hittimes_list) != 0:
        rate = float(sum(hittimes_list))/(len(hittimes_list)*500)
    list.append(process_decimal(rate))
    return list

def hittimes_rate(specific_id):
    enable_hittimes_list = []
    disable_hittimes_list = []
    temp_list1 = []
    temp_list2 = []
    return_list = []
    batch_id_bound = 3
    batch_id = 1
    while batch_id <= batch_id_bound:
        disable_dir_name = "./disable_batch_" + str(batch_id)
        enable_dir_name = "./enable_batch_" + str(batch_id)
        if not os.path.isdir(disable_dir_name + "/" + str(specific_id)) or not os.path.isdir(enable_dir_name + "/" + str(specific_id)):
            batch_id += 1
            continue
        os.chdir(disable_dir_name + "/" + str(specific_id))
        disable_result_list = process(target_functions, input_functions, experiment_output)
        disable_hittimes_list = disable_result_list[-2]
        os.chdir("../..")
        os.chdir(enable_dir_name + "/" + str(specific_id))
        enable_result_list = process(target_functions, input_functions, experiment_output)
        enable_hittimes_list = enable_result_list[-2]
        os.chdir("../..")

        temp_list1 = compute_hittimes_rate(disable_hittimes_list)
        temp_list1.append(disable_result_list[0][0])
        distance1 = extract_distance(disable_result_list[0][0])
        temp_list1.append(distance1)
        return_list.append(temp_list1)
        temp_list1 = []


        temp_list2 = compute_hittimes_rate(enable_hittimes_list)
        temp_list2.append(enable_result_list[0][0])
        distance2 = extract_distance(enable_result_list[0][0])
        temp_list2.append(distance2)
        return_list.append(temp_list2)
        temp_list2 = []
        batch_id += 1
    return return_list

def process_decimal(number):
    result = round(number * 100, 2)
    return result

def process_decimal_2(number):
    result = round(number, 2)
    return result

def compute_avg(total_list):
    enable_avg = -1
    disable_avg = -1
    difference = -1
    for i, result in enumerate(total_list):
        if len(result) >= 6:
            disable_1, enable_1, disable_2, enable_2, disable_3, enable_3 = result
            enable_avg = (enable_1[3] + enable_2[3] + enable_3[3]) / 3
            disable_avg = (disable_1[3] + disable_2[3] + disable_3[3]) / 3
            difference = enable_avg - disable_avg
            total_list[i].append(process_decimal_2(enable_avg))
            total_list[i].append(process_decimal_2(disable_avg))
            total_list[i].append(process_decimal_2(difference))
    return total_list

def export_to_csv(total_list):

    output_file = 'total_list_output.csv'

    list = compute_avg(total_list)

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        header = ['n', 'target function1','target function2','target function3','target function4','target function5','target function6', 'distance', 
        'enable_1_sum', 'enable_1_len', 'enable_1_rate',
        'enable_2_sum', 'enable_2_len', 'enable_2_rate',
        'enable_3_sum', 'enable_3_len', 'enable_3_rate',
        'disable_1_sum', 'disable_1_len', 'disable_1_rate',
        'disable_2_sum', 'disable_2_len', 'disable_2_rate',
        'disable_3_sum', 'disable_3_len', 'disable_3_rate',
        'enable_avg', 'disable_avg', 'difference'
        ]
        writer.writerow(header)
        
        for i, result in enumerate(list):
            if len(result) >= 9:
                disable_1, enable_1, disable_2, enable_2, disable_3, enable_3, enable_avg, disable_avg, difference = result

                row = [i, enable_1[4], enable_2[4], enable_3[4], disable_1[4], disable_2[4], disable_3[4], disable_1[5],
                    enable_1[1], enable_1[2], enable_1[3], 
                    enable_2[1], enable_2[2], enable_2[3],
                    enable_3[1], enable_3[2], enable_3[3],
                    disable_1[1], disable_1[2], disable_1[3], 
                    disable_2[1], disable_2[2], disable_2[3], 
                    disable_3[1], disable_3[2], disable_3[3],
                    enable_avg, disable_avg, difference
                    ] 

                writer.writerow(row)
    # print(f"Data has been successfully written to {output_file}")

def generate_latex(list):
    with open(latex_table, 'w') as output:
        output.write('\\begin{table}[h!]\n')
        output.write('\\centering\n')
        output.write('\\begin{tabular}{|c|l|c|ccc|ccc|c|}\n')
        output.write('\\hline\n')
        output.write('\\multirow{2}{*}{ID} & \\multirow{2}{*}{Target Function} & \\multirow{2}{*}{Dist.} & \\multicolumn{3}{c|}{\\toolname Hit \\%} & \\multicolumn{3}{c|}{Syzkaller Hit \\%} & \\multirow{2}{*}{Avg. Diff}\\\\ \\cline{4-9}\n')
        output.write('  &    &                   & Run 1 & Run 2 & Run 3 & Run 1 & Run 2 & Run 3 &\\\\ \\hline\n')
        for i, row in enumerate(list):
            if len(row) >= 9:
                disable_1, enable_1, disable_2, enable_2, disable_3, enable_3, enable_avg, disable_avg, difference = row
                output.write(f"{i} & {disable_1[4]} & {disable_1[5]} & ")
                output.write(f"{enable_1[3]} & {enable_2[3]} & {enable_3[3]} & ")
                output.write(f"{disable_1[3]} & {disable_2[3]} & {disable_3[3]} & ")
                output.write(f"{difference} \\\\\n")

        output.write('\\hline\n')
        output.write('\\end{tabular}\n')
        output.write('\\vspace{3pt}\n')
        output.write('\\caption{Experimental Data Comparison between Two Methods }\n')
        output.write('(``Dist.'' denotes the minimum length of call path from some system call to target function. ``Hit \\%'' represents the ratio of the test cases that covered close area in the sampled test cases in percentage. ``Avg. Diff'' denotes the average difference of the hit rate of \\toolname  minus the hit rate of Syzkaller across all runs.)\n')
        output.write('\\label{tab:exp_table}\n')
        output.write('\\vspace{-20pt}\n')
        output.write('\\end{table}\n')


if __name__ == "__main__":
    
    # total results
    total_list = []
    for id in range(0, 41):
        total_list.append(hittimes_rate(id))
        draw_compare_specific_count(id)
    export_to_csv(total_list)
    generate_latex(total_list)
    
    
    # draw hit times charts
    for id in range(0, 41):
        list = hittimes_rate(id)
        if len(list) >= 6:
            # print(list[1]) # enable_1
            # enable 123 -> 135; disable 123 -> 024
            draw_id_hittimes_chart(range(1, list[1][2]+1), list[1][0], range(1, list[3][2]+1), list[3][0], range(1, list[5][2]+1), list[5][0], range(1, list[0][2]+1), list[0][0], range(1, list[2][2]+1), list[2][0], range(1,list[4][2]+1), list[4][0], id)
    
    
    