#!/usr/bin/python
import pprint
class PdbSumObj(object):

    def __init__(self,line):
        self.interactions = []
        self.interactions.append(line)
        self.pdb_id = line.split(",")[-1].split("_")[0].lower()
        #line_array[i:i + 2] for i in range(0,len(line_array),2)]
    
    def __repr__(self):
        return " AND ".join(self.interactions)    

    def is_valid(self):
        bools = []
        for i in self.interactions:
            bools.append(len(i.split(",")) == 9)
        return not(False in bools)

    def append_interaction(self,interaction_text):
        self.interactions.append(interaction_text)

    def get_atoms_in_interaction_string(self):
        atoms = [ line.split(",")[1] for line in self.interactions]
        return " or id ".join(atoms)
    
        
if __name__ == '__main__':
    p = PdbSumObj("312,3293,N19,3601,CAU,408,A ,2.85,2RH1_grow.out")
    p.append_interaction("312,3294,O17,3598,CAU,408,A ,2.77,2RH1_grow.out")
    print "Interactions for" , p.pdb_id ,":\n", p  
    print "Validity", p.is_valid()
    p.append_interaction("312,3293,N19,3601,CAU,408,A ,2.85,2RH1_grow.out")
    print p
    print p.get_atoms_in_interaction_string()
