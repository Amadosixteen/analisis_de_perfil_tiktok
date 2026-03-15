import subprocess
import sys
import os

def ejecutar_script(nombre_archivo):
    """Ejecuta un script de Python y espera a que termine."""
    print(f"\n--- INICIANDO: {nombre_archivo} ---")
    try:
        # Usamos sys.executable para asegurarnos de usar el mismo intérprete de Python
        resultado = subprocess.run([sys.executable, nombre_archivo], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ El script {nombre_archivo} falló con código {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado al ejecutar {nombre_archivo}: {e}")
        return False

def main():
    print("========================================")

    # 1. Ejecutar Extractor
    if not ejecutar_script("extractor.py"):
        print("\n⚠️ El pipeline se detuvo porque el Extractor falló.")
        return

    # 2. Ejecutar Analizador (Solo si el extractor tuvo éxito)
    if not ejecutar_script("analizador.py"):
        print("\n⚠️ El pipeline falló durante la fase de análisis.")
        return

    print("\n" + "="*40)
    print("INFORMEFINALIZADO CON ÉXITO")
    print("'informe_final.txt'")
    print("="*40)

if __name__ == "__main__":
    main()
