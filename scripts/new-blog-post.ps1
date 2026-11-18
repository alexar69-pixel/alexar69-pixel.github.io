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

# Regenerar blog/rss.xml automáticamente
$rssPath = Join-Path $repo 'blog\rss.xml'
$buildDate = (Get-Date).ToUniversalTime().ToString("r")

$xmlItems = ""
foreach ($p in $updated) {
  $pDate = [DateTime]::Parse($p.date).ToString("r")
  $xmlItems += "    <item>`n"
  $xmlItems += "      <title>$($p.title)</title>`n"
  $xmlItems += "      <link>https://alexanderarmentia.com/blog/posts/$($p.slug).html</link>`n"
  $xmlItems += "      <guid>https://alexanderarmentia.com/blog/posts/$($p.slug).html</guid>`n"
  $xmlItems += "      <pubDate>$pDate</pubDate>`n"
  $xmlItems += "      <description>$($p.excerpt)</description>`n"
  $xmlItems += "    </item>`n"
}

$rssContent = @"
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Blog de Alexander Armentia</title>
    <link>https://alexanderarmentia.com/blog/</link>
    <description>Resiliencia, tecnología y liderazgo técnico</description>
    <language>es-es</language>
    <lastBuildDate>$buildDate</lastBuildDate>
$xmlItems  </channel>
</rss>
"@

$rssContent | Set-Content -Encoding UTF8 -LiteralPath $rssPath

Write-Output "Post created: $slug"
Write-Output "File: $postFile"
Write-Output "RSS Feed updated: $rssPath"
