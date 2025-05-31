$sourceFolder = "C:\Users\nadim\Downloads\1188976"
$zipFiles = Get-ChildItem -Path $sourceFolder -Filter *.zip

foreach ($zipFile in $zipFiles) {
    $destinationFolder = "$sourceFolder\$($zipFile.BaseName)"
    if (-not (Test-Path $destinationFolder)) {
        New-Item -ItemType Directory -Force -Path $destinationFolder
    }
    Write-Host "Extracting $($zipFile.Name) to $destinationFolder"
    Expand-Archive -Path $zipFile.FullName -DestinationPath $destinationFolder
}
