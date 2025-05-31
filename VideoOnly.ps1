# Folder to clean up
$folderPath = "C:\Users\nadim\Downloads\1188976"

# Go through all files, including subfolders
Get-ChildItem -Path $folderPath -File -Recurse | ForEach-Object {
    $fileName = $_.Name

    # If filename does NOT start with 02-01-, delete it
    if ($fileName -notmatch '^02-') {
        Write-Host "Deleting $fileName"
        Remove-Item $_.FullName
    }
}
