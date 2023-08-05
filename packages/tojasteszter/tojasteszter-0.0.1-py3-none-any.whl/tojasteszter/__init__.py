from random import shuffle

class GenTester:
    
    def __init__(self,maxnemtorik,emelet,tojasno):
        self.maxnemtorik = maxnemtorik
        self.emelet = emelet
        self.tojasno = tojasno
        self.dobasok = 0
        self.toresek = 0
        self.elfogyott = False
    
    
    def dobalo(self,k):
        if self.toresek == self.tojasno:
            self.elfogyott = True
        self.dobasok += 1
        if k <= self.maxnemtorik:
            return False
        else:
            self.toresek += 1
            return True

def test(fun,emelet=100,tojas=2,verbose=True):
    
    cases = list(range(1,emelet+1))
    shuffle(cases)    

    maxtry = 0
    maxcase = 0
    correct = 0
    incorrect = 0
    overrun = 0

    for case in cases:
        testinst = GenTester(case,emelet,tojas)
        out = fun(testinst.dobalo)
        if testinst.dobasok > maxtry:
            maxtry = testinst.dobasok
            maxcase = case
        if testinst.elfogyott:
            overrun += 1
        if out == case:
            correctinst = True
            correct += 1
        else:
            correctinst = False
            incorrect += 1
        if verbose:
            print('\n\n###### %d-es eset: ######' % case)
            if not correctinst:
                print('----------------------- HIBÁS VÁLASZ -----------------------')
            if testinst.elfogyott:
                print('----- HIBA: ELFOGYOTT A TOJÁS MIELŐTT MEGVOLT A VÁLASZ -----')
            print('a helyes válasz:  %d\nadott válasz:  %d\ndobási kísérlet:    %d\ntörött tojás:   %d' % (case,out,testinst.dobasok,testinst.toresek))

    print('------------ ÖSSZESEN: ------------')
    print('%d helyes válasz\n%d helytelen válasz\n%d alkalommal fogyott el a tojás\n%d volt a legtöbb dobás ami kellett válaszhoz\n%d volt a helyes válasz mikor a legtöbb dobás kellett' % (correct,incorrect,overrun,maxtry,maxcase))



