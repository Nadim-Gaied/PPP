# run_filter.ps1

param(
    [string]$inputDir = "C:\Users\nadim\Downloads\output_ppp",
    [string]$relativePath = "C:\Users\nadim\Downloads\output_ppp",
    [string]$outputDir = "C:\Users\nadim\Downloads\filtered_output"
)


# Get all CSV files in the input directory
$csvFiles = Get-ChildItem -Path $inputDir -Filter *.csv -Recurse

foreach ($file in $csvFiles) {
    Write-Host "Processing $($file.FullName)..."
    python "C:\Users\nadim\Downloads\CSV_Filterer.py" $file.FullName $relativePath $outputDir
}
