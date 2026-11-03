[CmdletBinding()]
param(
    [string]$TranscriptPath = '.\VBL-INPUT-RAW.md',
    [string]$WorkingCopyPath
)
$ErrorActionPreference = 'Stop'

$source = [IO.Path]::GetFullPath($TranscriptPath)
if (-not $WorkingCopyPath) {
    $directory = [IO.Path]::GetDirectoryName($source)
    $stem = [IO.Path]::GetFileNameWithoutExtension($source)
    $extension = [IO.Path]::GetExtension($source)
    $WorkingCopyPath = Join-Path $directory ($stem + '.working' + $extension)
}
$working = [IO.Path]::GetFullPath($WorkingCopyPath)
$sourceDir = [IO.Path]::GetDirectoryName($source)
$workingDir = [IO.Path]::GetDirectoryName($working)
if (-not (Test-Path -LiteralPath $sourceDir -PathType Container)) {
    throw "Transcript directory does not exist: $sourceDir"
}
if (-not (Test-Path -LiteralPath $workingDir -PathType Container)) {
    throw "Working-copy directory does not exist: $workingDir"
}

if (-not (Test-Path -LiteralPath $source)) {
    $stream = [IO.File]::Open($source, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $stream.Dispose()
    Write-Warning "Created an empty placeholder only. It is not evidence until you add and verify source material: $source"
}
if (Test-Path -LiteralPath $source -PathType Container) {
    throw "Transcript path is a directory: $source"
}
if (Test-Path -LiteralPath $working) {
    throw "Refusing to overwrite an existing working copy: $working"
}

Copy-Item -LiteralPath $source -Destination $working
$sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
$workingHash = (Get-FileHash -LiteralPath $working -Algorithm SHA256).Hash.ToLowerInvariant()
if ($sourceHash -ne $workingHash) {
    throw 'Working-copy SHA-256 differs from source; do not edit either file until investigated.'
}
Write-Output "Source SHA-256: $sourceHash"
Write-Output "Working copy: $working"
Write-Output 'Edit only the working copy; preserve the source file.'
Start-Process -FilePath 'notepad.exe' -ArgumentList ('"{0}"' -f $working)