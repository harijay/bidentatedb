#!/usr/bin/python
import subprocess
import Queue
from Queue import Queue
import os
from threading import Thread,Lock
import pdbsumobj
import tempfile
import subprocess


# interaction_dict is a dictionary keyed by pdb_id with PdbSumObj objects
# Each PdbSumUbj has a interactions array which has all the line Strings
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
            apdbsumobj  = self.in_queue.get()
            if apdbsumobj is not None:
                print apdbsumobj.is_valid()
                print apdbsumobj.get_atoms_in_interaction_string()
                self.increment_interactioncount(len(apdbsumobj.interactions))
                t = tempfile.NamedTemporaryFile(dir="/tmp",suffix=".py")
                t.write("""#!/usr/bin/python
cmd.load("/media/default/pdb/data/structures/all/pdb/pdb{pdb_id}.ent.gz", "figobj{pdb_id}")
preset.ligand_cartoon("figobj{pdb_id}")
cmd.select("myasn","resi {asn_resi} and chain {chainid}")
cmd.select("asnlig", "((resn {ligid} and chain {chainid}) within 6.0 of myasn) or myasn")
cmd.zoom("asnlig",3.0)
cmd.save("/media/FreeAgent GoFlex Drive/pdbfigures/{pdb_id}_{ligid}.png")
cmd.delete("figobj{pdb_id}")""".format(pdb_id=apdbsumobj.pdb_id,atomstring=apdbsumobj.get_atoms_in_interaction_string(),ligid=apdbsumobj.interactions[0].split(",")[4],chainid=apdbsumobj.interactions[0].split(",")[6],asn_resi = apdbsumobj.interactions[0].split(",")[0]))
                t.seek(0)
                subprocess.call(["pymol" , "-qc" , t.name])
                out_queue.put(apdbsumobj)
                # This deletes the named temporary file
                t.close()
            if pdbsumobj == None:
                print "TOTAL INTERACTIONS PROCESSED BY THREADS", self.__class__.interactioncount
                break
        
if __name__ == '__main__':
        NUM_THREADS = 5
        in_queue = Queue()
        out_queue = Queue()
        f = open("/home/hari/asn_query/bidentate/bidentate_HBOND_annotated.txt","r")
        old_pdb_id = ""
        current_pdb_sum_obj = None
        for line in f:
            # Extract the pdb_id from the interaction line
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
