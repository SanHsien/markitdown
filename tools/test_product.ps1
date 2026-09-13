[CmdletBinding()]
param(
    [switch]$AllPackages,
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
$srcPaths = @(
    Join-Path $repoRoot "packages\markitdown\src"
    Join-Path $repoRoot "packages\markitdown-ocr\src"
    Join-Path $repoRoot "packages\markitdown-mcp\src"
    Join-Path $repoRoot "packages\markitdown-sample-plugin\src"
)
$env:PYTHONPATH = $srcPaths -join [IO.Path]::PathSeparator

Write-Host "==> Run MarkItDown product test suite (Windows)"
if ($AllPackages) {
    $TestArgs = @(
        "packages/markitdown/tests",
        "packages/markitdown-ocr/tests",
        "packages/markitdown-mcp/tests",
        "packages/markitdown-sample-plugin/tests"
    )
} elseif ($TestArgs.Count -eq 0) {
    $TestArgs = @("packages/markitdown/tests")
}

& $pythonExe -m pytest --import-mode=importlib @TestArgs
if ($LASTEXITCODE -ne 0) {
    throw "Product tests failed with exit code $LASTEXITCODE"
}

Write-Host "PRODUCT TESTS GREEN"
