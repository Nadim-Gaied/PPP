# Define the path to FeatureExtraction.exe and the directories
$featureExtractionPath = "C:\Users\nadim\Downloads\OpenFace_2.2.0_win_x64\OpenFace_2.2.0_win_x64\FeatureExtraction.exe"
$inputDir = "C:\Users\nadim\Downloads\1188976"
$outputDir = "C:\Users\nadim\Downloads\output_ppp"

# Get all .mp4 files recursively in the specified directory and its subdirectories
$files = Get-ChildItem -Path $inputDir -Recurse -File -Filter "*.mp4"

# Loop through each .mp4 file
foreach ($file in $files) {
    Write-Host "Processing file: $($file.Name)"
    
    # Construct the FeatureExtraction command with the full path to the current video file
    $command = "& `"$featureExtractionPath`" -f `"$($file.FullName)`" -out_dir `"$outputDir`" -2Dfp false -pdmparams false -pose -aus -3Dfp -tracked -recurse"
    
    # Run the command
    Invoke-Expression $command

    Write-Host "FeatureExtraction complete for file: $($file.Name)"
}

Write-Host "Processing complete."

