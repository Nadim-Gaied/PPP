$sourceFolder = "C:\Users\nadim\Downloads\1188976"
$zipFiles = Get-ChildItem -Path $sourceFolder -Filter *.zip

foreach ($zipFile in $zipFiles) {
    Remove-Item $zipFile.FullName
    Write-Host "Deleted $($zipFile.Name)"
}
