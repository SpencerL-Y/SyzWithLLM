import os
import sys

project_root = "/home/clexma/Desktop/fox3/fuzzing/"

def clear_old_files():
    # cg_file = "./ChatAnalyzer/callgraphFile.txt"
    # os.system("rm " + cg_file + " " + path_file)
    path_file = "./ChatAnalyzer/pathsFile.txt"
    path_source_code_file = "./ChatAnalyzer/path_source_code.txt"
    syz_comm_content = "./ChatAnalyzer/syz_comm_content.txt"
    syz_comm_sig = "./ChatAnalyzer/syz_comm_sig.txt"
    close_function_file = "./linuxRepo/line2addr/input_functions.txt"
    func2addr_info_file = "./linuxRepo/line2addr/func2addr_info.txt"
    result_addr_info_file = "./linuxRepo/line2addr/result_addr_info.txt"
    cov_raw_folder = "./syzkaller/cov_fodler_vm*"
    close_function_file = "./linuxRepo/line2addr/input_functions.txt"
    os.truncate(path_source_code_file, 0)
    os.truncate(path_file, 0)
    os.truncate(syz_comm_content, 0)
    os.truncate(syz_comm_sig, 0)
    os.truncate(close_function_file, 0)
    os.truncate(func2addr_info_file, 0)
    os.truncate(result_addr_info_file, 0)
    os.truncate(close_function_file, 0)
    os.system("rm -rf " + cov_raw_folder)

if __name__ == "__main__":
    if "copy" in sys.argv[1]:
        target_functions_file_name = "./target_functions.txt"
        path_file = "./ChatAnalyzer/pathsFile.txt"
        path_source_code_file = "./ChatAnalyzer/path_source_code.txt"
        syz_comm_content = "./ChatAnalyzer/syz_comm_content.txt"
        syz_comm_sig = "./ChatAnalyzer/syz_comm_sig.txt"
        close_function_file = "./linuxRepo/line2addr/input_functions.txt"
        close_cov_result_file = "./syzkaller/close_cov_result.txt"
        func2addr_info_file = "./linuxRepo/line2addr/func2addr_info.txt"
        result_addr_info_file = "./linuxRepo/line2addr/result_addr_info.txt"
        cov_raw_folder = "./syzkaller/cov_fodler_vm*"
        print("cp -rf" + path_file + " " + path_source_code_file + " " + target_functions_file_name + " " + syz_comm_content + " " + syz_comm_sig + " " + close_function_file + " " + func2addr_info_file + " " + result_addr_info_file + " " + cov_raw_folder + "  ./experiment_result")
        os.system("cp -rf " + path_file + " " + path_source_code_file + " " + syz_comm_content + " " + syz_comm_sig + " " + close_function_file + " " + func2addr_info_file + " " + result_addr_info_file + " "  + "  ./experiment_result")
        print("cp -rf " + cov_raw_folder + "  ./experiment_result")
        os.system("cp -rf " + cov_raw_folder + "  ./experiment_result")
        print("cp ./syzkaller/experiment_output_llmenabled.txt ./experiment_result")
        os.system("cp ./syzkaller/experiment_output_llmenabled.txt ./experiment_result")
    elif "run" in sys.argv[1]:
        llm_enabled_str = sys.argv[2]
        llm_enabled = False
        if "1" in llm_enabled_str:
            llm_enabled = True 
        # pass
        clear_old_files()
        target_functions_file_name = "./target_functions.txt"
        target_functions_file = open(target_functions_file_name, "r")
        if llm_enabled:
            os.chdir("./ChatAnalyzer")
            # obtain the path of function and the corresponding path of function body and store it into the files in ChatAnalyzer
            for line in target_functions_file.readlines():
                function_name = line.strip().replace("\n", "")
                print("python3 chat_interface.py init " + function_name)
                os.system("python3 chat_interface.py init " + function_name)
            target_functions_file.seek(0)
        else:
            os.chdir("./ChatAnalyzer")
        for line in target_functions_file.readlines():
            function_name = line.strip().replace("\n", "")
            print("python3 chat_interface.py close " + function_name + " 2")
            os.system("python3 chat_interface.py close " + function_name + " 2")
        target_functions_file.close()
        os.chdir("../linuxRepo/line2addr")
        print(os.getcwd())
        print("python3 ./addr_extractor.py ./input_functions.txt")
        os.system("python3 ./addr_extractor.py ./input_functions.txt")
        os.chdir(project_root + "syzkaller")
        os.system("python3 clean.py")
        os.system("sudo ./bin/syz-manager  -config ./my.cfg >> experiment_output_llmenabled.txt 2>&1")