Attribute VB_Name = "Module2"
Public Function fun_Reg_Plot(SN, S_ID)
    Dim X_Data(15), Y_Data(15), XX_Data(15), YY_Data(15), XL_Data(2), YL_Data(2), mychart As Variant
    Dim rr, r, bm, b_sd, REE_name, TBKN, tmp1, tmp2, tmp As Variant
    Dim RN, flag_2i, j, i, Yid As Integer

    Set rr = Worksheets("Results")
    Set r = Worksheets("Input data")
    'rr.Activate
    'ActiveWindow.DisplayGridlines = False
    RN = Application.CountA(r.Range("K:K"))
    Lst_Idx = S_ID + 3
    
    XL_Data(1) = 0
    YL_Data(1) = 0
    
    'X_Data = rr.Range("R" & Lst_Idx & ":AF" & Lst_Idx & "")
    'Y_Data = rr.Range("AG" & Lst_Idx & ":AU" & Lst_Idx & "")
    'MsgBox X_Data(1)
    flag_2i = 1
    For j = 1 To 15
        X_Data(j) = rr.Cells(Lst_Idx, j + 17).Value
        Y_Data(j) = rr.Cells(Lst_Idx, j + 32).Value
        XX_Data(j) = X_Data(j)
        YY_Data(j) = Y_Data(j)
        If (rr.Cells(Lst_Idx, j + 17).Font.Strikethrough And rr.Cells(Lst_Idx, j + 17).Value <> "") Or _
            (rr.Cells(Lst_Idx, j + 17).Font.Strikethrough And rr.Cells(Lst_Idx, j + 17).Value <> "") Or _
            (rr.Cells(Lst_Idx, j + 32).Font.Strikethrough And rr.Cells(Lst_Idx, j + 32).Value <> "") Then
            YY_Data(j) = Empty
            XX_Data(j) = Empty
            flag_2i = 2
        End If
    Next j
    'XL_Data(2) = Application.WorksheetFunction.Min(X_Data) * 1.3
    XL_Data(2) = -10
    'MsgBox Str(XL_Data(2))
    bm = rr.Cells(Lst_Idx, 49).Value
    b_sd = rr.Cells(Lst_Idx, 50).Value
    TBKN = rr.Cells(Lst_Idx, 51).Value
    'bm = MyLinEst(XX_Data, YY_Data) - 273.15
    YL_Data(2) = XL_Data(2) * (bm + 273.15) * 0.001
    
    If Charts.Count = 0 Then
        ActiveWorkbook.Charts.Add After:=Worksheets(Worksheets.Count)
        'Charts.Add After:=Worksheets(Worksheets.Count)
        ActiveChart.Name = "iPlot"
    Else
        Yid = 0
        For j = 1 To Charts.Count
            If Charts(j).Name = "iPlot" Then Yid = j
        Next j
        If Yid > 0 Then Charts("iPlot").Select
        If Yid = 0 Then
            ActiveWorkbook.Charts.Add After:=Worksheets(Worksheets.Count)
            'Charts.Add After:=Worksheets(Worksheets.Count)
            ActiveChart.Name = "iPlot"
        End If
    End If
    
    ActiveChart.ChartType = xlXYScatter
    Do While ActiveChart.SeriesCollection.Count > 0
        ActiveChart.SeriesCollection(1).Delete
    Loop
    
    'If ActiveChart.Shapes.Count > 0 Then
    '    ActiveChart.Shapes.SelectAll
    '    Selection.Delete
    'End If
    
    'ActiveChart.Shapes.AddTextbox(msoTextOrientationHorizontal, 370, 320, 170, 55). _
    'TextFrame.Characters.Text = "T(REE) = " & CInt(bm) & "" & ChrW(177) & _
        CInt(b_sd) & " " & ChrW(176) & "C" & vbCrLf & "T(BKN) = " & CInt(TBKN) & " " & ChrW(176) & "C"
    'With ActiveChart.Shapes(1).TextEffect
    '    .FontSize = 16
    '    .FontBold = True
    'End With
            
    ActiveChart.SeriesCollection.NewSeries
    ActiveChart.SeriesCollection.NewSeries
    ActiveChart.SeriesCollection.NewSeries
    
    With ActiveChart.SeriesCollection(1)
        If Val(Application.Version) >= 12 Then
            .Name = "Sample: " & SN & " [Excluded]"
            .Values = Y_Data
            .XValues = X_Data
        Else
            MsgBox "Please use a newer version of EXCEL."
            End
        End If
        .Border.LineStyle = xlNone
        .MarkerStyle = xlCircle
        .MarkerSize = 12
        .MarkerBackgroundColorIndex = 46
        .MarkerForegroundColorIndex = 1
        .Shadow = False
    End With
    
    For j = 1 To 15
        ActiveChart.SeriesCollection(1).Points(j + 1).HasDataLabel = True
        If IsNumeric(X_Data(j)) Then
            ActiveChart.SeriesCollection(1).Points(j + 1).DataLabel.Text = _
                rr.Cells(2, j + 17).Value
            ActiveChart.SeriesCollection(1).Points(j + 1).DataLabel.Font.Size = 14
        End If
    Next j
    
    With ActiveChart.SeriesCollection(2)
        'If .Count = 1 Then .NewSeries
        If Val(Application.Version) >= 12 Then
            .Name = "Sample: " & SN & " [Included]"
            .Values = YY_Data
            .XValues = XX_Data
        End If
        .Border.LineStyle = xlNone
        .MarkerStyle = xlCircle
        .MarkerSize = 12
        .MarkerBackgroundColorIndex = 36
        .MarkerForegroundColorIndex = 1
        .Shadow = False
    End With
    
    With ActiveChart.SeriesCollection(3)
        'If .Count = 2 Then .NewSeries
        If Val(Application.Version) >= 12 Then
            .Name = "Linear regression"
            .Values = YL_Data
            .XValues = XL_Data
        Else
            '.Select
            Names.Add "_", XL_Data
            ExecuteExcel4Macro "series.XL_Data(!_)"
            Names.Add "_", YL_Data
            ExecuteExcel4Macro "series.YL_Data(,!_)"
            Names("_").Delete
        End If
        .Border.LineStyle = xllinestyleEn
        .Format.Line.Weight = 5.5
        '.Border.Weight = xlThick
        .Border.ColorIndex = 5
        .MarkerStyle = xlNone
        .Shadow = False
    End With
    
    'If flag_2i = 1 Then
    '    ActiveChart.Legend.LegendEntries(1).Delete
    'End If
    
    ActiveSheet.Tab.ColorIndex = 3
    
    With ActiveChart.PlotArea
        .Width = 370
        .Height = 350
        .Top = 55
        .Left = 165
        .Border.LineStyle = xllinestyleEn
        .Format.Line.Weight = 2
    End With
    
    ActiveChart.ChartArea.Border.LineStyle = xlNone
    
    With ActiveChart.Legend
        .Font.Size = 16
        .Left = 215
        .Top = 80
    End With
    
    ActiveChart.HasTitle = True
    tmp1 = "T(REE) = " & CInt(bm) & "" & ChrW(177) & CInt(b_sd) & " " & ChrW(176) & "C" & ";  "
    tmp2 = "T(BKN) = " & CInt(TBKN) & " " & ChrW(176) & "C"
    tmp = Len(tmp1)
    With ActiveChart.ChartTitle
        .AutoScaleFont = False
        .Top = 35
        .Left = 200
        .Text = tmp1 & tmp2
        .Characters.Font.Size = 18
        .Characters.Font.Bold = True
        .Characters.Font.Name = "Times New Roman"
        '.Characters(2, 3).Font.Subscript = True
        '.Characters(tmp + 2, 3).Font.Subscript = True
    End With
    'ActiveChart.ChartTitle.Characters(2, 3).Font.Subscript = True
    'ActiveChart.ChartTitle.Characters(tmp + 2, 3).Font.Subscript = True
    
    With ActiveChart.Axes(xlValue)
        .TickLabelPosition = xlTickLabelPositionNextToAxis ' xlTickLabelPositionHigh
        .MinorTickMark = xlTickMarkInside
        .MajorTickMark = xlTickMarkInside
        .HasMajorGridlines = False
        .HasMinorGridlines = False
            .Border.LineStyle = xllinestyleEn
            .Format.Line.Weight = 2
        .TickLabels.Font.Size = 16
        .HasTitle = True
        .AxisTitle.Caption = "B/1000"
        .AxisTitle.Font.Size = 20
        .AxisTitle.Font.Name = "Times New Roman"
        .AxisTitle.Font.Bold = True
        .AxisTitle.Left = 120
        .CrossesAt = -13
        .MinimumScale = -13
        .MaximumScale = 0
    End With
    
    With ActiveChart.Axes(xlCategory)
        .TickLabelPosition = xlTickLabelPositionNextToAxis ' xlTickLabelPositionHigh
        .MajorTickMark = xlTickMarkInside
        .MinorTickMark = xlTickMarkInside
            .Border.LineStyle = xllinestyleEn
            .Format.Line.Weight = 2
        .TickLabels.Font.Size = 16
        .HasTitle = True
        .AxisTitle.Caption = "ln(D)-A"
        .AxisTitle.Font.Size = 20
        .AxisTitle.Font.Name = "Times New Roman"
        .AxisTitle.Font.Bold = True
        .AxisTitle.Top = 420
        .AxisTitle.Left = 320
        .CrossesAt = -10
        .MinimumScale = -10
        .MaximumScale = 0
    End With
    
End Function

Public Function MyLinEst(MyVariantX, MyVariantY)
    'Calculate T in Kelvin
    Dim CountNonBlank2 As Integer
    Dim Slope_Int, b_std(2) As Variant
    Dim NewX(), NewY(), NewXX(), NewYY(), tmp, Sxx, SSE As Double
    CountNonBlank2 = Application.Count(MyVariantX) + 1
    
    If CountNonBlank2 = 1 Then
        MsgBox "WARNING!!!" & vbNewLine & "No data available for regression!"
        End
    End If
    
    'MsgBox Str(CountNonBlank2)
    ReDim NewX(CountNonBlank2), NewY(CountNonBlank2)
    ReDim NewXX(CountNonBlank2), NewYY(CountNonBlank2)
    Dim i, j As Integer
    i = 1
    For j = 1 To 15
        If IsNumeric(MyVariantX(j)) Then
            NewX(i) = MyVariantX(j)
            NewY(i) = MyVariantY(j)
            i = i + 1
        End If
    Next j
    NewX(i) = 0
    NewY(i) = 0
    'Slope_Int = Application.LinEst(NewY, NewX, False, False)
    'MyLinEst = Slope_Int(1)
    'Linear least-square regression with zero intercept
    tmp = 0
    For j = 1 To CountNonBlank2
        NewYY(j) = NewX(j) * NewY(j)
        NewXX(j) = NewX(j) * NewX(j)
        tmp = tmp + NewXX(j)
    Next j
    b_std(1) = WorksheetFunction.Average(NewYY) / WorksheetFunction.Average(NewXX)
    
    SSE = 0
    For j = 1 To CountNonBlank2
        SSE = SSE + (NewY(j) - b_std(1) * NewX(j)) ^ 2
    Next j
    b_std(2) = (SSE / (CountNonBlank2 - 1) / tmp) ^ 0.5
    MyLinEst = b_std
End Function
Public Function MyRobustEst(MyVariantX, MyVariantY, km)
    'Calculate T in Kelvin
    Dim CountNonBlank2, CountNonBlank1 As Integer
    Dim Slope_Int, b0, b1, b2, T_std, SSE, T_op(2) As Variant
    Dim NewX(), NewY(), NewXX(), NewYY(), NewXXX(), NewYYY(), bn(), tmp, s_tmp, x1, x2 As Double
    CountNonBlank1 = 15
    CountNonBlank2 = Application.Count(MyVariantX) + 1
    'MsgBox Str(CountNonBlank2)
    ReDim NewX(CountNonBlank2), NewY(CountNonBlank2), NewXX(CountNonBlank2), NewYY(CountNonBlank2)
    ReDim bn(CountNonBlank2)
    Dim i, j As Integer
    
    If CountNonBlank2 = 1 Then
        MsgBox "WARNING!!!" & vbNewLine & "No data available for inversion!"
        End
    End If
        
    i = 1
    For j = 1 To CountNonBlank1
        If IsNumeric(MyVariantX(j)) Then
            NewX(i) = MyVariantX(j)
            NewY(i) = MyVariantY(j)
            'MsgBox MyVariantX(j)
            bn(i) = NewY(i) / NewX(i)
            i = i + 1
        Else
            'NewX(i) = 0
            'NewY(i) = 0
        End If
        'i = i + 1
    Next j
    
    NewX(i) = 0
    NewY(i) = 0

    'Linear least-square regression with zero intercept
    For j = 1 To CountNonBlank2
        NewYY(j) = NewX(j) * NewY(j)
        NewXX(j) = NewX(j) * NewX(j)
    Next j
    b0 = WorksheetFunction.Average(NewYY) / WorksheetFunction.Average(NewXX)

    tmp = MyLinEst(MyVariantX, MyVariantY)
    b0 = tmp(1)
    
    b0 = WorksheetFunction.Median(NewY) / WorksheetFunction.Median(NewX)
    
    b1 = b0
    b2 = 0
'MsgBox CountNonBlank2 & "-" & UBound(NewX)
    SSE = 0
    i = 0
    Do
        'MsgBox b1 - 273.15
        T_std = ff(NewX, NewY, km, b1)
        b2 = T_std(1)
        If Abs(b2 - b1) < 0.01 Or i > 200 Then
            Exit Do
        Else
            b1 = b2
        End If
        i = i + 1
    Loop
    If i > 200 Then T_std = ff(NewX, NewY, km, (b1 + b2) / 2)
    T_op(1) = T_std(1)
    T_op(2) = T_std(2)
    MyRobustEst = T_op
    If b2 = b0 Then MyRobustEst = MyLinEst(MyVariantX, MyVariantY)
End Function
Public Function ff(XX, YY, kc, bc)
Dim T(2), MAD, RSD, tiny_s, adj_f As Variant
Dim Ya, Xa, s_tmp, tmp, SSE2, SSE_2, Sxx, T_sd, wx, wxx As Double
Dim j As Integer
Dim epsilon As Double

'epsilon = 0.001
adj_f = 1 / (1 - 0.9999) ^ 0.5

RSD = XX
    s_tmp = 0
    Ya = 0
    Xa = 0
    SSE_2 = 0
    Sxx = 0
    MAD = 0 ' median absolute deviation
        
    For j = 1 To Application.Count(XX)
        RSD(j) = adj_f * (YY(j) - XX(j) * bc)
    Next j

    For j = 1 To Application.Count(XX)
        RSD(j) = Abs(RSD(j) - WorksheetFunction.Median(RSD))
    Next j

    SSE = WorksheetFunction.Median(RSD) / 0.6745
    tiny_s = 1e-06 * WorksheetFunction.StDev(YY)
    If tiny_s = 0 Then tiny_s = 1
    SSE = WorksheetFunction.Max(SSE, tiny_s)
    
    wx = 0
    wxx = 0
    For j = 1 To Application.Count(XX)
        tmp = (YY(j) - XX(j) * bc) * adj_f
        If Abs(tmp) <= SSE * kc Then
            s_tmp = (1 - (tmp / SSE / kc) ^ 2) ^ 2
            SSE_2 = SSE_2 + (YY(j) - XX(j) * bc) ^ 2
            Sxx = Sxx + XX(j) * XX(j)
            wx = wx + Abs(s_tmp * XX(j))
            wxx = wxx + (s_tmp * XX(j)) ^ 2
        Else
            s_tmp = 0
        End If
        
        Ya = Ya + s_tmp * XX(j) * YY(j)
        Xa = Xa + s_tmp * XX(j) * XX(j)
        
    Next j
    
    'T_sd = wx / wxx * (SSE_2 / (Application.Count(XX))) ^ 0.5
    ''T_sd = (SSE_2 / (Application.Count(XX) - 2) / Sxx) ^ 0.5
    'T(1) = Ya / Xa
    'T(2) = T_sd
    'ff = T

    If wxx > 0 Then
        T_sd = wx / wxx * (SSE_2 / (Application.Count(XX))) ^ 0.5
        T(1) = Ya / Xa
        T(2) = T_sd
    Else
        T(1) = bc
        T(2) = 0
    End If
    ff = T

End Function
