Entrance: syz-manager/manager.go

- manager creation: &Manager
- rpc server started to communicate with Fuzzer: startRPCServer(), listenAndServe()
    - handle connection:
        - handshake( with syz-fuzzer.go): 
            - recv: Connection Request Raw
            - send: Connection Reply
            - recv: InfoRequest Raw
            - send: InfoReply
            - RunCheck()
                - machinechecked()
                    - NewFuzzer(): （注意这里的fuzzer相当于是管理的数据结构，不是虚拟机运行的fuzzer）
                        - create &Fuzzer in Manager
                        - newExecQueues(): register callback function genFuzz(), genFuzz() will generate or mutate the existing test cases or generate new test cases based on current programs and choiceTable
                        genFuzz() may call: mutateProgRequest(), genProgRequest(), which calls fuzzer.ChoiceTable() in  to make choice table, prepare to register the triage process for req. 
                        （镇铎需要看genFuzz中如何生成系统调用的arguments）
                        - **Thread**: choiceTableUpdater()
                            - choiceTableUpdater() listen to Fuzzer.ctRegenerate channel, when the channel is set by fuzzer.ChoiceTable()
            - ConnectionLoop()
- run instances, run fuzzer on instance 
- VMLoop()


Entrance syz-fuzzer/fuzzer.go (照月需要看这个文件，特别是handleConnection中的request如何被执行的代码，弄清在虚拟机上是如何运行系统调用程序的)

- getTarget()

(connection with manager.go)
- send: ConnectionRequest
- recv ConnectionReplyRaw
- send: InfoRequest
- recv: InfoReplyRaw
- create FuzzerTool
- startProc() 
- handleConnection()




