# -*- coding:UTF-8 -*-
import os
import git
import multiprocessing
import signal
import time
# Constants
url_base_1 = "https://www.github.com/"
url_base_2 = ".git"


def get_size_in_kb(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size/1024


def clone(i):
    git.Repo.clone_from(url, "./projects/%s" % (i))


def handler(signum, frame):
    raise Exception("Jumped...")


if __name__ == '__main__':
    file = open(r'repo_lists.txt', 'r')
    read_file = file.read()
    read_file_spit = read_file.split(',')
    count = 0
    signal.signal(signal.SIGALRM, handler)
    for i in read_file_spit:
        try:
            record0 = open(r'02project_name.txt', 'a')
            record1 = open(r'02project_size.txt', 'a')
            record2 = open(r'name+size.txt', 'a')
            record3 = open(r'02FILES_NEED_TO_DELET.txt', 'a')
            url = url_base_1 + i + url_base_2
            i=i.replace("/", "_")
            signal.alarm(30)
            try:
                clone(i)
                print(time.clock(), "GIT-CLONED:%s" % (i), count)
                record0.write(i)
                record0.write("\n")
            except Exception as exc:
                print (exc)
                record3.write(i)
                record3.write("\n")
                continue
            try:
                size = str(get_size_in_kb("./projects/%s" % (i)))
                print (size)
                record1.write(size)
                record1.write("\n")
                count = count + 1
                record2.write(i)
                record2.write("\n")
                record2.write(size)
                record2.write("\n")
                record0.close()
                record1.close()
                record2.close()
            except Exception:
                record3.write(i)
                record3.write("\n")
                continue
        except git.exc.GitCommandError:
            pass
