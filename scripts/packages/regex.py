import re
regex = r"((((meth?icillin|vancomycin)?(-| )?resistan(ce|t) )?(staph(ylo)?(cocc[uai][ls]?|bacill[ui]s?)?|S\.?(?= aureus))( (aureus|A\.?))?|MRSA|VRSA) ?((( \+|-|pos(itive)|neg(ative) )?stat(e|us))| infection)?)"
regex = re.compile(regex,re.IGNORECASE)

test1 = "methicillin resistant staphylococcus aureus status"
test2 = "mrsa"



print regex.findall(test1)
print regex.findall(test2)