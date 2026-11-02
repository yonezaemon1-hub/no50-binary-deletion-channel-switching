# No.50 v0.2 -- Windows PowerShell 5.1; no internet, no API, no GPU.
# Usage: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_audit_windows.ps1
# Fail closed: verify SHA256 before any Python code; exit nonzero on mismatch.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $root
try {
    $manifest = Join-Path $root 'SHA256SUMS.txt'
    if (-not (Test-Path -LiteralPath $manifest -PathType Leaf)) {
        throw 'Missing SHA256SUMS.txt'
    }
    $checked = 0
    foreach ($line in (Get-Content -LiteralPath $manifest -Encoding UTF8)) {
        if ($line.Trim() -eq '') { continue }
        if ($line -cnotmatch '^([0-9a-f]{64})  (.+)$') {
            throw "Bad manifest format: $line"
        }
        $expected = $Matches[1]
        $relative = $Matches[2].Replace('/','\')
        if ($relative.Contains('..') -or [System.IO.Path]::IsPathRooted($relative)) {
            throw "Unsafe manifest path: $relative"
        }
        $target = Join-Path $root $relative
        if (-not (Test-Path -LiteralPath $target -PathType Leaf)) {
            throw "Missing file: $relative"
        }
        $actual = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actual -cne $expected) { throw "SHA256 mismatch: $relative" }
        $checked++
    }
    if ($checked -lt 15) { throw "Manifest has unexpectedly few files: $checked" }
    Write-Host "PASS: $checked SHA256 file hashes" -ForegroundColor Green

    $python = Get-Command python -ErrorAction Stop
    $outDir = Join-Path $root 'audit_output'
    if (-not (Test-Path -LiteralPath $outDir)) {
        New-Item -Path $outDir -ItemType Directory | Out-Null
    }
    function Invoke-Verify([string]$ScriptPath, [string[]]$Arguments, [string]$ExpectedFile, [string]$OutputFile) {
        & $python.Source -I -B $ScriptPath @Arguments
        if ($LASTEXITCODE -ne 0) { throw "Verifier failed ($LASTEXITCODE): $ScriptPath" }
        if (-not (Test-Path -LiteralPath $OutputFile -PathType Leaf)) {
            throw "Missing verifier output: $OutputFile"
        }
        $expectedHash = (Get-FileHash -LiteralPath $ExpectedFile -Algorithm SHA256).Hash
        $actualHash = (Get-FileHash -LiteralPath $OutputFile -Algorithm SHA256).Hash
        if ($expectedHash -cne $actualHash) {
            throw "Verifier JSON differs (byte mismatch): $ScriptPath"
        }
        Write-Host "PASS: verifier + exact JSON match: $ScriptPath" -ForegroundColor Green
    }

    $s1 = Join-Path $root 'code\verify_no50.py'
    $e1 = Join-Path $root 'evidence\verified_results.json'
    $o1 = Join-Path $outDir 'verified_results.json'
    Invoke-Verify $s1 @('--out', $o1) $e1 $o1

    $s2 = Join-Path $root 'code\verify_envelope_n6_n8.py'
    $e2 = Join-Path $root 'evidence\envelope_n6_n8.json'
    $o2 = Join-Path $outDir 'envelope_n6_n8.json'
    Invoke-Verify $s2 @('--out', $o2) $e2 $o2

    $s3 = Join-Path $root 'code\independent_mask_audit.py'
    $e3 = Join-Path $root 'evidence\independent_mask_results.json'
    $o3 = Join-Path $outDir 'independent_mask_results.json'
    Invoke-Verify $s3 @('--envelope', $e2, '--out', $o3) $e3 $o3

    Write-Host 'ALL PASS: HASH + FINITE PROOFS + INDEPENDENT TV CHECK' -ForegroundColor Green
    Write-Host 'No proof of unbounded switching; NOVELTY INCONCLUSIVE; PUBLICATION HOLD.'
}
catch {
    Write-Error ("FAIL-CLOSED: " + $_.Exception.Message)
    exit 1
}
finally {
    Pop-Location
}
