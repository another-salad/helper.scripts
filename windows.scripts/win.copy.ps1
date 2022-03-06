# Copies files from the source DIR to the destination, recursive is False by default
# Example:
#
#  To copy the files from the source DIR to the destination without copying sub-directories
#  win.copy.ps1 -source "C:\test\dir\here" -destination "D:\other\dir\here"
#
#  To copy the files and sub-directories from the source DIR to the destination
#  win.copy.ps1 -source "C:\test\dir\here" -destination "D:\other\dir\here" -recursive
#
# Robocopy is set to verbose, so all copy info is pumped into the terminal window
#
# To run this script, you may need to set the following execution policy (as MS loves policies....):
#  Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser

param ([string]$source, [string]$destination, [switch]$recursive)

function confirmationLog {
    $consoleLines = "---------------------------------------------------------------------------"
    Write-Host $consoleLines -ForegroundColor DarkGreen
    Write-Host " WinCopy - Read the following carefully before confirming:"
    Write-Host $consoleLines -ForegroundColor DarkGreen
    Write-Host " The source directory: $source"
    Write-Host " The destination directory: $destination"
    Write-Host " Copy all sub-directories (i.e recursive copy): $recursive"
    Write-Host $consoleLines -ForegroundColor DarkGreen
}

function copyItems ($source, $destination, $recursive) {
    # We want verbose output by default
    $cmdArgs = [System.Collections.ArrayList]@($source, $destination, "/v")
    if ($recursive) {
        $cmdArgs.Add("/e")
    }
    robocopy @cmdArgs
}

confirmationLog
$confirmation = Read-Host "Are you Sure You Want To Proceed (y/n)"
if ($confirmation -eq 'y') {
    copyItems $source $destination $recursive
} else {
    Write-Host " Cancelled. Nothing has been copied."
}