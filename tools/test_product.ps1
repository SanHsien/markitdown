[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$TestArgs = @()
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $venvPython) {
    $pythonExe = $venvPython
} else {
    $pythonExe = (Get-Command python -ErrorAction Stop).Source
}

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = Join-Path $repoRoot "packages\markitdown\src"

Write-Host "==> Run MarkItDown product test suite (Windows)"
if ($TestArgs.Count -eq 0) {
    $TestArgs = @("packages/markitdown/tests")
}

& $pythonExe -m pytest @TestArgs
if ($LASTEXITCODE -ne 0) {
    throw "Product tests failed with exit code $LASTEXITCODE"
}

Write-Host "PRODUCT TESTS GREEN"
