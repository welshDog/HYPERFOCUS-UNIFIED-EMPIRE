# PowerShell script to activate the virtual environment

# Enable script execution if needed
try {
    $currentPolicy = Get-ExecutionPolicy
    if ($currentPolicy -eq "Restricted") {
        Write-Output "Changing PowerShell execution policy to allow scripts..."
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
    }
} catch {
    Write-Output "Unable to check/change execution policy. You may need admin rights."
}

# Activate the virtual environment
Write-Output "Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

# Instructions if manual activation is needed
if (-not $?) {
    Write-Output "`nAutomatic activation failed. Try these steps instead:"
    Write-Output "1. Run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process"
    Write-Output "2. Then run: .\venv\Scripts\Activate.ps1"
    Write-Output "`nOr use Command Prompt instead with:"
    Write-Output "venv\Scripts\activate.bat"
}
