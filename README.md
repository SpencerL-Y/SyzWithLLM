# LLMGuidedSyzkaller

SyzWithLLM is a directed fuzzing project that implemented upon Google's kernel fuzzer Syzkaller. The idea is using static analysis and LLM to guide the initial generation of test cases and guide the adjustment of test cases generation during the fuzzing procedure, in order to fuzz to specific function in the kernel.

## Platform Requirement

Ubuntu host, QEMU vm, x86-64 kernel and the same environment requirement imposed by [Syzkaller](https://github.com/google/syzkaller/).

## Hierarchy
The folder hierarchy is shown below:

```
LLMGuidedSyzkaller/ 
    ├── ChatAnalyzer/   # LLM interface and static analyzer  interface
    |        ├── syz_comm_content.txt
    |        ├── syz_comm_sig.txt
    |        ├── target_syscalls.txt
    |        ├── callgraphFile.txt
    |        ├── disabled_calls.txt
    |        ├── enabled_calls.txt
    |        ├── close_cov_prog_source_code.txt
    |        ├── path_source_code.txt
    |        ├── pathFile.txt
    |        └── ...
    ├── experiment_result/ 
    ├── go/             # go binary folder
    ├── imageDir/       # image dir for linux kernel
    |        ├── create_image.sh
    |        └── ...
    ├── linuxRepo/      # linux repositoryies, tags, and line2addr
    |        ├── line2addr/ 
    |        ├── linux_new/ 
    |        ├── llvm_kernel_analysis/ 
    |        ├── .ctags
    |        └── tags
    ├── syzkaller/      # our modified syzkaller └──
    ├── total_result_FASE/ # experimental results used in the paper
    ├── target_functions.txt        # target functions being processed
    ├── target_functions_list.txt   # list of target functions
```

## Configuring the Environment

All scripts below are executed at the root of the project.
###  Clone ChatAnalyzer

```
git clone git@github.com:SpencerL-Y/ChatAnalyzer.git
```

### install ```Go```

Syzkaller is implemented in Golang. We use following script to install go binary. 

```
wget https://dl.google.com/go/go1.22.1.linux-amd64.tar.gz
tar -xf go1.22.1.linux-amd64.tar.gz
export GOROOT=`pwd`/go
export PATH=$GOROOT/bin:$PATH
```

### clone modifed Syzkaller
```
clone git@github.com:SpencerL-Y/SyzLLM.git
mv SyzLLM syzkaller
cd syzkaller
make
cd ..
```

### construct ```imageDir```

```
mkdir imageDir
cp ./syzkaller/tools/create-image.sh ./imageDir/
cd imageDir
./create-image.sh
cd ..
```

### construct ```linuxRepo``` folder
```
cd linuxRepo
git@github.com:torvalds/linux.git
mv linux linux_new
git@github.com:SpencerL-Y/line2addr_kernel.git
ctags -R  --options=.ctags  linux_new
mv line2addr_kernel line2addr
git@github.com:SpencerL-Y/llvm_kernel_analysis.git
cd ./llvm_kernel_analysis/
mkdir bc_dir
python3 Compilation.py fuzzing
cd ./Analyzer
mkdir build
cd ./build
cmake ../src
make cd ../../../
```

Note that the root path and folder path used in ```Compilation.py``` and ```project_root``` in ```Analyzer.cpp``` need to be configured accordingly.

### Configuring Syzkaller

We refer the configuring of Syzkaller to [HERE](https://github.com/SpencerL-Y/SyzLLM/blob/master/docs/linux/setup_ubuntu-host_qemu-vm_x86-64-kernel.md) and [HERE](https://github.com/SpencerL-Y/SyzLLM/blob/master/docs/linux/setup.md).




## Run experiment

```
python3 ./run_batch_experiment [1/0] [close_distance]
```

```[1/0]``` represents that whether the LLM is enabled or not
```[close_distance]``` is a number >= 1 used to denote the close distance.




