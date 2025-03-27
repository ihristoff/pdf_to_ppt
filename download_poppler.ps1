$ErrorActionPreference = "Stop"

# URL of the latest Poppler release
$url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip"

# Download location
$output = "poppler\poppler.zip"

Write-Host "Downloading Poppler..."
Invoke-WebRequest -Uri $url -OutFile $output

Write-Host "Extracting Poppler..."
Expand-Archive -Path $output -DestinationPath "poppler" -Force

# Clean up the zip file
Remove-Item $output

Write-Host "Poppler has been installed successfully!" 