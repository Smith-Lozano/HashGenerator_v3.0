@echo off
chcp 65001 >nul
echo ========================================
echo  HASH GENERATOR - EXCEPCIÓN WINDOWS DEFENDER
echo ========================================
echo.
echo Este script agregará HashGenerator.exe a las excepciones
echo de Windows Defender para evitar bloqueos.
echo.
echo REQUISITO: Ejecutar como Administrador
echo.
echo Opciones:
echo   1. Agregar excepción automáticamente
echo   2. Ver excepciones actuales
echo   3. Eliminar todas las excepciones (peligroso)
echo   4. Salir
echo.
set /p choice="Selecciona opción (1-4): "

if "%choice%"=="1" (
    powershell -ExecutionPolicy Bypass -File "%~dp0Add-WindowsDefenderExclusion.ps1"
) else if "%choice%"=="2" (
    powershell -Command "Get-MpPreference | Select-Object -ExpandProperty ExclusionPath"
    pause
) else if "%choice%"=="3" (
    echo ¡ADVERTENCIA! Esto eliminará TODAS las excepciones.
    set /p confirm="¿Estás seguro? (s/n): "
    if /i "%confirm%"=="s" (
        powershell -Command "Set-MpPreference -ExclusionPath @()"
        echo Excepciones eliminadas.
        pause
    )
) else (
    exit
)
