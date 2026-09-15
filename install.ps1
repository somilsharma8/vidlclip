#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallRoot = Join-Path $env:LOCALAPPDATA "vidclip"
$VenvDir = Join-Path $InstallRoot "venv"
$BinDir = Join-Path $InstallRoot "bin"

function Find-Python {
    foreach ($name in @("py", "python")) {
        $cmd = Get-Command $name -ErrorAction SilentlyContinue
        if (-not $cmd) { continue }
        if ($name -eq "py") {
            try {
                $ver = & py -3 -c "import sys; print(sys.version_info[:2] >= (3, 10))"
                if ($ver -eq "True") { return @("py", "-3") }
            } catch { }
        } else {
            try {
                $ver = & python -c "import sys; print(sys.version_info[:2] >= (3, 10))"
                if ($ver -eq "True") { return @("python") }
            } catch { }
        }
    }
    return $null
}

$python = Find-Python
if (-not $python) {
    Write-Host "Python 3.10+ is required."
    Write-Host "Install it with:"
    Write-Host "  winget install -e --id Python.Python.3.12"
    Write-Host "Then close this window, open a new terminal, and run install.ps1 again."
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        $answer = Read-Host "Install Python 3.12 with winget now? [Y/n]"
        if ($answer -notmatch "^[Nn]") {
            winget install -e --id Python.Python.3.12
            Write-Host "Re-open a new PowerShell window and run install.ps1 again so PATH updates."
        }
    }
    exit 1
}

Write-Host "Installing vidclip for this Windows user..."
New-Item -ItemType Directory -Force -Path $InstallRoot, $BinDir | Out-Null

$pythonExe = $python[0]
$pythonArgs = @()
if ($python.Length -gt 1) { $pythonArgs = $python[1..($python.Length - 1)] }

& $pythonExe @pythonArgs -m venv $VenvDir
$pip = Join-Path $VenvDir "Scripts\python.exe"
& $pip -m pip install -U pip
& $pip -m pip install --upgrade $RepoRoot

$shim = Join-Path $BinDir "vidclip.cmd"
@"
@echo off
"$VenvDir\Scripts\vidclip.exe" %*
"@ | Set-Content -Path $shim -Encoding ASCII

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not $userPath) { $userPath = "" }
if ($userPath -notlike "*$BinDir*") {
    $newPath = if ($userPath) { "$userPath;$BinDir" } else { $BinDir }
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    $env:Path = "$BinDir;$env:Path"
    Write-Host "Added $BinDir to your user PATH."
}

Write-Host ""
Write-Host "Installed. Open a NEW terminal, then run:"
Write-Host "  vidclip doctor"
Write-Host "  vidclip"
Write-Host "  vidclip `"https://www.youtube.com/watch?v=VIDEO_ID`""
