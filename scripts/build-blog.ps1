$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot
$postsJsonPath = Join-Path $repo 'blog\data\posts.json'
$postsSrcDir = Join-Path $repo 'blog\posts-src'
$postsDestDir = Join-Path $repo 'blog\posts'
$templatePath = Join-Path $repo 'blog\post.html'

if (-not (Test-Path $postsJsonPath)) {
    Write-Error "No se encuentra posts.json en $postsJsonPath"
}
if (-not (Test-Path $templatePath)) {
    Write-Error "No se encuentra la plantilla post.html en $templatePath"
}

# Leer con encoding UTF-8 explícito
$utf8 = [System.Text.Encoding]::UTF8
$posts = [System.IO.File]::ReadAllText($postsJsonPath, $utf8) | ConvertFrom-Json
$template = [System.IO.File]::ReadAllText($templatePath, $utf8)

# Crear directorio de destino si no existe
if (-not (Test-Path $postsDestDir)) {
    New-Item -ItemType Directory -Path $postsDestDir -Force
}

$fmt = New-Object System.Globalization.CultureInfo("es-ES")

foreach ($post in $posts) {
    $slug = $post.slug
    $srcFile = Join-Path $postsSrcDir "$slug.html"
    $destFile = Join-Path $postsDestDir "$slug.html"
    
    if (-not (Test-Path $srcFile)) {
        Write-Warning "No se encuentra el fragmento de contenido para $slug en $srcFile. Saltando..."
        continue
    }
    
    $contentFragment = [System.IO.File]::ReadAllText($srcFile, $utf8)
    
    # Determinar imagen Open Graph
    $imageName = "$slug.png"
    if ($slug -eq "openclaw-desarrollo-agntico-en-el-workspace-local") {
        $imageName = "openclaw-infografia.jpg"
    }
    $imageUrl = "https://alexanderarmentia.com/blog/assets/$imageName"
    
    # Formatear la fecha
    $dateObj = [DateTime]::Parse($post.date)
    $formattedDate = $dateObj.ToString("d 'de' MMMM 'de' yyyy", $fmt)
    
    # Generar etiquetas Open Graph y SEO
    $ogMeta = @"
    <meta name="description" content="$($post.excerpt)" />
    <meta name="author" content="Alexander Armentia Bravo" />
    <link rel="canonical" href="https://alexanderarmentia.com/blog/posts/$slug.html" />
    <meta property="og:title" content="$($post.title)" />
    <meta property="og:description" content="$($post.excerpt)" />
    <meta property="og:image" content="$imageUrl" />
    <meta property="og:url" content="https://alexanderarmentia.com/blog/posts/$slug.html" />
    <meta property="og:type" content="article" />
    <meta property="article:author" content="https://www.linkedin.com/in/alexar69/" />
    <meta property="article:published_time" content="$($post.date)T00:00:00Z" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="$($post.title)" />
    <meta name="twitter:description" content="$($post.excerpt)" />
    <meta name="twitter:image" content="$imageUrl" />
"@
    
    # Realizar reemplazos en la plantilla
    $html = $template
    
    # 1. Título
    $html = [regex]::Replace($html, '(?i)<title>.*?</title>', "<title>$($post.title) | Blog | Alexander Armentia</title>")
    
    # 2. Inyectar metatags debajo de </head>
    $html = $html.Replace("</head>", "$ogMeta`n</head>")
    
    # 3. Terminal slug cmd
    $html = $html.Replace('<span class="term-cmd" id="terminal-post-slug">loading.md</span>', "<span class='term-cmd' id='terminal-post-slug'>$slug.md</span>")
    
    # 4. Inyectar artículo
    $articleHtml = @"
<span class="mono" style="color: var(--a); font-size: 0.8rem; display: block; margin-bottom: 0.5rem;">// Publicado el $formattedDate</span>
                    <h1 class="post-title" style="margin-top: 0.25rem; margin-bottom: 1.5rem; color: var(--t); font-weight: 800; font-size: clamp(1.8rem, 3.5vw, 2.8rem); line-height: 1.15;">$($post.title)</h1>
                    <div class="content">$contentFragment</div>
"@
    
    $targetArticle = '<article id="post" class="post">
                    <div class="mono" style="color: var(--a);">Descifrando archivo...</div>
                </article>'
                
    $replacementArticle = "<article id=`"post`" class=`"post`">$articleHtml</article>"
    
    if (-not $html.Contains($targetArticle)) {
        $targetArticleRegex = '(?s)<article id="post" class="post">.*?</article>'
        $html = [regex]::Replace($html, $targetArticleRegex, $replacementArticle)
    } else {
        $html = $html.Replace($targetArticle, $replacementArticle)
    }

    # 5. Reemplazar el panel de compartir dinámico por uno 100% estático
    $postUrlEncoded = [Uri]::EscapeDataString("https://alexanderarmentia.com/blog/posts/$slug.html")
    $postTitleString = "$($post.title) - por Alexander Armentia"
    $postTitleEncoded = [Uri]::EscapeDataString($postTitleString)
    
    $staticSharePanel = @"
                <div class="share-panel">
                    <span class="mono share-hdr">// compartir_articulo.sh</span>
                    <div class="share-btns">
                        <a id="share-linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url=$postUrlEncoded" class="btn btn-ghost mag-btn" target="_blank" rel="noopener">
                            <span>LinkedIn</span>
                        </a>
                        <a id="share-twitter" href="https://twitter.com/intent/tweet?url=$postUrlEncoded&text=$postTitleEncoded" class="btn btn-ghost mag-btn" target="_blank" rel="noopener">
                            <span>Compartir en X</span>
                        </a>
                        <button id="share-copy" class="btn btn-ghost mag-btn" onclick="navigator.clipboard.writeText(window.location.href); document.getElementById('copy-btn-text').textContent='Copiar Enlace'; alert('Enlace copiado al portapapeles');">
                            <span id="copy-btn-text">Copiar Enlace</span>
                        </button>
                    </div>
                </div>
"@

    $targetSharePanelRegex = '(?s)<div class="share-panel">.*?</div>\s*</div>\s*</div>\s*</section>'
    $replacementSharePanel = "$staticSharePanel`n            </div>`n        </div>`n    </section>"
    $html = [regex]::Replace($html, $targetSharePanelRegex, $replacementSharePanel)

    # 6. Eliminar la inclusión de post.js
    $html = $html.Replace('<script src="/blog/post.js" defer></script>', '<!-- Script dinámico removido para renderizado estático nativo -->')

    # Escribir el archivo final en UTF-8 sin BOM
    [System.IO.File]::WriteAllText($destFile, $html, $utf8)
    Write-Output "Generado estatico: $destFile"
}

# Regenerar blog/rss.xml automaticamente para mantener sincronizados los extractos largos
$rssPath = Join-Path $repo 'blog\rss.xml'
$buildDate = (Get-Date).ToUniversalTime().ToString("r")

$xmlItems = ""
foreach ($p in $posts) {
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
    <description>Resiliencia, tecnologia y liderazgo tecnico</description>
    <language>es-es</language>
    <lastBuildDate>$buildDate</lastBuildDate>
$xmlItems  </channel>
</rss>
"@

[System.IO.File]::WriteAllText($rssPath, $rssContent, $utf8)
Write-Output "RSS Feed actualizado: $rssPath"

Write-Output "Compilacion de blog completada con exito"
