# concatenate_csv.ps1

param(
    [string]$inputDir = "C:\Users\nadim\Downloads\filtered_output",
    [string]$outputFile ="C:\Users\nadim\Downloads\bigfile.csv"
)

# Get all CSV files in the input directory
$csvFiles = Get-ChildItem -Path $inputDir -Filter *.csv -Recurse

# Create a list to store the combined CSV data
$allData = @()

foreach ($file in $csvFiles) {
    Write-Host "Processing $($file.FullName)..."
    
    # Read each CSV file
    $csvData = Import-Csv -Path $file.FullName
    $allData += $csvData
}

# Export the concatenated data to a single CSV file
$allData | Export-Csv -Path $outputFile -NoTypeInformation
Write-Host "Concatenated dataset saved to $outputFile"

# Pause to keep the window open
Read-Host "Press Enter to exit..."
