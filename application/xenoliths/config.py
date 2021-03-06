import os

DEBUG = True

DB_NAME = "xenoliths_flask"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "postgresql://Daven@localhost/"+DB_NAME

SITE_DIR = "/Users/Daven/Development/Xenoliths/versioned/application"

DATA_DIR = os.path.join(SITE_DIR,"data")
DB_BACKUP_DIR = os.path.join(DATA_DIR, "backups")
RAW_DATA = os.path.join(SITE_DIR,"raw_data")

CATIONS = "Si Fe Mg Ti Al Na Ca Mn Cr Ni K".split()
OXIDES = "SiO2 FeO MgO TiO2 Al2O3 Na2O CaO MnO Cr2O3 NiO K2O".split()
SAMPLES = "CK-1 CK-2 CK-3 CK-4 CK-5 CK-6 CK-7 CK-D1 CK-D2".split()

LOG_DIR = os.path.join(DATA_DIR,"logs")

MINERALS = {
	"cpx": "Clinopyroxene",
	"opx": "Orthopyroxene",
	"sp": "Spinel",
	"ol": "Olivine",
    "al": "Alteration",
	"na": "Unknown"
}

MINERAL_DENSITIES = {
	"cpx": 3.279,
	"opx": 3.204,
	"ol": 3.21,
	"sp": 3.6,
	"al": 3.23
}

COLORS = {
	"CK-2": "#456AA0",
	"CK-3": "#FF9700",
	"CK-4": "#FFD100",
	"CK-5": "#3A9B88",
	"CK-6": "#FF2C00",
	"CK-7": "#8BD750",
    "CK-1": "#999999",
	"CK-D1": "#888888",
	"CK-D2": "#444444"
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

BAD_TAGS = [
	"bad",
	"alteration",
	"mixed",
	"marginal",
	"anomalous",
	"review",
	"near alteration"
]

