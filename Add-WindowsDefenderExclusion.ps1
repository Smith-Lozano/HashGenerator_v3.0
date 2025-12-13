# Script para agregar excepción en Windows Defender
# Ejecutar como Administrador: Botón derecho -> "Ejecutar como administrador"

$exePath = "C:\Users\Smith Lozano\PyCharmMiscProject\Proyectos\Hash Generator\HashGenerator.exe"

if (Test-Path $exePath) {
    Write-Host "Agregando excepción para: $exePath" -ForegroundColor Green

    try {
        Add-MpPreference -ExclusionPath $exePath
        Write-Host "✓ Excepción agregada exitosamente" -ForegroundColor Green

        # Verificar
        $exclusions = Get-MpPreference | Select-Object -ExpandProperty ExclusionPath
        if ($exePath -in $exclusions) {
            Write-Host "✓ Verificado: La excepción está activa" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "✗ Error: $_" -ForegroundColor Red
        Write-Host "Asegúrate de ejecutar como Administrador" -ForegroundColor Yellow
    }
}
else {
    Write-Host "✗ No se encuentra el ejecutable: $exePath" -ForegroundColor Red
    Write-Host "Ejecuta primero el script de compilación" -ForegroundColor Yellow
}

Write-Host "`nPresiona cualquier tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
