#!/usr/bin/python
import subprocess
import Queue
from Queue import Queue
import os
import pymol
from threading import Thread,Lock
import pdbsumobj

interaction_dict = {}

class PymolThread(Thread):
    interactioncount = 0
    mutex = Lock()
    def __init__(self,in_queue,out_queue):
        Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
    def increment_interactioncount(self,number):
        self.mutex.acquire()
        self.__class__.interactioncount = self.__class__.interactioncount + int(number)
        self.mutex.release()

    def run(self):
        while True:
            pdbsumobj  = self.in_queue.get()
            if pdbsumobj is not None:
                print pdbsumobj.is_valid()
                self.increment_interactioncount(len(pdbsumobj.interactions))
                out_queue.put(pdbsumobj)
            if pdbsumobj == None:
                print "TOTAL INTERACTIONS PROCESSED BY THREADS", self.__class__.interactioncount
                break
        
if __name__ == '__main__':
        NUM_THREADS = 3
        in_queue = Queue()
        out_queue = Queue()
        f = open("/home/hari/asn_query/bidentate/bidentate_HBOND_annotated.txt","r")
        old_pdb_id = ""
        current_pdb_sum_obj = None
        for line in f:
            pdb_id = line.split(",")[-1].split("_")[0].lower()
            if pdb_id in interaction_dict.keys():
                interaction_dict[pdb_id].append_interaction(line)
            else:
                current_pdb_sum_obj = pdbsumobj.PdbSumObj(line)
                interaction_dict[pdb_id] = current_pdb_sum_obj
        for akey in interaction_dict.keys():        
        	in_queue.put(interaction_dict[akey])    
        print "TOTAL INTERACTION PDBS" , len(interaction_dict.keys())
        
        for i in range(NUM_THREADS):
            in_queue.put(None)     

    
        worker_thread_list = []

        for i in range(NUM_THREADS):
            w = PymolThread(in_queue,out_queue)
            w.start()
            worker_thread_list.append(w)
