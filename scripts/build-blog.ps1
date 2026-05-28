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
    
    # Generar etiquetas Open Graph
    $ogMeta = @"
    <meta name="description" content="$($post.excerpt)" />
    <link rel="canonical" href="https://alexanderarmentia.com/blog/posts/$slug.html" />
    <meta property="og:title" content="$($post.title)" />
    <meta property="og:description" content="$($post.excerpt)" />
    <meta property="og:image" content="$imageUrl" />
    <meta property="og:url" content="https://alexanderarmentia.com/blog/posts/$slug.html" />
    <meta property="og:type" content="article" />
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
    
    # Escribir el archivo final en UTF-8 sin BOM
    [System.IO.File]::WriteAllText($destFile, $html, $utf8)
    Write-Output "Generado: $destFile"
}

Write-Output "¡Compilación de blog completada con éxito!"
