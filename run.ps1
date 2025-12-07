#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Run the Income By Major Scraper and API
.DESCRIPTION
    This script starts the Flask API and optionally runs the scraper.
    Both processes can run independently or together.
.PARAMETER RunScraper
    Run the scraper before starting the API
.PARAMETER APIOnly
    Only run the API (don't run scraper)
.PARAMETER ScraperOnly
    Only run the scraper (don't start API)
.EXAMPLE
    .\run.ps1                # Run scraper then start API
    .\run.ps1 -APIOnly       # Only start API
    .\run.ps1 -ScraperOnly   # Only run scraper
#>
param(
    [switch]$RunScraper = $true,
    [switch]$APIOnly = $false,
    [switch]$ScraperOnly = $false
)

# Get the script directory
$ScriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Check if virtual environment exists
$venvPath = Join-Path -Path $ScriptDir -ChildPath ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Error: Virtual environment not found at $venvPath" -ForegroundColor Red
    Write-Host "Please create a virtual environment first:" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
$activateScript = Join-Path -Path $venvPath -ChildPath "Scripts\Activate.ps1"
& $activateScript

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Income By Major Scraper and API" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Handle parameter logic
if ($ScraperOnly) {
    Write-Host ""
    Write-Host "[1/1] Running Scraper Only" -ForegroundColor Yellow
    Write-Host ""
    python (Join-Path -Path $ScriptDir -ChildPath "run_scraper.py")
    exit $LASTEXITCODE
}

if ($APIOnly) {
    Write-Host ""
    Write-Host "[1/1] Starting API Only" -ForegroundColor Yellow
    Write-Host ""
    python (Join-Path -Path $ScriptDir -ChildPath "run_api.py")
    exit $LASTEXITCODE
}

# Default: Run scraper first, then start API
if ($RunScraper) {
    Write-Host ""
    Write-Host "[1/2] Running Scraper" -ForegroundColor Yellow
    Write-Host ""
    python (Join-Path -Path $ScriptDir -ChildPath "run_scraper.py")
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "Warning: Scraper failed with exit code $LASTEXITCODE" -ForegroundColor Yellow
        Write-Host "Continuing to start API anyway..." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "[2/2] Starting API Server" -ForegroundColor Yellow
Write-Host ""
Write-Host "API running at http://localhost:5000" -ForegroundColor Green
Write-Host "Frontend will connect to http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

python (Join-Path -Path $ScriptDir -ChildPath "run_api.py")
