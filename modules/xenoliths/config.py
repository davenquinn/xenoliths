import os

DEBUG = True

DB_NAME = "xenoliths_flask"
SQLALCHEMY_DATABASE_URI = "postgresql://Daven@localhost/"+DB_NAME

SITE_DIR = "/Users/Daven/Development/Xenoliths/"

DATA_DIR = os.path.join(SITE_DIR,"data")
RAW_DATA = os.path.join(SITE_DIR,"raw_data")

CATIONS = "Si Fe Mg Ti Al Na Ca Mn Cr Ni".split()
OXIDES = "SiO2 FeO MgO TiO2 Al2O3 Na2O CaO MnO Cr2O3 NiO".split()
SAMPLES = "CK-1 CK-2 CK-3 CK-4 CK-5 CK-6 CK-7 CK-D1 CK-D2".split()

CATION_BASIS = dict(
	Si=2,
	Fe=1,
	Mg=1,
	Ti=2,
	Al=1.5,
	Na=0.5,
	Ca=1,
	Mn=1,
	Cr=1.5,
	Ni=1
)

MINERALS = {
	"cpx": "Clinopyroxene",
	"opx": "Orthopyroxene",
	"sp": "Spinel",
	"ol": "Olivine",
	"na": "Unknown"
}

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
