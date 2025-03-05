# SyzAgent

SyzAgent is a directed fuzzing project that implemented upon Google's kernel fuzzer Syzkaller. The idea is using static analysis and LLM to guide the initial generation of test cases and guide the adjustment of test cases generation during the fuzzing procedure, in order to fuzz to specific function in the kernel.

## Platform Requirement

Ubuntu host, QEMU vm, x86-64 kernel and the same environment requirement imposed by [Syzkaller](https://github.com/google/syzkaller/).

## Hierarchy
The folder hierarchy is shown below:

```
SyzAgent/ 
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

When `create-image.sh` is finished, the `bullseyes.img` file will be generated at `/SyzWithLLM/imageDir/`.

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
```

When `Compilation.py` is finished, `vmlinux` will be generated at `/SyzWithLLM/linuxRepo/llvm_kernel_analysis/bc_dir/` and `bzImage` will be generated at `/SyzWithLLM/linuxRepo/llvm_kernel_analysis/bc_dir/arch/x86/boot/`.

```
cd ./Analyzer
mkdir build
cd ./build
cmake ../src
make 
cd ../../../
```

Note that the root path and folder path used in ```Compilation.py``` and ```project_root``` in ```Analyzer.cpp``` need to be configured accordingly.

### Configuring Syzkaller

We refer the configuring of Syzkaller to [HERE](https://github.com/SpencerL-Y/SyzLLM/blob/master/docs/linux/setup_ubuntu-host_qemu-vm_x86-64-kernel.md) and [HERE](https://github.com/SpencerL-Y/SyzLLM/blob/master/docs/linux/setup.md).

And the following steps of configuring Syzkaller are for your reference.

Before configuring Syzkaller, you should install qemu first, and verify if kernel boot and sshd start. If it succeeds, you are prompted to enter root to log in. Otherwise, something may have gone wrong in one of the previous steps.
```
apt install qemu-system-x86 
qemu-system-x86_64 \
	-m 2G \
	-smp 2 \
	-kernel $KERNEL/arch/x86/boot/bzImage \   
	-append "console=ttyS0 root=/dev/sda earlyprintk=serial net.ifnames=0" \
	-drive file=$IMAGE/bullseye.img,format=raw \   
	-net user,host=10.0.2.10,hostfwd=tcp:127.0.0.1:10021-:22 \
	-net nic,model=e1000 \
	-enable-kvm \
	-nographic \
	-pidfile vm.pid \
	2>&1 | tee vm.log
```

Now we can configure Syzkaller and it should be in the `SyzWithLLM/` directory.
 ```
cd syzkaller
 ```
Create a syz-manager configuration file `my.cfg` with the following contents (the path where SyzWithLLM is located needs to be relpaced with the actual path) and palce the file in the `SyzWithLLM/syzkaller/` directory.
```
{
    "target": "linux/amd64",
    "http": "127.0.0.1:56741",
    "workdir": "/home/ubuntu/SyzWithLLM/syzkaller/workdir",
    "kernel_obj": "/home/ubuntu/SyzWithLLM/linuxRepo/llvm_kernel_analysis/bc_dir",
    "image": "/home/ubuntu/SyzWithLLM/imageDir/bullseye.img",
    "sshkey": "/home/ubuntu/SyzWithLLM/imageDir/bullseye.id_rsa",
    "syzkaller": "/home/ubuntu/SyzWithLLM/syzkaller",
    "procs": 8,
    "type": "qemu",
    "vm": {
        "count": 4,
        "kernel": "/home/ubuntu/SyzWithLLM/linuxRepo/llvm_kernel_analysis/bc_dir/arch/x86/boot/bzImage",
        "cpu": 2,
        "mem": 2048
    }
}
```
Run Syzkaller and check if you configure it successfully.
```
mkdir workdir
./bin/syz-manager -config=my.cfg
```

## Run experiment

There are several absolute paths in our source code, before running the experiment, please follow the following tips to modify these paths into your actual path to avoid running errors. 

Here we take `SyzWithLLM/ChatAnalyzer/chat_interface.py, line 5 and line 7` as example, and you can modify them into the following lines. The `prefix path` represents where `SyzWithLLM` is in.

```
sys.path.insert(0, os.path.abspath('prefix path + /SyzWithLLM/ChatAnalyzer'))
project_root = "prefix path + /SyzWithLLM/"
```

The files containing absolute paths are as follows:

```
SyzWithLLM/ChatAnalyzer/chat_interface.py, line 5 and line 7.
SyzWithLLM/ChatAnalyzer/chat_interface_mannual.py, line 5 and line 6.
SyzWithLLM/ChatAnalyzer/extract_func_body.py, line 5.
SyzWithLLM/ChatAnalyzer/extract_function_callpaths.py, line 5 and line 8.
SyzWithLLM/ChatAnalyzer/mutation_prompt.py, line 3.
SyzWithLLM/linuxRepo/line2addr/addr_extractor.py, line 8.
SyzWithLLM/run_experiment.py, line 7.
```

Now you can run the experiment using the following instruction.

```
python3 ./run_batch_experiment [1/0] [close_distance]
```

```[1/0]``` represents that whether the LLM is enabled or not
```[close_distance]``` is a number >= 1 used to denote the close distance.


## Publication

Paper of FASE 2025 is [HERE](https://arxiv.org/abs/2503.02301)
