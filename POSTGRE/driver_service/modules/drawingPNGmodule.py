# PICTURE DRAWING MODULE
# import rdkit
# from matplotlib.colors import ColorConverter 
# def generate_png(SMILES, user_id):
# 	mol = rdkit.Chem.MolFromSmiles("{}".format(SMILES))
# 	img = rdkit.Chem.Draw.MolToImage(mol, size=(500, 500), kekulize=True, wedgeBonds=True, fitImage=True)
# 	png = './tmp/PNG/{}.png'.format(user_id)
# 	img.save(png)

import rdkit
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

def generate_png(SMILES, user_id):
	try:
		#print(SMILES, "this is smiles from which is picture generated")
		mol = Chem.MolFromSmiles(SMILES)
		rdkit.Chem.SanitizeMol(mol)
		d = rdMolDraw2D.MolDraw2DCairo(500, 600) # or MolDraw2DSVG to get SVGs
		# d.SetFontSize()
		d.drawOptions().addStereoAnnotation = True
		# d.drawOptions().addAtomIndices = True
		d.DrawMolecule(mol)
		d.FinishDrawing()
		png = './tmp/PNG/{}.png'.format(user_id)
		with open(png, 'wb') as f:   
		    f.write(d.GetDrawingText())
	except:
		raise ValueError