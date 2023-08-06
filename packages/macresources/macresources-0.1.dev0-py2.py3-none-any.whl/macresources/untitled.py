import macresources

for fn in open('../biglist'):
	fn = fn.rstrip('\n')
	print(fn)
	base = open(fn+'/..namedfork/rsrc','rb').read()
	mein = list(macresources.iter_from_rsrcfork(base))
	print(mein)
	ser = macresources.make_rez_code(mein)
	open(fn+'.rdump','wb').write(mein)
