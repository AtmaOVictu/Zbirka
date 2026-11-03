[CmdletBinding()]
param(
    [Parameter(Mandatory=$true, Position=0)][string]$LeftPath,
    [Parameter(Mandatory=$true, Position=1)][string]$RightPath
)
$ErrorActionPreference = 'Stop'
$left = (Resolve-Path -LiteralPath $LeftPath).Path
$right = (Resolve-Path -LiteralPath $RightPath).Path
if (-not (Test-Path -LiteralPath $left -PathType Leaf)) { throw "Left path is not a file: $left" }
if (-not (Test-Path -LiteralPath $right -PathType Leaf)) { throw "Right path is not a file: $right" }
$li = Get-Item -LiteralPath $left
$ri = Get-Item -LiteralPath $right
$lh = (Get-FileHash -LiteralPath $left -Algorithm SHA256).Hash.ToLowerInvariant()
$rh = (Get-FileHash -LiteralPath $right -Algorithm SHA256).Hash.ToLowerInvariant()
$byteEqual = $false
if ($li.Length -eq $ri.Length) {
    $a = [System.IO.File]::OpenRead($left)
    $b = [System.IO.File]::OpenRead($right)
    try {
        $bufA = New-Object byte[] 65536
        $bufB = New-Object byte[] 65536
        $byteEqual = $true
        while ($true) {
            $na = $a.Read($bufA, 0, $bufA.Length)
            $nb = $b.Read($bufB, 0, $bufB.Length)
            if ($na -ne $nb) { $byteEqual = $false; break }
            if ($na -eq 0) { break }
            for ($i = 0; $i -lt $na; $i++) {
                if ($bufA[$i] -ne $bufB[$i]) { $byteEqual = $false; break }
            }
            if (-not $byteEqual) { break }
        }
    } finally { $a.Dispose(); $b.Dispose() }
}
[pscustomobject]@{
    left_path = $left
    right_path = $right
    left_bytes = $li.Length
    right_bytes = $ri.Length
    left_sha256 = $lh
    right_sha256 = $rh
    size_equal = ($li.Length -eq $ri.Length)
    hash_equal = ($lh -eq $rh)
    byte_identical = $byteEqual
    status = if ($byteEqual) { 'PASS_BYTE_IDENTICAL' } else { 'FAIL_NOT_BYTE_IDENTICAL' }
    limitation = 'This comparison does not establish authorship, provenance, meaning, publication history, permissions, or legal validity.'
} | ConvertTo-Json -Depth 4
