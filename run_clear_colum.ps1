param(
    [string]$TargetDate = Read-Host "Enter the target date (YYYY-MM-DD)"
)

# if (-not $TargetDate) {
#     $TargetDate = (Get-Date).AddDays(-1).ToString("yyyy-MM-dd")
#     Write-Host "No date passed. Using yesterday's date: $TargetDate"
# }



& python.exe ".\app.py" $TargetDate
