import utils

def make_mald_ipa(arpabet_phonemes):
    ipa = []
    for phoneme in arpabet_phonemes.split(' '):
        phoneme = utils.remove_numeric(phoneme)
        if phoneme in arpabet_to_ipa.keys():
            ipa.append(arpabet_to_ipa[phoneme])
        else:
            for char in phoneme:
                ipa.append(arpabet_to_ipa[char])
    return ' '.join(ipa)
    
        

arpabet_to_ipa = {
    'AA': 'ɑ',
    'AE': 'æ',
    'AH': 'ʌ',
    'AO': 'ɔ',
    'AW': 'aʊ',
    'AX': 'ə',
    'AY': 'aɪ',
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
    'G': 'ɡ',
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

ipa_to_examples = {}
for key, value in arpabet_to_examples.items():
    ipa_to_examples[ arpabet_to_ipa[key] ] = value

sampa_to_ipa = {
	"p":'p',
	"b":'b',
	"t":'t',
	"d":'d',
	"4":'ɾ',
	"tS":'tʃ',
	"dZ":'dʒ',
	"k":'k',
	"g":'ɡ',
	"f":'f',
	"v":'v',
	"T":'θ',
	"D":'ð',
	"s":'s',
	"z":'z',
	"S":'ʃ',
	"Z":'ʒ',
	"h":'h',
	"m":'m',
	"n":'n',
    "n,":'n̩',
	"N":'ŋ',
	"l":'l',
	"l,":'l̩',
	"r\\":'ɹ',
	# "r":'ɹ',
	"r":'r',
	"w":'w',
	"j":'j',
	"W":'ʍ',
	"x":'x',
	"A":'ɑ',
	"i":'i',
	"I":'ɪ',
	"E":'ɛ',
    "3":'ɜː',
	"3`":'ɝ',
	"{":'æ',
	"Ar\\":'ɑɹ',
	"V":'ʌ',
	"A":'ɑ',
	"O":'ɔ', 
	"U":'ʊ',
	"u":'u',
	"@":'ə',
	"@`":'ɚ',
    "@U":'əʊ',
	"eI":'eɪ',
	"aI":'aɪ',
	"OI":'ɔɪ',
	"oU":'oʊ', 
	"aU":'aʊ',
	# "ju":'ju',
	"I@":'ɪə',
	"E@":'ɛə',
	"U@":'ʊə',
	# "ir\\":'iɹ',
	# "er\\":'eɹ',
	# "Ur\\":'ʊɹ',
    'A~:':'æ̃',
    'O~:':'ɔ̃',
}

ipa_to_sampa = {}
for sampa, ipa in ipa_to_sampa.keys():
    ipa_to_sampa[ipa] = sampa

arpabet_to_sampa = {}
for sampa, ipa in sampa_to_ipa.items():
    # if ipa not in ipa_to_arpabet.keys(): continue
    arpabet_to_sampa[ ipa_to_arpabet[ipa] ] = sampa

sampa_to_arpabet = {}
for arpabet, sampa in arpabet_to_sampa.items():
    sampa_to_arpabet[sampa] = arpabet

    


celex_to_sampa = {}
celex_to_sampa["p"] = "p"
celex_to_sampa["b"] = "b"
celex_to_sampa["t"] = "t"
celex_to_sampa["d"] = "d"
celex_to_sampa["k"] = "k"
celex_to_sampa["g"] = "g"
celex_to_sampa["N"] = "N"
celex_to_sampa["m"] = "m"
celex_to_sampa["n"] = "n"
celex_to_sampa["n,"] = "n,"
celex_to_sampa["l"] = "l"
celex_to_sampa["l,"] = "l,"
celex_to_sampa["r"] = "r"
celex_to_sampa["f"] = "f"
celex_to_sampa["v"] = "v"
celex_to_sampa["T"] = "T"
celex_to_sampa["D"] = "D"
celex_to_sampa["s"] = "s"
celex_to_sampa["z"] = "z"
celex_to_sampa["S"] = "S"
celex_to_sampa["Z"] = "Z"
celex_to_sampa["j"] = "j"
celex_to_sampa["x"] = "x"
celex_to_sampa["h"] = "h"
celex_to_sampa["w"] = "w"
celex_to_sampa["tS"] = "tS"
celex_to_sampa["dZ"] = "dZ"
celex_to_sampa["i"] = "i"
celex_to_sampa["i:"] = "i"
celex_to_sampa["V"] = "V"
celex_to_sampa["I"] = "I"
celex_to_sampa["O"] = "O"
celex_to_sampa["u"] = "u"
celex_to_sampa["U"] = "U"
celex_to_sampa["3"] = "3"
celex_to_sampa["y"] = "y"
celex_to_sampa["E"] = "E"
celex_to_sampa["e"] = "e"
celex_to_sampa["o"] = "o"
celex_to_sampa["eI"] = "eI"
celex_to_sampa["aI"] = "aI"
celex_to_sampa["&"] = "{"
celex_to_sampa["@"] = "@"
celex_to_sampa["A:"] = "A"
celex_to_sampa["@U"] = "@U"
celex_to_sampa["aU"] = "aU"
celex_to_sampa["OI"] = "OI"
celex_to_sampa["aU"] = "aU"
celex_to_sampa["I@"] = "I@"
celex_to_sampa["E@"] = "E@"
celex_to_sampa["U@"] = "U@"
celex_to_sampa["A~:"] = "A~:"
celex_to_sampa["O~:"] = "O~:"

sampa_to_celex = {}
for celex, sampa in celex_to_sampa.items():
    sampa_to_celex[sampa] = celex

celex_to_ipa = {}
for celex, sampa in celex_to_sampa.items():
    if not sampa in sampa_to_ipa.keys(): continue
    celex_to_ipa[celex] = sampa_to_ipa[sampa]

ipa_to_celex = {}
for celex, ipa in celex_to_ipa.items():
    ipa_to_celex[ipa] = celex

celex_to_arpabet = {}
for arpabet, ipa in arpabet_to_ipa.items():
    if not ipa in ipa_to_celex.keys(): continue
    celex_to_arpabet[ ipa_to_celex[ipa] ] = arpabet

arpabet_to_celex = {}
for celex, arpabet in celex_to_arpabet.items():
    arpabet_to_celex[arpabet] = celex


disc_to_sampa = {}
disc_to_sampa["p"] = "p"
disc_to_sampa["b"] = "b"
disc_to_sampa["t"] = "t"
disc_to_sampa["d"] = "d"
disc_to_sampa["k"] = "k"
disc_to_sampa["g"] = "g"
disc_to_sampa["N"] = "N"
disc_to_sampa["m"] = "m"
disc_to_sampa["n"] = "n"
disc_to_sampa["H"] = "n,"
disc_to_sampa["l"] = "l"
disc_to_sampa["P"] = "l,"
disc_to_sampa["R"] = "r"
disc_to_sampa["r"] = "r"
disc_to_sampa["f"] = "f"
disc_to_sampa["v"] = "v"
disc_to_sampa["T"] = "T"
disc_to_sampa["D"] = "D"
disc_to_sampa["s"] = "s"
disc_to_sampa["z"] = "z"
disc_to_sampa["S"] = "S"
disc_to_sampa["Z"] = "Z"
disc_to_sampa["j"] = "j"
disc_to_sampa["x"] = "x"
disc_to_sampa["h"] = "h"
disc_to_sampa["w"] = "w"
disc_to_sampa["J"] = "tS"
disc_to_sampa["_"] = "dZ"
disc_to_sampa["i"] = "i"
disc_to_sampa["I"] = "I"
disc_to_sampa["E"] = "E"
disc_to_sampa['c'] = '{'
disc_to_sampa["{"] = "{"
disc_to_sampa["V"] = "V"
disc_to_sampa["$"] = "O"
disc_to_sampa["#"] = "A"
disc_to_sampa["Q"] = "O"
disc_to_sampa["$"] = "O"
disc_to_sampa["u"] = "u"
disc_to_sampa["U"] = "U"
# disc_to_sampa["y"] = "y"
disc_to_sampa["E"] = "E"
# disc_to_sampa["e"] = "e"
# disc_to_sampa["o"] = "o"
disc_to_sampa["1"] = "eI"
disc_to_sampa["2"] = "aI"
disc_to_sampa["3"] = "3"
disc_to_sampa["4"] = "OI"
disc_to_sampa["5"] = "@U"
disc_to_sampa["6"] = "aU"
disc_to_sampa["7"] = "I@"
disc_to_sampa["8"] = "E@"
disc_to_sampa["9"] = "U@"
disc_to_sampa["@"] = "@"
disc_to_sampa['q'] = 'A~:'
disc_to_sampa['~'] = 'O~:'

sampa_to_disc = {}
for disc, sampa in disc_to_sampa.items():
    sampa_to_disc[sampa] = disc

celex_to_disc = {}
for disc, sampa in disc_to_sampa.items():
    celex_to_disc[sampa_to_celex[sampa]] = disc

disc_to_celex = {}
for celex, disc in celex_to_disc.items():
    disc_to_celex[disc] = celex

disc_to_ipa = {}
for disc, sampa in disc_to_sampa.items():
    disc_to_ipa[disc] = sampa_to_ipa[sampa]

ipa_to_disc = {}
for disc, ipa in disc_to_ipa.items():
    ipa_to_disc[ipa] = disc

disc_to_arpabet = {}
for disc, sampa in disc_to_sampa.items():
    ipa = sampa_to_ipa[sampa]
    disc_to_arpabet[disc] = ipa_to_arpabet[ipa]

arpabet_to_disc = {}
for disc, arpabet in disc_to_arpabet.items():
    arpabet_to_disc[arpabet] = disc

