param(
  [Parameter(Mandatory = $true)]
  [string]$ProjectFolder
)

$ErrorActionPreference = 'Stop'
$project = (Resolve-Path -LiteralPath $ProjectFolder).Path
$pdf = Join-Path $project 'deliverables\xiaohongshu-cards.pdf'
$pngDir = Join-Path $project 'deliverables\png'

if (-not (Test-Path -LiteralPath $pdf -PathType Leaf)) {
  throw "Missing combined PDF: $pdf"
}

New-Item -ItemType Directory -Force -Path $pngDir | Out-Null

$bundled = Join-Path $HOME '.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
$command = Get-Command pdftoppm -ErrorAction SilentlyContinue
if (Test-Path -LiteralPath $bundled -PathType Leaf) {
  $pdftoppm = $bundled
} elseif ($command) {
  $pdftoppm = $command.Source
} else {
  throw 'pdftoppm was not found.'
}

$prefix = Join-Path $pngDir 'rendered'
Get-ChildItem -LiteralPath $pngDir -Filter 'rendered-*.png' -ErrorAction SilentlyContinue | Remove-Item -Force
& $pdftoppm '-png' '-r' '96' $pdf $prefix
if ($LASTEXITCODE -ne 0) {
  throw "pdftoppm failed with exit code $LASTEXITCODE"
}

$generated = Get-ChildItem -LiteralPath $pngDir -Filter 'rendered-*.png' |
  Sort-Object { [int]($_.BaseName -replace '^rendered-', '') }
if (-not $generated) {
  throw 'No PNG pages were generated.'
}

$index = 1
foreach ($file in $generated) {
  $target = Join-Path $pngDir ('page-{0:D2}.png' -f $index)
  Move-Item -LiteralPath $file.FullName -Destination $target -Force
  $index++
}

Write-Output "Exported $($generated.Count) PNG pages from existing PDF."
