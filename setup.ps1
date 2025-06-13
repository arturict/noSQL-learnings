# MongoDB M165 Project Setup for Windows PowerShell
# =================================================

$env:MONGODB_URI = "mongodb://localhost:27017/"

Write-Host "MongoDB M165 Project Setup" -ForegroundColor Green
Write-Host "=========================="
Write-Host "Environment variable MONGODB_URI has been set for this session" -ForegroundColor Yellow
Write-Host ""
Write-Host "Available applications:"
Write-Host ""
Write-Host "1. python environment_demo.py     - Environment variables demo"
Write-Host "2. python database_explorer.py    - Database browser" 
Write-Host "3. python restaurant_crud.py      - Restaurant operations"
Write-Host "4. python power_monitor.py        - System monitoring"
Write-Host "5. python power_grapher.py        - Monitoring graphs"
Write-Host ""
Write-Host "To make environment variable persistent:" -ForegroundColor Cyan
Write-Host "[Environment]::SetEnvironmentVariable('MONGODB_URI', 'mongodb://localhost:27017/', 'User')" -ForegroundColor Gray
Write-Host ""

$choice = Read-Host "Start an application? (1-5 or n)"

switch ($choice) {
    "1" { python environment_demo.py }
    "2" { python database_explorer.py }
    "3" { python restaurant_crud.py }
    "4" { python power_monitor.py }
    "5" { python power_grapher.py }
    default { Write-Host "Setup complete!" -ForegroundColor Green }
}

Read-Host "Press Enter to continue..."
