Attribute VB_Name = "Module1"
Option Base 1
Sub CalPyx()
' Calculate REE temperature
' Chenguang Sun
' Date: 2012-09-16
'
    Dim H2O, kk, Pre As Double
    Dim Major_c(10), Major_o(10) As Double
    Dim REE_c(15), REE_o(15) As Variant
    Dim PFMc, PFMo, T, LnD_A(15), LnD_A2(15) As Variant
    Dim Ao, Ac, A, R0_o, R0_c, E_o, E_c, Bo, bc, Br(15), B3(15), DREE(15) As Double
    Dim N_i, C_i, M_i, Mo_i, Mr_i, Mor_i, Cali_i As Integer
    Dim T_BKN2px, RN2 As Variant
    Dim i, j, RN As Integer
    
    Const PI = 3.14159265358979
    Const NA = 602
    
    kk = 2
    Cali_i = 0
    
    'IR = La, Ce, Pr, Nd, Sm, Eu, Gd, Tb, Dy, Y, Ho, Er, Tm, Yb, Lu
    IR = Array(1.16, 1.143, 1.126, 1.109, 1.079, 1.066, 1.053, 1.04, 1.027, 1.019, 1.015, 1.004, 0.994, 0.985, 0.977)

    'The Variant data type is used to declare a variable whose type is not explicitly specified.
    N_i = 14
    'C_i = the number of cells before the major data along the column
    'M_i = the number of cells before cpx major data along the row
    'Mo_i = the number of cells before opx major data along the row
    'Mr_i = the number of cells before cpx REE data along the row
    'Mor_i = the number of cells before opx REE data along the row
    C_i = 3
    M_i = 9 + 1
    Mo_i = 29 + 6 + 1
    Mr_i = 13 + 6 + 1
    Mor_i = 39 + 6 + 1
    Set r = Worksheets("Input data")
    Set rr = Worksheets("Results")
    'r.Activate
    'ActiveWindow.DisplayGridlines = False

    'RN = count the number of samples according to cpx_SiO2
    RN = Application.Count(r.Range("K:K"))

    'REE_name = Array("La", "Ce", "Pr", "Nd", "Sm", "Eu", "Gd", "Tb", "Dy", "Y", "Ho", "Er", "Tm", "Yb", "Lu")
    'r.Range("N3:AB3").Value = REE_name

    For i = 1 To RN
        Pre = r.Cells(i + C_i, 7).Value
        If Pre = Empty Then Pre = 1 'GPa
        rr.Cells(i + C_i - 1, 54).Value = Pre
        H2O = r.Cells(i + C_i, M_i - 1).Value
        H2O = 0.000170685747186617 * H2O ^ 3 - 0.006831778563526 * H2O ^ 2 + 0.109999984719062 * H2O _
                + 0.000971902247238525
        H2O = 0
        For j = 1 To 10
        
            'Major = SiO2, TiO2, Al2O3, Cr2O3, FeO, MnO, MgO, CaO, Na2O, K2O
            If IsNumeric(r.Cells(i + C_i, j + M_i).Value) Then
                Major_c(j) = r.Cells(i + C_i, j + M_i).Value
            Else
                Major_c(j) = 0
            End If
            If IsNumeric(r.Cells(i + C_i, j + Mo_i).Value) Then
                Major_o(j) = r.Cells(i + C_i, j + Mo_i).Value
            Else
                Major_o(j) = 0
            End If
        Next j
        For j = 1 To 15
            'REE = La, Ce, Pr, Nd, Sm, Eu, Gd, Tb, Dy, Y, Ho, Er, Tm, Yb, Lu
            
            REE_c(j) = r.Cells(i + C_i, j + Mr_i).Value
            'MsgBox j + Mor_i & "-" & r.Cells(i + C_i, j + Mor_i).Value
            REE_o(j) = r.Cells(i + C_i, j + Mor_i).Value
            
            If REE_c(j) > 0 And IsNumeric(REE_c(j)) _
            And REE_o(j) > 0 And IsNumeric(REE_o(j)) Then
                DREE(j) = REE_o(j) / REE_c(j)
                LnD_A(j) = DREE(j)
            Else
                DREE(j) = 0
                LnD_A(j) = ""
            End If
        Next j
        
        PFMc = PyxForm(Major_c)
        PFMo = PyxForm(Major_o)
        T_BKN2px = T_BKN_2px(PFMc, PFMo, Pre)
        
        'PFM = SiIV, AlIV, TiIV, AlVI, TiVI, CrVI, MgVI, FeVI, MgM2, FeM2, MnM2, CaM2, NaM2, KM2, MgN
        A = (-5.37068370408382) - (-7.13615731281538)
        Ao = 3.56148426371104 * PFMo(12) + 3.54081780772732 * PFMo(2)
        Ac = 4.37096420622614 * PFMc(2) + 1.9813056415739 * PFMc(9) - 0.908067851839806 * H2O
        A = A + Ao - Ac
                
        R0_o = 0.692505524356551 + 0.431788725148506 * PFMo(12) + 0.227605456716806 * PFMo(9)
        E_o = -1372.47337291936 + 1854.82137214735 * R0_o - 530.577358996128 * PFMo(12)
        
        R0_c = 1.06596147404798 - 0.103654121912384 * PFMc(4) - 0.211803756387744 * PFMc(9)
        E_c = -1996.06952151084 + 2271.90977329864 * R0_c
        For j = 1 To 15
            Bo = 4 * PI * E_o * NA * (R0_o / 2 * (R0_o - IR(j)) ^ 2 - (R0_o - IR(j)) ^ 3 / 3)
            bc = 4 * PI * E_c * NA * (R0_c / 2 * (R0_c - IR(j)) ^ 2 - (R0_c - IR(j)) ^ 3 / 3)
            Br(j) = (38733.9838585151 - 71864.8736892434 - Bo + bc) / 8.3145
            B3(j) = Br(j) * 0.001
        Next j
        rr.Range("A" & i + C_i - 1 & ":A" & i + C_i - 1 & "").Value = _
    r.Range("B" & i + C_i & ":B" & i + C_i & "").Value
        rr.Range("B" & i + C_i - 1 & ":P" & i + C_i - 1 & "").Value = LnD_A
        rr.Range("Q" & i + C_i - 1 & ":Q" & i + C_i - 1 & "").Value = A
        rr.Range("BE" & i + C_i - 1 & "").Value = PFMc(15) * 100
        rr.Range("BF" & i + C_i - 1 & "").Value = PFMo(15) * 100
        
        'Calculate ln(D)-A
        For j = 1 To 15
            If DREE(j) > 0 Then
                DREE(j) = Log(DREE(j)) - A
                LnD_A(j) = DREE(j)
            Else
                LnD_A(j) = ""
            End If
            'DREE(6) = 0
            'LnD_A(6) = ""
            LnD_A2(j) = LnD_A(j)
            If rr.Cells(i + C_i - 1, j + 2).Font.Strikethrough Or rr.Cells(i + C_i - 1, j + 17).Font.Strikethrough _
            Or rr.Cells(i + C_i - 1, j + 32).Font.Strikethrough Then
                LnD_A2(j) = ""
            End If
        Next j
        rr.Range("R" & i + C_i - 1 & ":AF" & i + C_i - 1 & "").Value = LnD_A
        rr.Range("AG" & i + C_i - 1 & ":AU" & i + C_i - 1 & "").Value = B3
        
        T = MyRobustEst(LnD_A2, Br, kk)    ' Perform robust regression with Tukey's biweight (kk = 2)
        'T = MyLinEst(LnD_A2, Br)    ' Perform least square regresion.

        'If rr.Range("BD" & i + C_i - 1 & "").Value = "" Then
        '    rr.Range("BD" & i + C_i - 1 & "").Value = True
        '    T = MyRobustEst(LnD_A2, Br, kk)    ' Perform robust regression with Tukey's biweight (kk = 2)
        'End If
        
        'MsgBox LnD_A2(2)
        If rr.Range("BD" & i + C_i - 1 & "").Value = "" Then
            rr.Range("BD" & i + C_i - 1 & "").Value = True
            'MsgBox LnD_A2(2)
            T = MyRobustEst(LnD_A2, Br, kk)    ' Perform robust regression with Tukey's biweight (kk = 2)
            'tmp = MyLinEst(LnD_A2, Br)
            'If T(1) = tmp(1) Then rr.Range("BD" & i + C_i - 1 & "").Value = False
        End If
        
        If rr.Range("BD" & i + C_i - 1 & "").Value = False Then
            T = MyLinEst(LnD_A2, Br)    ' Perform least square regresion.
        End If
               
        rr.Range("AW" & i + C_i - 1 & ":AW" & i + C_i - 1 & "").Value = T(1) - 273.15
        rr.Range("AX" & i + C_i - 1 & ":AX" & i + C_i - 1 & "").Value = T(2)
        rr.Range("AY" & i + C_i - 1 & ":AY" & i + C_i - 1 & "").Value = T_BKN2px - 273.15
        
        r.Range("C" & i + C_i & "").Value = T(1) - 273.15
        r.Range("D" & i + C_i & "").Value = T(2)
        r.Range("E" & i + C_i & "").Value = T_BKN2px - 273.15
        
        If PFMo(15) < 0.7 Or PFMc(15) < 0.54 Then
            rr.Range("BF" & i + C_i - 1 & "").Interior.ColorIndex = 22
            rr.Range("BF" & i + C_i - 1 & "").Font.ColorIndex = 3
            rr.Range("BE" & i + C_i - 1 & "").Interior.ColorIndex = 22
            rr.Range("BE" & i + C_i - 1 & "").Font.ColorIndex = 3
            rr.Range("BG" & i + C_i - 1 & "").Value = False
            rr.Range("BG" & i + C_i - 1 & "").Interior.ColorIndex = 22
            rr.Range("BG" & i + C_i - 1 & "").Font.ColorIndex = 3
            r.Range("C" & i + C_i & "").Font.Strikethrough = True
            r.Range("D" & i + C_i & "").Font.Strikethrough = True
            
            r.Range("C" & i + C_i & "").Interior.ColorIndex = 22
            r.Range("D" & i + C_i & "").Interior.ColorIndex = 22
            r.Range("C" & i + C_i & "").Font.ColorIndex = 3
            r.Range("D" & i + C_i & "").Font.ColorIndex = 3
            
            rr.Range("AW" & i + C_i - 1 & "").Font.Strikethrough = True
            rr.Range("AX" & i + C_i - 1 & "").Font.Strikethrough = True
            
            rr.Range("AW" & i + C_i - 1 & "").Interior.ColorIndex = 22
            rr.Range("AX" & i + C_i - 1 & "").Interior.ColorIndex = 22
            rr.Range("AX" & i + C_i - 1 & "").Font.ColorIndex = 3
            rr.Range("AW" & i + C_i - 1 & "").Font.ColorIndex = 3
            Cali_i = 1
        Else
            rr.Range("BF" & i + C_i - 1 & "").Interior.ColorIndex = 2
            rr.Range("BF" & i + C_i - 1 & "").Font.ColorIndex = 1
            rr.Range("BE" & i + C_i - 1 & "").Interior.ColorIndex = 2
            rr.Range("BE" & i + C_i - 1 & "").Font.ColorIndex = 1
            rr.Range("BG" & i + C_i - 1 & "").Value = True
            rr.Range("BG" & i + C_i - 1 & "").Interior.ColorIndex = 2
            rr.Range("BG" & i + C_i - 1 & "").Font.ColorIndex = 1
            r.Range("C" & i + C_i & "").Font.Strikethrough = False
            r.Range("D" & i + C_i & "").Font.Strikethrough = False
            
            r.Range("C" & i + C_i & "").Interior.ColorIndex = 6
            r.Range("D" & i + C_i & "").Font.ColorIndex = 1
            r.Range("D" & i + C_i & "").Interior.ColorIndex = 6
            r.Range("C" & i + C_i & "").Font.ColorIndex = 1
            
            rr.Range("AW" & i + C_i - 1 & "").Font.Strikethrough = False
            rr.Range("AX" & i + C_i - 1 & "").Font.Strikethrough = False
            
            rr.Range("AW" & i + C_i - 1 & "").Interior.ColorIndex = 6
            rr.Range("AX" & i + C_i - 1 & "").Interior.ColorIndex = 6
            rr.Range("AX" & i + C_i - 1 & "").Font.ColorIndex = 1
            rr.Range("AW" & i + C_i - 1 & "").Font.ColorIndex = 1
        End If
    Next i

    With rr.Range("B3:P" & RN + 2 & "")
        .NumberFormat = "0.0000"
        .Font.ColorIndex = 1
        .HorizontalAlignment = xlCenter
        With .Interior
            .ColorIndex = 19
            .Pattern = xlSolid
        End With
    End With

    With rr.Range("Q3:AU" & RN + 2 & "")
        .NumberFormat = "0.00"
        .Font.ColorIndex = 1
        .HorizontalAlignment = xlCenter
        With .Interior
            .ColorIndex = 34
            .Pattern = xlSolid
        End With
    End With
    rr.Range("AW3:BA" & RN + 2 & "").NumberFormat = "0"
    rr.Range("BE3:BF" & RN + 2 & "").NumberFormat = "0"
    rr.Range("BE3:BF" & RN + 2 & "").HorizontalAlignment = xlCenter
    
    With rr.Range("AW3:AZ" & RN + 2 & "")
        .NumberFormat = "0"
        .HorizontalAlignment = xlCenter
        '.Font.ColorIndex = 1
        'With .Interior
        '    .ColorIndex = 6
        '    .Pattern = xlSolid
        'End With
    End With
    
    rr.Range("BB3:BB" & RN + 2 & "").HorizontalAlignment = xlCenter
    rr.Columns("A:BB").EntireColumn.AutoFit
    
    With r.Range("C4:E" & RN + 3 & "")
        .NumberFormat = "0"
        '.Font.ColorIndex = 1
        .HorizontalAlignment = xlCenter
        '.VerticalAlignment = xlCenter
        'With .Interior
        '    .ColorIndex = 6
        '    .Pattern = xlSolid
        'End With
    End With
    
    'If Cali_i = 1 Then
    '    MsgBox "WARNING!!!" & vbNewLine & _
    '    "The Mg# of some samples are out of the calibration range (opx: Mg# > 70; cpx: Mg# > 54)!" & vbCrLf & vbCrLf & _
    '    "T(REE) of these samples are highlighted!"
    'End If

    'r.Columns("B:D").EntireColumn.AutoFit

End Sub

Private Function T_BKN_2px(Mc, Mo, Pre)
    Dim FeN_c, FeN_o, KD As Double
    'PFM = SiIV, AlIV, TiIV, AlVI, TiVI, CrVI, MgVI, FeVI, MgM2, FeM2, MnM2, CaM2, NaM2, KM2, MgN
    FeN_c = 1 - Mc(15)
    FeN_o = 1 - Mo(15)
    KD = (1 - Mc(12) / (1 - Mc(13))) / (1 - Mo(12) / (1 - Mo(13)))
    T_BKN_2px = (23664 + (24.9 + 126.3 * FeN_c) * Pre * 10) / (13.38 + Log(KD) ^ 2 + 11.59 * FeN_o)
End Function


Private Function PyxForm(Major)
    'Dim Cat_T() As Variant
    Dim i, ln As Integer
    Dim O_factor As Double
    Dim O, SiO2, TiO2, Al2O3, Cr2O3, FeO, MnO, MgO, CaO, Na2O, K2O As Double
    O = 15.9994
    SiO2 = 28.0855 + O * 2
    TiO2 = 47.867 + O * 2
    Al2O3 = 26.9815 * 2 + O * 3
    Cr2O3 = 51.9961 * 2 + O * 3
    Fe2O3 = 55.845 * 2 + O * 3
    FeO = 55.845 + O
    MnO = 54.938 + O
    MgO = 24.305 + O
    CaO = 40.078 + O
    Na2O = 22.9898 * 2 + O
    K2O = 39.0983 * 2 + O
    mol_wt = Array(SiO2, TiO2, Al2O3, Cr2O3, FeO, MnO, MgO, CaO, Na2O, K2O)
    Cat_n = Array(1, 1, 2, 2, 1, 1, 1, 1, 2, 2)
    Ano_n = Array(2, 2, 3, 3, 1, 1, 1, 1, 1, 1)
    'Major = Array(51.6, 0.4, 4.8, 2.1, 0, 0, 16.4, 24.5, 0, 0)
    ln = UBound(mol_wt)
    For i = 1 To ln
        Major(i) = Major(i) / mol_wt(i) * Ano_n(i) ' Calculate oxygen mol
    Next i
    O_factor = 6 / WorksheetFunction.Sum(Major)
    Cat_T = Major
    For i = 1 To ln
        Cat_T(i) = Major(i) * O_factor / Ano_n(i) * Cat_n(i)
    Next i
    ' Assign cations to different sites in pyroxene
    SiIV = Cat_T(1)
    Ti = Cat_T(2)
    Al = Cat_T(3)
    CrVI = Cat_T(4)
    Fe = Cat_T(5)
    MnM2 = Cat_T(6)
    Mg = Cat_T(7)
    CaM2 = Cat_T(8)
    NaM2 = Cat_T(9)
    KM2 = Cat_T(10)
    ' T = Si-Al-Ti
    AlIV = 0
    AlVI = 0
    TiIV = 0
    TiVI = 0
    If SiIV < 2 And Al > 2 - SiIV Then
        AlIV = 2 - SiIV
        AlVI = Al - AlIV
    ElseIf Al <= 2 - SiIV Then
        AlIV = Al
        AlVI = 0
        If Ti > 2 - SiIV - Al Then
            TiIV = 2 - SiIV - Al
            TiVI = Ti - TiIV
        End If
    End If
    MgN = Mg / (Mg + Fe)
    MgM2 = 0
    FeM2 = 0
    M2_t = CaM2 + NaM2 + KM2 + MnM2
    
    If Mg > 0 Then
        R_Fe_Mg = Fe / Mg
        If M2_t <= 1 Then
            MgM2 = (1 - M2_t) / (1 + R_Fe_Mg)
            FeM2 = MgM2 * R_Fe_Mg
        End If
        MgVI = Mg - MgM2
        FeVI = Fe - FeM2
    ElseIf Mg = 0 Then
        FeM2 = 1 - M2_t
        MgVI = 0
        FeVI = Fe - FeM2
    End If
    
    PyxForm = Array(SiIV, AlIV, TiIV, AlVI, TiVI, CrVI, MgVI, FeVI, MgM2, FeM2, MnM2, CaM2, NaM2, KM2, MgN)
    'MsgBox PyxForm0(15)
End Function
