#!/usr/bin/python3
# coding=utf8

import sys
import time
import re
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from Uploaders import Uploader
from MUConfig import MagicUploaderConfig
import _thread
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

def get_absolute_path(file_path: str) -> str:
    return os.path.abspath(file_path)


def get_related_path(file_path: str) -> str:
    if not os.path.isabs(file_path):
        print("It's not abs_path!")
        return None
    return file_path[len(os.path.abspath(MagicUploaderConfig.root_path)) + 1:]


def re_check(file_name: str) -> bool:
    for item in MagicUploaderConfig.dont_upload:
        p = re.compile(item)
        if p.search(file_name) is not None:
            return False
    return True


class MagicUploader(Uploader, FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def upload(self, file_from: str, file_to: str):
        absolute_path = get_absolute_path(file_from)
        related_path = get_related_path(get_absolute_path(file_to))
        _thread.start_new_thread(self._upload, (absolute_path, related_path))

    def on_created(self, event):
        absolute_path = get_absolute_path(event.src_path)
        related_path = get_related_path(absolute_path)
        print("[Created] : %s " % absolute_path)
        if not re_check(event.src_path):
            print("[CHECK]   : Ignore file [%s]" % absolute_path)
            return
        if event.is_directory:
            print("[CHECK]   : Directory Dont Upload")
            return
        _thread.start_new_thread(self._upload, (absolute_path, related_path))

    def on_deleted(self,  event):
        absolute_path = get_absolute_path(event.src_path)
        related_path = get_related_path(absolute_path)
        print("[Deleted] : %s" % absolute_path)
        if not re_check(absolute_path):
            print("[CHECK]   : Ignore File [%s]" % absolute_path)
            return
        if event.is_directory:
            print("[CHECK]   : Directory Dont Upload")
            return
        # Do not delete now
        return
        # info = self._remove(event.src_path)
        # print (info)

    def on_moved(self ,event):
        pass
        #print ("Move From %s to %s"%(event.src_path[2:],event.dest_path[2:]))

    def on_modified(handler, event):
        pass
        #print ("[Modified] : %s"%event.src_path[2:])



def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # 重定向标准文件描述符（默认情况下定向到/dev/null）
    try:
        pid = os.fork()
        # 父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。
        if pid > 0:
            sys.exit(0)  # 父进程退出
    except OSError as e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

        # 从母体环境脱离
    os.chdir("/")  # chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录
    os.umask(0)  # 调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。
    os.setsid()  # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。

    # 执行第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # 第二个父进程退出
    except OSError as e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

        # 进程已经是守护进程了，重定向标准文件描述符

    for f in sys.stdout, sys.stderr: f.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())  # dup2函数原子化关闭和复制文件描述符
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


class RequestHandler(SimpleXMLRPCRequestHandler):
    # Add these headers to all responses
    def end_headers(self):
        self.send_header("Access-Control-Allow-Headers",
                         "Origin, X-Requested-With, Content-Type, Accept")
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleXMLRPCRequestHandler.end_headers(self)


def start_xml_rpc(ip: str, port: int, instance: MagicUploader):
    server = SimpleXMLRPCServer((ip, port), allow_none=True, requestHandler=RequestHandler)
    server.register_function(instance.list_files)
    print("RPC Started")
    server.serve_forever()


def start_watchdog(wg: MagicUploader):
    observer = Observer()
    observer.schedule(wg, os.path.abspath(MagicUploaderConfig.root_path), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



if __name__ == '__main__':
    if len(sys.argv) == 3:
        if (sys.argv[2] == "-d") or (sys.argv[2] == "--deamon"):
            daemonize()
    event_handler = MagicUploader()
    event_handler._set_do_upload(True)
    event_handler._set_show_process(True)
    event_handler._init_qiniu()
    _thread.start_new_thread(start_xml_rpc,("",8080,event_handler))
    start_watchdog(event_handler)
