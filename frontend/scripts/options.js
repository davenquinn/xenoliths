define([],function(){
	options = {
		samples: {
			"CK-2": {
				"bounds": [0.0, -8640.0, 8577.0, 0.0]
			},
			"CK-3": {
				"bounds": [0.0, -5040.0, 11436.0, 0.0]
			},
			"CK-4": {
				"bounds": [0.0, -7200.0, 8577.0, 0.0]
			},
			"CK-5": {
				"bounds": [0.0, -9854.0, 9920.0, 0.0]
			},
			"CK-6": {
				"bounds": [0.0, -8338.0, 8928.0, 0.0]
			},
			"CK-7": {
				"bounds": [0.0, -9096.0, 8928.0, 0.0]
			}
		},
		"minerals": {
			"cpx": {
				name: "Clinopyroxene",
				color: "#a6ff9b"
    		},
        	"opx": {
    			name: "Orthopyroxene",
    			color: "#cc0000"
    		},
        	"ol": {
    			name: "Olivine",
    			color: "#006699"
    		},
        	"sp": {
    			name: "Spinel",
    			color: "#663300"
    		},
    		"na": {
    			name: "None",
    			color: "#000000"
    		}
		},
		"oxides": ["SiO2","MgO","FeO","CaO","Al2O3","Cr2O3","TiO2","NiO","MnO","Na2O"],
		"cations": ["Si","Mg","Fe","Ca","Al","Cr","Ti","Ni","Mn","Na"]
	};
	return options;
});
