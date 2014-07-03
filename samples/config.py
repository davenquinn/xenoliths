import os

DEBUG = True

SITE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),"..")

CATIONS = "Si Fe Mg Ti Al Na Ca Mn Cr Ni".split()
OXIDES = "SiO2 FeO MgO TiO2 Al2O3 Na2O CaO MnO Cr2O3 NiO".split()
SAMPLES = "CK-1 CK-2 CK-3 CK-4 CK-5 CK-6 CK-7 CKD1 CKD2".split()

MINERALS = [
	("cpx", "Clinopyroxene"),
	("opx", "Orthopyroxene"),
	("sp", "Spinel"),
	("ol", "Olivine"),
	("na", "Unknown")
]

MINERAL_SYSTEMS = {
	"silicate": {
		"si": {"SiO2": 1},
		"fe": {"FeO": 1},
		"mg": {"MgO": 1}
	},
	"pyroxene": {
		"Wo": {"SiO2":1,"CaO":1},
		"En": {"SiO2":1,"MgO":1},
		"Fs": {"SiO2":1,"FeO":1}
	},
	"na_px": {
		"di": {"SiO2":2,"CaO":1,"MgO":1},
		"he": {"SiO2":2, "CaO":1,"FeO":1},
		"ja": {"SiO2":2, "Al2O3":.5,"Na2O":.5}
	},
	"olivine": {
		"Fo": {"SiO2":1,"MgO":2},
		"Fa": {"SiO2":1,"FeO":2}
	},
	"minerals": {
		"sp": {"FeO + MgO": 1, "Al2O3 + Cr2O3": 1},
		"ol": {"FeO + MgO":2,"SiO2":1},
		"cpx": {"FeO + MgO":1,"CaO":1,"SiO2": 2},
		"opx": {"FeO + MgO":2,"SiO2": 2}
	}
}
