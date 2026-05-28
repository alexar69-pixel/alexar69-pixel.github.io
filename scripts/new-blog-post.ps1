param(
  [Parameter(Mandatory = $true)][string]$Title,
  [Parameter(Mandatory = $true)][string]$Date,
  [Parameter(Mandatory = $true)][string]$Tags,
  [Parameter(Mandatory = $true)][string]$Excerpt,
  [Parameter(Mandatory = $true)][string]$HtmlPath
)

$ErrorActionPreference = 'Stop'

function New-Slug([string]$text) {
  $slug = $text.ToLowerInvariant() -replace '[^a-z0-9\s-]', '' -replace '\s+', '-' -replace '-+', '-'
  return $slug.Trim('-')
}

$repo = Split-Path -Parent $PSScriptRoot
$postsJsonPath = Join-Path $repo 'blog\data\posts.json'
$postsDir = Join-Path $repo 'blog\posts'

$slug = New-Slug $Title
$postFile = Join-Path $postsDir ("$slug.html")

Copy-Item -LiteralPath $HtmlPath -Destination $postFile -Force

$posts = Get-Content -Raw -LiteralPath $postsJsonPath | ConvertFrom-Json
$tagList = $Tags.Split(',') | ForEach-Object { $_.Trim() } | Where-Object { $_ }

$newItem = [PSCustomObject]@{
  slug = $slug
  title = $Title
  excerpt = $Excerpt
  date = $Date
  tags = $tagList
}

$updated = @($posts | Where-Object { $_.slug -ne $slug }) + @($newItem)
$updated = $updated | Sort-Object { [datetime]$_.date } -Descending
$updated | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 -LiteralPath $postsJsonPath

Write-Output "Post created: $slug"
Write-Output "File: $postFile"
