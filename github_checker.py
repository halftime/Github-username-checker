#!/usr/bin/env python3

import requests
import threading
import queue
import sys
import time
import argparse

class github_checker:
    def __init__(self, threadcount, wordlist):
        self.http_fail_sleep = 30
        self.http_timeout = 3
        self.lock = threading.Lock()
        self.threads_wait = threading.Event()
        self.queue = queue.Queue(maxsize=1000)
        self.out_file = open("git-user-404s.txt", "a")
        self.start_threads(threadcount)
        self.load_wordlist(wordlist)
        self.queue.join()
        self.out_file.close()
        sys.stderr.write("Done!\n")

    def thread_worker(self,):
        while True:
            while self.threads_wait.isSet():
                time.sleep(1)
            try:
                s = self.queue.get(timeout=30)
            except queue.Empty:
                break
            try:
                r = requests.get("https://github.com/{0}".format(s), timeout=self.http_timeout)
            except:
                if not self.threads_wait.isSet():
                    self.threads_wait.set()
                    sys.stderr.write("HTTP-request failed, will sleep for {0}s\n".format(self.http_fail_sleep))
                    time.sleep(self.http_fail_sleep)
                    self.threads_wait.clear()
                    sys.stderr.write("Sleep done, restarting\n")
                continue
            
            self.queue.task_done()
            if r.status_code == 404:
                with self.lock:
                    sys.stderr.write("Possible untaken github:\t{0}\n".format(s))
                    self.out_file.write(s + "\n")
                    self.out_file.flush()
            else:
                with self.lock:
                    sys.stderr.write("Already taken github:\t{0}\n".format(s))


    def start_threads(self, threadcount):
        for i in range(threadcount):
            t = threading.Thread(target=self.thread_worker)
            t.deamon = True
            t.start()

    def load_wordlist(self, wordlist):
        for line in open(wordlist, "r"):
            try:
                line = line.replace("\n", "").lower()
            except:
                continue
            self.queue.put(line)

parser = argparse.ArgumentParser(description="Find 404'd (untaken) github profiles")
parser.add_argument("wordlist", type=str, help="Wordlist to read usernames from (wordlist.txt)")
parser.add_argument("threads", type=int, help="Amount of threads (24)")
args = parser.parse_args()

sys.stderr.write("Starting search for untaken github usernames!\n")
sys.stderr.write("Threads:\t{0}\n".format(args.threads))
sys.stderr.write("Wordlist:\t{0}\n".format(args.wordlist))
git = github_checker(args.threads, args.wordlist)
