param(
    [Parameter(Mandatory)][ValidateSet("post", "project", "note")][string]$Type,
    [Parameter(Mandatory)][string]$Name
)

$slug = $Name.ToLower() -replace '\s+', '-' -replace '[^a-z0-9\-]', ''

$map = @{
    post    = "posts"
    project = "projects"
    note    = "notes"
}

$dir = "$($map[$Type])/$slug"
$dest = "$dir/index.qmd"
$template = "$($map[$Type])/_template.qmd"

if (Test-Path $dest) {
    Write-Error "$dest already exists."
    exit 1
}

if (-not (Test-Path $template)) {
    Write-Error "Template not found: $template"
    exit 1
}

New-Item -ItemType Directory -Path $dir -Force | Out-Null
Copy-Item $template $dest

$today = Get-Date -Format "yyyy-MM-dd"
(Get-Content $dest) -replace 'date: "2026-01-01"', "date: `"$today`"" -replace 'draft: true', 'draft: true' | Set-Content $dest

Write-Host "Created: $dest"
Write-Host "Edit the file, then remove 'draft: true' when ready to publish."
