#!/usr/bin/python
# Loop through all the files in the bidentate directory
import os
import sys
import pymol
import time
pymol.finish_launching()

#print "/media/default/pdb/data/biounit/coordinates/divided/{adir}/{pdb_id}.pdb1.gz".format(adir = pdbdir,pdb_id=pdb_id)
#pymol.cmd.load("/media/default/pdb/data/biounit/coordinates/divided/{adir}/{pdb_id}.pdb1.gz".format(adir = pdbdir,pdb_id=pdb_id)) 

old_pdb_id = ""
 
if __name__ == '__main__':
    f = open("/home/hari/asn_query/bidentate/bidentate_HBOND_annotated.txt","r")
    # f = open("temp.txt","r")
    for line in f:
        pdb_id = line.split(",")[-1].split("_")[0].lower()
        print pdb_id
        if old_pdb_id != pdb_id:
            pdbdir = pdb_id[1:3]
            print pdbdir
            pymol.cmd.load("/media/default/pdb/data/biounit/coordinates/divided/{adir}/{pdb_id}.pdb1.gz".format(adir = pdbdir,pdb_id=pdb_id))
            line_split = line.split(",")
            ligid = line_split[4]
            res1,lig1 = line_split[1],line_split[3]
            newline = f.next()
            line_split2 = newline.split(",")
            res2,lig2 = line_split2[1],line_split2[3]
            print res1,res2,lig1,lig2
            pymol.cmd.select("id {res1} or id {lig1} or id {res2} or id {lig2}".format(res1 = res1 , res2 = res2 , lig1 = lig1 , lig2 = lig2))
            pymol.cmd.orient("sele")
            pymol.cmd.move("z" , -2.5)
            pymol.cmd.png("{pdb_id}_{ligid}.png".format(pdb_id=pdb_id,ligid = ligid))
            time.sleep(3)
            pymol.cmd.delete(pdb_id)
            
                           
             
