# Set source and destination directories
$sourceDir = "C:\Users\nadim\Downloads\output_ppp"
$destinationDir = "C:\Users\nadim\Downloads\extra_Zavdess"


# Get all files in the source directory except .csv
Get-ChildItem -Path $sourceDir -File | Where-Object { $_.Extension -ne ".csv" } | ForEach-Object {
    $destinationPath = Join-Path -Path $destinationDir -ChildPath $_.Name
    Move-Item -Path $_.FullName -Destination $destinationPath
}
