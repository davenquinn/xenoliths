Attribute VB_Name = "Module3"
Option Explicit
Public RNc As Integer
Public Pb_ID As Integer
' RNc is the row number of the sample, not the order of the sample
Sub Reg_Plot()
    Dim tmp As Variant
    If Not Application.OperatingSystem Like "*Mac*" Then
        If Val(Application.Version) < 11 Then
            tmp = MsgBox("WARNING!!!" & vbNewLine & _
            "Your Excel version is old. You probably would " & _
            "not be able to run this program. Do you still want to give a try?", vbOKCancel)
            If tmp = vbNo Then End
        End If
        UserForm1.Show False
    Else
        If Val(Application.Version) < 14 Then
            tmp = MsgBox("WARNING!!!" & vbNewLine & _
            "Your Excel version is old. You probably would " & _
            "not be able to run this program. Do you still want to give a try?", vbOKCancel)
            If tmp = vbNo Then End
        End If
        UserForm1.Show
    End If
    
End Sub

