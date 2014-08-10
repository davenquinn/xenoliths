module.exports =
    samples:
        "CK-2":
            bounds: [
                0.0
                -8640.0
                8577.0
                0.0
            ]
            layers:
                sem: [
                    0
                    -8640.0
                ]
                scan: [ # 0.0, -11466.0, 11519.0, 0.0
                    -1447
                    -10054
                ]

            color: "#456AA0"

        "CK-3":
            bounds: [
                0.0
                -5040.0
                11436.0
                0.0
            ]
            layers:
                sem: [
                    0
                    -5040.0
                ]
                scan: [
                    0
                    -5040.0
                ]

            color: "#FF9700"

        "CK-4":
            bounds: [
                0.0
                -7200.0
                8577.0
                0.0
            ]
            layers:
                sem: [
                    0.0
                    -7200.0
                ]
                scan: [
                    0.0
                    -7200.0
                ]

            color: "#FFD100"

        "CK-5":
            bounds: [
                0.0
                -9854.0
                9920.0
                0.0
            ]
            layers:
                sem: [
                    0.0
                    -9854.0
                ]
                scan: [ #[-485*2,-11882]//0.0, -12571.0, 12402.0, 0.0
                    -956
                    -11197
                ]

            color: "#3A9B88"

        "CK-6":
            bounds: [
                0.0
                -8338.0
                8928.0
                0.0
            ]
            layers:
                sem: [
                    0.0
                    -8338.0
                ]
                scan: [ # 0.0, -11632.0, 11528.0, 0.0
                    -2 * 816 - 6
                    -11632 + 526 + 516
                ]

            color: "#FF2C00"

        "CK-7":
            bounds: [
                0.0
                -9096.0
                8928.0
                0.0
            ]
            layers:
                sem: [
                    0.0
                    -9096.0
                ]
                scan: [ #0.0, -11642.0, 11529.0, 0.0
                    -782 - 194
                    -(9096 + 482) - 566
                ]

            color: "#8BD750"

        CKD1:
            bounds: [
                0.0
                -9854.0
                13776.0
                0.0
            ]
            layers:
                sem: [
                    0.0
                    -9854.0
                ]
                scan: [ #0.0, -11642.0, 11529.0, 0.0
                    0.0
                    -9854.0
                ]

            color: "#888888"

        CKD2:
            bounds: [
                0.0
                -5306.0
                11904.0
                0.0
            ]
            layers:
                sem: [
                    0.0
                    -5306.0
                ]
                scan: [ #0.0, -11642.0, 11529.0, 0.0
                    0.0
                    -5306.0
                ]

            color: "#444444"

    minerals:
        cpx:
            name: "Clinopyroxene"
            color: "#a6ff9b"

        opx:
            name: "Orthopyroxene"
            color: "#cc0000"

        ol:
            name: "Olivine"
            color: "#006699"

        sp:
            name: "Spinel"
            color: "#663300"

        al:
            name: "Alteration"
            color: "#888888"

        na:
            name: "None"
            color: "#000000"

    oxides: [
        "SiO2"
        "MgO"
        "FeO"
        "CaO"
        "Al2O3"
        "Cr2O3"
        "TiO2"
        "NiO"
        "MnO"
        "Na2O"
    ]
    cations: [
        "Si"
        "Mg"
        "Fe"
        "Ca"
        "Al"
        "Cr"
        "Ti"
        "Ni"
        "Mn"
        "Na"
    ]
    bad_tags: [
        "bad"
        "alteration"
        "mixed"
        "marginal"
        "anomalous"
        "review"
        "near alteration"
    ]
    systems:
        silicate:
            components: [
                "si"
                "fe"
                "mg"
            ]

        pyroxene:
            components: [
                "Wo"
                "Fs"
                "En"
            ]

        na_px:
            components: [
                "ja"
                "he"
                "di"
            ]
