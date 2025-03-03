' Create BROski desktop shortcut
Option Explicit

' Declare variables
Dim objWshShell, objShortcut, objFSO
Dim strDesktop, strAppPath, strWorkingDir, strIconLocation

' Create WScript Shell and FileSystemObject
Set objWshShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get desktop path and current directory
strDesktop = objWshShell.SpecialFolders("Desktop")
strWorkingDir = objWshShell.CurrentDirectory

' Set paths
strAppPath = strWorkingDir & "\BROSKI_QUICK_START.bat"
strIconLocation = strWorkingDir & "\favicon.ico"

' Check if the batch file exists
If Not objFSO.FileExists(strAppPath) Then
    WScript.Echo "Error: Cannot find the BROSKI_QUICK_START.bat file."
    WScript.Echo "Make sure you run this script from the BROski directory."
    WScript.Quit
End If

' Try to create the shortcut
On Error Resume Next
Set objShortcut = objWshShell.CreateShortcut(strDesktop & "\BROski Crypto Bot.lnk")

' Check for errors
If Err.Number <> 0 Then
    WScript.Echo "Error creating shortcut: " & Err.Description
    WScript.Echo "Try running this script as Administrator."
    WScript.Quit
End If

' Configure the shortcut
objShortcut.TargetPath = strAppPath
objShortcut.WorkingDirectory = strWorkingDir
objShortcut.Description = "BROski Crypto Trading Bot"
objShortcut.WindowStyle = 1  ' Normal window

' Set icon if it exists
If objFSO.FileExists(strIconLocation) Then
    objShortcut.IconLocation = strIconLocation
End If

' Save the shortcut
objShortcut.Save

' Check for errors when saving
If Err.Number <> 0 Then
    WScript.Echo "Error saving shortcut: " & Err.Description
    WScript.Echo "Try running this script as Administrator."
Else
    WScript.Echo "BROski shortcut created on your desktop!"
End If

' Clean up
Set objShortcut = Nothing
Set objWshShell = Nothing
Set objFSO = Nothing
