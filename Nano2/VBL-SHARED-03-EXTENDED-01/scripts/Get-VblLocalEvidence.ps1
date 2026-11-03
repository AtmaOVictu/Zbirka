[CmdletBinding()]
param(
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$TranscriptPath = '.\VBL-INPUT-RAW.md',
    [string]$ItemPath = '.\isti',
    [string]$OutputFile,
    [switch]$ReadWindowsTimeStatus
)
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath($ProjectRoot)
$transcript = if ([IO.Path]::IsPathRooted($TranscriptPath)) { [IO.Path]::GetFullPath($TranscriptPath) } else { [IO.Path]::GetFullPath((Join-Path $root $TranscriptPath)) }
$item = if ([IO.Path]::IsPathRooted($ItemPath)) { [IO.Path]::GetFullPath($ItemPath) } else { [IO.Path]::GetFullPath((Join-Path $root $ItemPath)) }
$now = Get-Date
$tz = Get-TimeZone
$gitText = @()
$gitExit = $null
$git = Get-Command git -ErrorAction SilentlyContinue
if ($git) {
    $gitText = @(& git -C $root status --short 2>&1 | ForEach-Object { [string]$_ })
    $gitExit = $LASTEXITCODE
}
$alias = Get-Alias ni -ErrorAction SilentlyContinue
$transcriptInfo = $null
if (Test-Path -LiteralPath $transcript -PathType Leaf) {
    $f = Get-Item -LiteralPath $transcript
    $transcriptInfo = [ordered]@{ path=$transcript; exists=$true; bytes=$f.Length; sha256=(Get-FileHash -LiteralPath $transcript -Algorithm SHA256).Hash.ToLowerInvariant() }
} else {
    $transcriptInfo = [ordered]@{ path=$transcript; exists=$false; bytes=$null; sha256=$null }
}
$itemInfo = $null
if (Test-Path -LiteralPath $item) {
    $f = Get-Item -LiteralPath $item
    $itemInfo = [ordered]@{ path=$item; exists=$true; kind=$(if($f.PSIsContainer){'DIRECTORY'}else{'FILE'}); bytes=$(if($f.PSIsContainer){$null}else{$f.Length}); sha256=$(if($f.PSIsContainer){$null}else{(Get-FileHash -LiteralPath $item -Algorithm SHA256).Hash.ToLowerInvariant()}); filesystem_creation_time_local=$f.CreationTime.ToString('o'); filesystem_last_write_time_local=$f.LastWriteTime.ToString('o') }
} else {
    $itemInfo = [ordered]@{ path=$item; exists=$false; kind=$null; bytes=$null; sha256=$null; filesystem_creation_time_local=$null; filesystem_last_write_time_local=$null }
}
$windowsTime = [ordered]@{ requested=[bool]$ReadWindowsTimeStatus; status='NOT_RUN'; query_status_output=@(); query_source_output=@() }
if ($ReadWindowsTimeStatus) {
    $w32 = Get-Command w32tm.exe -ErrorAction SilentlyContinue
    if ($w32) {
        $windowsTime.query_status_output = @(& w32tm.exe /query /status 2>&1 | ForEach-Object { [string]$_ })
        $windowsTime.query_status_exit_code = $LASTEXITCODE
        $windowsTime.query_source_output = @(& w32tm.exe /query /source 2>&1 | ForEach-Object { [string]$_ })
        $windowsTime.query_source_exit_code = $LASTEXITCODE
        $windowsTime.status = 'READ_ONLY_QUERY_COMPLETED; INTERPRET_OUTPUT_AND_EXIT_CODES'
    } else {
        $windowsTime.status = 'W32TM_NOT_FOUND'
    }
}
$record = [ordered]@{
    record_type='VBL_LOCAL_EVIDENCE_READOUT'; record_version='1';
    project_root=$root; observed_local=$now.ToString('o'); observed_utc_conversion=$now.ToUniversalTime().ToString('o');
    clock_source='Local Windows system clock'; clock_accuracy='UNVERIFIED_INDEPENDENTLY'; timezone_id=$tz.Id; timezone_base_utc_offset=$tz.BaseUtcOffset.ToString();
    ni_alias=$(if($alias){[ordered]@{name=$alias.Name; definition=$alias.Definition; source=$alias.Source}}else{$null});
    transcript=$transcriptInfo; item=$itemInfo;
    git_status_short=[ordered]@{available=[bool]$git; exit_code=$gitExit; lines=$gitText; ignored_paths_are_not_shown_by_default=$true};
    windows_time=$windowsTime;
    limitations=@('This is a local readout, not an independent witness or trusted timestamp.','An observed path and timestamp do not prove who created it or which command caused it.','An empty git status does not include ignored files.','No cleanup or source-file modification is performed by this script.')
}
$json = ConvertTo-Json -InputObject $record -Depth 8
if ($OutputFile) {
    $out = [IO.Path]::GetFullPath($OutputFile)
    $outDir = [IO.Path]::GetDirectoryName($out)
    if (-not (Test-Path -LiteralPath $outDir -PathType Container)) { throw "Output directory does not exist: $outDir" }
    $stream = [IO.File]::Open($out,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $writer = [IO.StreamWriter]::new($stream,[Text.UTF8Encoding]::new($false)); try {$writer.Write($json)} finally {$writer.Dispose()} } finally { if($stream){$stream.Dispose()} }
    Write-Output "Wrote new evidence record without overwrite: $out"
} else {
    Write-Output $json
}