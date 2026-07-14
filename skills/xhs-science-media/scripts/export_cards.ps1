param(
  [Parameter(Mandatory = $true)]
  [string]$ProjectPath
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path -LiteralPath $ProjectPath).Path
$html = Join-Path $root "web\index.html"
$deliverables = Join-Path $root "deliverables"
$pngDir = Join-Path $deliverables "png"
$pdf = Join-Path $deliverables "xiaohongshu-cards.pdf"
$profileDir = Join-Path $env:TEMP ("xhs-cards-edge-" + [guid]::NewGuid().ToString("N"))

if (-not (Test-Path -LiteralPath $html)) { throw "Missing web/index.html" }
New-Item -ItemType Directory -Force -Path $deliverables, $pngDir, $profileDir | Out-Null

$edgeCandidates = @(
  "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
  "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
  "$env:LOCALAPPDATA\Microsoft\Edge\Application\msedge.exe"
)
$edge = $edgeCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $edge) { throw "Microsoft Edge was not found." }

$pdftoppmCommand = Get-Command pdftoppm.exe -ErrorAction SilentlyContinue
$pdftoppm = if ($pdftoppmCommand) { $pdftoppmCommand.Source } else { $null }
if (-not $pdftoppm) {
  $bundled = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe"
  if (Test-Path -LiteralPath $bundled) { $pdftoppm = $bundled }
}
if (-not $pdftoppm) { throw "pdftoppm was not found." }

if (Test-Path -LiteralPath $pdf) { Remove-Item -LiteralPath $pdf -Force }
Get-ChildItem -LiteralPath $pngDir -Filter "page-*.png" -File -ErrorAction SilentlyContinue | Remove-Item -Force

$uri = ([System.Uri]$html).AbsoluteUri
& $edge --headless=new --disable-gpu --hide-scrollbars --run-all-compositor-stages-before-draw --user-data-dir="$profileDir" --no-pdf-header-footer --print-to-pdf="$pdf" $uri
for ($i = 0; $i -lt 60 -and -not (Test-Path -LiteralPath $pdf); $i++) { Start-Sleep -Seconds 1 }
if (-not (Test-Path -LiteralPath $pdf)) { throw "HTML to PDF export failed." }

& $pdftoppm -png -r 96 $pdf (Join-Path $pngDir "page")
if ($LASTEXITCODE -ne 0) { throw "PDF to PNG export failed." }

$files = Get-ChildItem -LiteralPath $pngDir -Filter "page-*.png" -File | Sort-Object { [int]($_.BaseName -replace "\D", "") }
$counter = 1
foreach ($file in $files) {
  $newName = "page-{0:D2}.png" -f $counter
  if ($file.Name -ne $newName) {
    Move-Item -LiteralPath $file.FullName -Destination (Join-Path $pngDir $newName) -Force
  }
  $counter++
}

Write-Host "Exported $($files.Count) cards to $deliverables"
