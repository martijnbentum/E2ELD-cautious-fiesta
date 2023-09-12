class Mapper:
    '''map phonemes from one set to another set.'''
    def __init__(self, language = 'english'):
        self.language = language
        self.ipa_set = ipa_set
        self.sampa_set = sampa_set
        self.celex_set = celex_set
        self.disc_set = disc_set
        self.examples_dutch = examples_dutch
        self.examples_english= examples_english
        self.examples_german= examples_german
        names = 'ipa_set,sampa_set,celex_set,disc_set'
        names += ',examples_dutch,examples_english,examples_german'
        self.names = names.split(',')
        self._make_dicts()
        self._add_arpabet()
        if self.language != 'dutch':
            self._fix_w()

    def _make_dicts(self):
        '''create dicts to map ipa, sampa, celex and disc phonemes
        '''
        self.ipa_to_sampa = {}
        self.ipa_to_celex = {}
        self.ipa_to_disc = {}
        self.sampa_to_ipa = {}
        self.sampa_to_celex = {}
        self.sampa_to_disc= {}
        self.celex_to_ipa = {}
        self.celex_to_sampa = {}
        self.celex_to_disc = {}
        self.disc_to_ipa = {}
        self.disc_to_sampa = {}
        self.disc_to_celex = {}
        
        sets = [self.ipa_set,self.sampa_set]
        sets += [self.celex_set,self.disc_set]
        for ipa, sampa, celex, disc in zip(*sets):
            self.ipa_to_sampa[ipa] = sampa
            self.ipa_to_disc[ipa] = disc
            self.ipa_to_celex[ipa] = celex
            self.sampa_to_ipa[sampa] = ipa
            self.sampa_to_disc[sampa] = disc
            self.sampa_to_celex[sampa] = celex
            self.celex_to_ipa[celex] = ipa
            self.celex_to_sampa[celex] = sampa
            self.celex_to_disc[celex] = disc
            self.disc_to_ipa[disc] = ipa
            self.disc_to_sampa[disc] = sampa
            self.disc_to_celex[disc] = celex

    def _add_arpabet(self):
        self.ipa_to_arpabet = ipa_to_arpabet
        self.arpabet_to_ipa = arpabet_to_ipa
        self.arpabet_to_examples = arpabet_to_examples
        self.arpabet_to_disc= {}
        self.disc_to_arpabet = {}
        for ipa, disc in self.ipa_to_disc.items():
            if ipa == '*': ipa = 'r'
            if ipa == 'iː': ipa = 'i'
            if ipa == 'uː': ipa = 'u'
            if ipa == 'ɑɪ': ipa = 'ai'
            if ipa == 'ɑ̃ː': ipa = 'ɑː'
            if ipa not in self.ipa_to_arpabet.keys():
                continue
            arpabet= self.ipa_to_arpabet[ipa]
            self.arpabet_to_disc[arpabet] = disc
            self.disc_to_arpabet[disc] = arpabet
        
    def _fix_w(self):
        self.celex_to_ipa['w'] ='w'
        self.sampa_to_ipa['w'] ='w'
        self.disc_to_ipa['w'] ='w'

            

def validate(ipa = None):
    if not ipa: ipa = Ipa()
    n_items = {}
    for name in ipa.names:
        attr = getattr(ipa,name)
        n_items[name] = len(attr)
    return n_items
    
        
def set_none(examples):
    for index, example in enumerate(examples):
        if example == 'None':
            examples[index] = None
    return examples

def show(ipa = None):
    if not ipa: ipa = Ipa()
    attrs = [getattr(ipa,name) for name in ipa.names]
    for line in zip(*attrs):
        sl = list(map(str,line))
        sl[:4] = [x.ljust(4) for x in sl[:4]]
        print('\t'.join(sl))


ipa_set = 'p,b,t,d,k,g,ŋ,m,n,l,r,f,v,θ,ð,s,z,ʃ,ʒ,j,x,ɣ'
ipa_set += ',h,w,ʋ,pf,ts,tʃ,dʒ,ŋ̩,m̩,n̩,l̩,*,iː,iːː,ɑː,aː,ɔː'
ipa_set += ',uː,ɜː,yː,yːː,ɛː,æː,ɒː,eː,øː,oː,eɪ,ɑɪ,ɔɪ,əʊ'
ipa_set += ',aʊ,ɪə,ɛə,ʊə,ɛi,œy,ɑu,ai,au,ɔy,ɪ,Y,ɛ,œ,æ,a,ɑ'
ipa_set += ',ɒ,ʌ,ɔ,ʊ,ʉ,ə,œ̃,æ̃,ɑ̃ː,æ̃ː,ɒ̃ː'
ipa_set = ipa_set.split(',')

sampa_set = 'p.b.t.d.k.g.N.m.n.l.r.f.v.T.D.s.z.S.Z.j.x.G.h.w.w'
sampa_set += '.pf.ts.tS.dZ.N,.m,.n,.l,.r*.i:.i::.A:.a:.O:.u:'
sampa_set += '.3:.y:.y::.E:./:.Q:.e:.|:.o:.eI.aI.OI.@U.aU'
sampa_set += '.I@.E@.U@.EI./I.Au.ai.au.Oy.I.Y.E./.{.a.A'
sampa_set += '.Q.V.O.U.}.@./".{".A":.{":.O":'
sampa_set = sampa_set.split('.')

celex_set = 'p.b.t.d.k.g.N.m.n.l.r.f.v.T.D.s.z.S.Z.j.x.G.h.w.w'
celex_set += '.pf.ts.tS.dZ.N,.m,.n,.l,r*..i:.i::.A:.a:.O:.u:'
celex_set += '.3:.y:.y::.E:.U:.Q:.e:.&:.o:.eI.aI.OI.@U.aU'
celex_set += '.I@.E@.U@.EI.UI.AU.ai.au.Oy.I.Y.E.Q.&.a.A'
celex_set += '.Q.V.O.U.U.@.Q".&".A":.&":.O":'
celex_set = celex_set.split('.')

disc_set = 'p,b,t,d,k,g,N,m,n,l,r,f,v,T,D,s,z,S,Z,j,x,G,h,w,w'
disc_set += ',+,=,J,_,C,F,H,P,R,i,!,#,a,$,u,3,y,(,),*,<,e,|,o,1,2,4'
disc_set += ',5,6,7,8,9,K,L,M,W,B,X,I,Y,E,/,{,&,A,Q,V,O,U,},@,^'
disc_set += ',c,q,O,"'
disc_set = disc_set.split(',')

examples_dutch = 'put,bad,tak,dak,kat,goal,lang,mat,nat,lat'
examples_dutch += ',rat/later,fiets,vat,None,None,sap,zat,sjaal'
examples_dutch += ',ravage'
examples_dutch += ',jas,light/gaat,regen,had,None,wat,None,None'
examples_dutch += ',None'
examples_dutch += ',jazz,None,None,None,None,None,liep,analyse,None'
examples_dutch += ',laat,None,boek,None,buut,centrifuge,scene'
examples_dutch += ',freule,zone'
examples_dutch += ',leeg,deuk,boom,None,None,None,None,None'
examples_dutch += ',None'
examples_dutch += ',None,None,wijs,huis,koud,None,None,None'
examples_dutch += ',lip,None,leg,None,None,None,lat,None,None,bom'
examples_dutch += ',None'
examples_dutch += ',put,gelijk,None,None,None,None,None'
examples_dutch = set_none(examples_dutch.split(','))

    
examples_english = 'pat,bad,tack,dad,cad,game,bang,mad,nat,lad'
examples_english += ',rat,fat'
examples_english += ',vat,thin,then,sap,zap,sheep,measure,yank,loch'
examples_english += ',None,had,why,None,None,None,cheap,jeep,bacon'
examples_english += ',idealism,burden,dangle,father,bean,None,barn'
examples_english += ',None,born,boon,burn,None,None,None,None'
examples_english += ',None,None,None,None,bay,buy,boy,no,brow'
examples_english += ',peer,pair'
examples_english += ',poor,None,None,None,None,None,None,pit'
examples_english += ',None,pet'
examples_english += ',None,pat,None,None,pot,putt,None,put'
examples_english += ',None,another'
examples_english += ',None,timbre,detente,lingerie,bouillon'
examples_english = set_none(examples_english.split(','))

examples_german = 'Pakt,Bad,Tag,dann,kalt,Gast,Klang,maß'
examples_german += ',naht,Last,Ratte'
examples_german += ',falsh,Welt,None,None,Gas,Suppe,Schiff'
examples_german += ',Genie,Jack'
examples_german += ',Bach/ich,None,Hand,waterproof,None,Pferd'
examples_german += ',Zahl,Matsch'
examples_german += ',Gin,None,None,None,None,None,Lied'
examples_german += ',None,Advantage'
examples_german += ',klar,Allroundman,Hut,Teamwork,für,None'
examples_german += ',Käse,None,None'
examples_german += ',Mehl,Möbel,Boot,Native,Shylock,Playboy,None'
examples_german += ',Allroundsportler,None,None,None,None,None,None'
examples_german += ',weit,Haut,freut,Mitte,Pfütze,Bett'
examples_german += ',Götter,Ragtime'
examples_german += ',hat,Kalevala,None,Plumpudding,Glocke,Pult,None'
examples_german += ',Beginn,Parfum,impromptu,Détente,lingerie'
examples_german += ',bouillon'
examples_german = set_none(examples_german.split(','))
    

arpabet_to_ipa = {
    'AA': 'ɑ',
    'AE': 'æ',
    'AH': 'ʌ',
    'AO': 'ɔ',
    'AW': 'aʊ',
    'AX': 'ə',
    'AY': 'ai',
    'EH': 'ɛ',
    'ER': 'ɝ',
    'EY': 'eɪ',
    'IH': 'ɪ',
    'IX': 'ɨ',
    'IY': 'i',
    'OW': 'oʊ',
    'OY': 'ɔɪ',
    'UH': 'ʊ',
    'UW': 'u',
    'UX': 'ʉ',
    'B': 'b',
    'CH': 'tʃ',
    'D': 'd',
    'DH': 'ð',
    'DX': 'ɾ',
    'EL': 'l̩',
    'EM': 'm̩',
    'EN': 'n̩',
    'F': 'f',
    'G': 'g',
    'HH': 'h',
    'H': 'h',
    'JH': 'dʒ',
    'K': 'k',
    'L': 'l',
    'M': 'm',
    'N': 'n',
    'NX': 'ɾ̃',
    'NG': 'ŋ',
    'P': 'p',
    'Q': 'ʔ',
    'R': 'ɹ',
    'S': 's',
    'SH': 'ʃ',
    'T': 't',
    'TH': 'θ',
    'V': 'v',
    'W': 'w',
    'WH': 'ʍ',
    'Y': 'j',
    'Z': 'z',
    'ZH': 'ʒ'
}

ipa_to_arpabet = {}
for key,value in arpabet_to_ipa.items():
    ipa_to_arpabet[value] = key
ipa_to_arpabet['n̩'] = 'n'
ipa_to_arpabet['r'] = 'R'
ipa_to_arpabet['x'] = 'X'
ipa_to_arpabet['ɜː'] = 'ER'
ipa_to_arpabet['ɑɹ'] = 'R'
ipa_to_arpabet['ɚ'] = 'AX'
ipa_to_arpabet['əʊ'] = 'UH'
ipa_to_arpabet['ɪə'] = 'IH'
ipa_to_arpabet['ɛə'] = 'EH'
ipa_to_arpabet['ʊə'] = 'UH'
ipa_to_arpabet['æ̃'] = 'AE'
ipa_to_arpabet['ɔ̃'] = 'AO'
ipa_to_arpabet['m̩'] = 'M'
ipa_to_arpabet['ɑː'] = 'AA'
ipa_to_arpabet['ɔː'] = 'AO'


arpabet_to_examples = {
    'AA': 'b(al)m,b(o)t',
    'AE': 'b(a)t',
    'AH': 'b(u)tt',
    'AO': 'c(augh)t,st(o)ry',
    'AW': 'b(ou)t',
    'AX': 'comm(a)',
    'AY': 'b(i)te',
    'EH': 'b(e)t',
    'ER': 'b(ir)d,forew(or)d',
    'EY': 'b(ai)t',
    'IH': 'b(i)t',
    'IX': 'ros(e)s,rabb(i)t',
    'IY': 'b(ea)t',
    'OW': 'b(oa)t',
    'OY': 'b(oy)',
    'UH': 'b(oo)k',
    'UW': 'b(oo)t',
    'UX': 'd(u)de',
    'B': '(b)uy',
    'CH': '(Ch)ina',
    'D': '(d)ie',
    'DH': '(th)y',
    'DX': 'bu(tt)er',
    'EL': 'bott(le)',
    'EM': 'ryth(m)',
    'EN': 'butt(on)',
    'F': '(f)ight',
    'G': '(g)uy',
    'HH': '(h)igh',
    'H': '(h)igh',
    'JH': '(j)ive',
    'K': '(k)ite',
    'L': '(l)ie',
    'M': '(m)y',
    'N': '(n)igh',
    'NX': 'wi(nn)er',
    'NG': 'si(ng)',
    'P': '(p)',
    'Q': 'uh(-)oh',
    'R': '(r)ye',
    'S': '(s)igh',
    'SH': '(sh)y',
    'T': '(t)ie',
    'TH': '(th)igh',
    'V': '(v)ie',
    'W': '(w)ise',
    'WH': '(wh)y',
    'Y': '(y)acht',
    'Z': '(z)oo',
    'ZH': 'plea(s)ure'
}
    