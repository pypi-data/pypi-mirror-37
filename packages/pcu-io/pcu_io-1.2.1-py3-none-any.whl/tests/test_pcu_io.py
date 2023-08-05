import unittest

from pcu_io.pcu_io import getEquivalentTextfile

class test_pcu_io(unittest.TestCase):

    def test_getEquivalentTextfile(self):
    	textfilename_json = getEquivalentTextfile("data/products.json")
    	try:
    		textfile_json = open(textfilename_json,"r")
    	except IOError:
    		print('cannot open')
    	else:
    		text_json = textfile_json.read()
    		print(text_json)
    		self.assertIn('Scandi', text_json)
    		textfile_json.close()
    	textfilename_pdf = getEquivalentTextfile("data/tika.pdf")
    	try:
    		textfile_pdf = open("data/tika.txt","r")
    	except IOError:
    		print('cannot open')
    	else:
    		text_pdf = textfile_pdf.read()
    		self.assertIn('Apache', text_pdf)
    		textfile_pdf.close()

if __name__ == '__main__':
    unittest.main()