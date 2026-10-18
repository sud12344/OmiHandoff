Attribute VB_Name = "OMi_ThreadState"
' OMi_ThreadState - set the resting state of every master in 11_MASTERS without rebuilding it.
'   SuppressThreads_AllMasters   : every THD_* feature suppressed in EVERY configuration, part saved  (project resting state)
'   UnsuppressThreads_AllMasters : the reverse (only for a look; the drawing macros do this themselves per view and put it back)
' Run with SolidWorks open and no documents open. Writes 03_SCRIPTS\ThreadState_report.txt.
Option Explicit
Const MASTER_DIR As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\11_MASTERS\"
Const REPORT_PATH As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\03_SCRIPTS\ThreadState_report.txt"
Const THREAD_PREFIX As String = "THD_"
Dim fnRep As Integer

Sub SuppressThreads_AllMasters()
    SetAll True
End Sub

Sub UnsuppressThreads_AllMasters()
    SetAll False
End Sub

Private Sub SetAll(suppress As Boolean)
    Dim swApp As SldWorks.SldWorks, swModel As SldWorks.ModelDoc2, f As String, e As Long, w As Long, n As Long, nParts As Long
    Set swApp = Application.SldWorks
    fnRep = FreeFile: Open REPORT_PATH For Output As #fnRep
    Print #fnRep, "OMi_ThreadState " & IIf(suppress, "SUPPRESS", "UNSUPPRESS") & "  " & Now
    f = Dir(MASTER_DIR & "*.SLDPRT")
    Do While f <> ""
        If Left(f, 1) <> "~" Then
            Set swModel = swApp.OpenDoc6(MASTER_DIR & f, swDocumentTypes_e.swDocPART, swOpenDocOptions_e.swOpenDocOptions_Silent, "", e, w)
            If swModel Is Nothing Then
                Print #fnRep, "FAIL  " & f & " could not be opened (error " & e & ")"
            Else
                n = SetThreads(swModel, suppress)
                swModel.ForceRebuild3 False
                Dim ok As Boolean: ok = swModel.Save3(swSaveAsOptions_e.swSaveAsOptions_Silent, e, w)
                Print #fnRep, IIf(ok, "OK    ", "FAIL  ") & f & ": " & n & " THD_ feature(s) " & IIf(suppress, "suppressed", "unsuppressed") & " in all configurations, saved=" & ok & IIf(ok, "", " (error " & e & ")")
                swApp.CloseDoc swModel.GetTitle
                nParts = nParts + 1
            End If
        End If
        f = Dir
    Loop
    Print #fnRep, nParts & " master(s) processed"
    Close #fnRep
    MsgBox nParts & " master(s) processed - see ThreadState_report.txt", vbInformation, "OMi_ThreadState"
End Sub

Private Function SetThreads(swModel As SldWorks.ModelDoc2, suppress As Boolean) As Long
    On Error Resume Next
    Dim ft As SldWorks.Feature, n As Long
    Set ft = swModel.FirstFeature
    Do While Not ft Is Nothing
        If Left(ft.Name, Len(THREAD_PREFIX)) = THREAD_PREFIX Then
            Dim act As Long, names As Variant, i As Long, st As Variant, live As Long
            act = IIf(suppress, swFeatureSuppressionAction_e.swSuppressFeature, swFeatureSuppressionAction_e.swUnSuppressFeature)
            ft.SetSuppression2 act, swInConfigurationOpts_e.swAllConfiguration, Empty
            names = swModel.GetConfigurationNames
            For i = LBound(names) To UBound(names)
                ft.SetSuppression2 act, swInConfigurationOpts_e.swSpecifyConfiguration, Array(names(i))
            Next i
            st = ft.IsSuppressed2(swInConfigurationOpts_e.swAllConfiguration, Empty)
            live = 0
            If IsArray(st) Then
                For i = LBound(st) To UBound(st)
                    If st(i) = Not suppress Then live = live + 1
                Next i
            End If
            Print #fnRep, "      " & ft.Name & ": " & IIf(suppress, "suppressed", "unsuppressed") & " in all configurations; " & live & " config(s) NOT in the requested state"
            n = n + 1
        End If
        Set ft = ft.GetNextFeature
    Loop
    SetThreads = n
End Function
