param(
  [Parameter(Mandatory = $true)]
  [string]$Root
)

$resolvedRoot = Resolve-Path -LiteralPath $Root -ErrorAction Stop
$rootPath = $resolvedRoot.Path
$files = @(Get-ChildItem -LiteralPath $rootPath -Recurse -File -Filter '*.md')
$errors = [System.Collections.Generic.List[string]]::new()

function Resolve-ObsidianTarget([System.IO.FileInfo]$from, [string]$target) {
  $base = $from.DirectoryName
  $candidates = @(
    (Join-Path $base $target),
    (Join-Path $base ($target + '.md')),
    (Join-Path (Join-Path $base $target) ('00-' + (Split-Path $target -Leaf) + '.md'))
  )
  foreach ($candidate in $candidates) {
    if (Test-Path -LiteralPath $candidate -PathType Leaf) { return $true }
  }
  return $false
}

foreach ($file in $files) {
  $relative = $file.FullName.Substring($rootPath.Length + 1)
  $text = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
  $lines = [System.IO.File]::ReadAllLines($file.FullName, [System.Text.Encoding]::UTF8)

  if ($text -notmatch '(?m)^> \u539f\u6587\uff1a\[[^\]]+\]\(https?://docs\.unity3d\.com/') {
    $errors.Add("Missing source link: $relative")
  }
  if ($file.Name -match '-\u4e2d\u6587\u6587\u6863') {
    $errors.Add("Forbidden filename suffix: $relative")
  }
  if ($text -match '\\\|') {
    $errors.Add("Escaped table separator found: $relative")
  }
  if ($text -match '(?im)^\s*(?:--\s*)?TODO(?:[\uff1a:\-\s]|$)|(?im)^\s*(?:--\s*)?TODO[-\uff1a:]?\u672a\u62c9\u53d6\u539f\u6587') {
    $errors.Add("Unresolved migration TODO: $relative")
  }
  if ($text -match '(?m)^\|.*\[\[[^\]]+\|[^\]]+\]\]') {
    $errors.Add("Aliased Obsidian link inside table: $relative")
  }

  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -eq '---') {
      $beforeBlank = $i -gt 0 -and [string]::IsNullOrWhiteSpace($lines[$i - 1])
      $afterBlank = $i -lt ($lines.Count - 1) -and [string]::IsNullOrWhiteSpace($lines[$i + 1])
      if (-not ($beforeBlank -and $afterBlank)) {
        $errors.Add("Separator needs blank lines: ${relative}:$($i + 1)")
      }
    }
  }

  [regex]::Matches($text, '!\[[^\]]*\]\(([^)]+)\)') | ForEach-Object {
    $image = $_.Groups[1].Value.Trim()
    if ($image -notmatch '^https?://' -and -not (Test-Path -LiteralPath (Join-Path $file.DirectoryName $image) -PathType Leaf)) {
      $errors.Add("Missing image: $relative -> $image")
    }
  }

  [regex]::Matches($text, '\[\[([^\]|#]+)(?:#[^\]|]+)?\]\]') | ForEach-Object {
    $target = $_.Groups[1].Value.Trim()
    if ($target -and -not (Resolve-ObsidianTarget $file $target)) {
      $errors.Add("Missing local link: $relative -> $target")
    }
  }
}

if ($errors.Count -gt 0) {
  $errors | ForEach-Object { Write-Output $_ }
  exit 1
}

Write-Output "PASS: $($files.Count) Markdown files"
exit 0
