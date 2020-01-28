import time 
import random
import os
import time
import json
import shutil
import subprocess

# Read system configuration from the config.json file
def main(a):
    with open(a) as json_file:
        # Load the config file
        app_config = json.load(json_file)
        with open(app_config.get('config_options').get('log_path'), 'w') as log:
            try:
                if app_config is not None:
                    log.write('Loading configuration file...\n')
                i = app_config.get('config_options').get('timer_wait')
                if i is not None:
                    log.write('Timer has been set to {} seconds.\n'.format(str(i)))
                ruta_origen = app_config.get('directories').get('path_to_watch')
                if ruta_origen is not None:
                    log.write('Origin path has been set to {}\n'.format(ruta_origen))
                ruta_destino = app_config.get('directories').get('path_destination')
                if ruta_destino is not None:
                    log.write('Destination path has been set to {}\n'.format(ruta_destino))
                ruta_backup = app_config.get('directories').get('path_backup')
                if ruta_backup is not None:
                    log.write('Backup path has been set to {}'.format(ruta_backup))
            except IOError:
                print('Config file not found.')
                pass
            while True:
                # Set the timer to the amount specified in the config file (seconds)
                time.sleep(i)
                # Iterate through the specified directory to search for .pdf files
                after = dict([(f, None) for f in os.listdir(ruta_origen)])
                added = [f for f in after if f[-4:] == '.pdf']
                # This won't happen if no PDF files are found in the directory
                if added:
                    try:
                        # Execute the exact same procedure for every file found
                        for archivo in added:
                            # Define both input and output files for the conversion process
                            _ruta_salida = ruta_destino + archivo
                            _ruta_entrada = ruta_origen + archivo
                            # Executes the cmd function with the defined routes as parameters
                            resultado = cmd(_ruta_salida, _ruta_entrada)
                            # If conversion is successful (the command will return 0),
                            # the original file is moved to a backup folder.
                            if resultado == 0:
                                log.write('El archivo {} ha sido comprimido y copiado exitosamente\n'.format(archivo))
                            shutil.move(_ruta_entrada, ruta_backup)
                    except IOError:
                        log.write('Error de directorio: {}' + IOError.with_traceback)
                        pass

def cmd(x, y):
    # This function executes a ghostscript command that reduces the quality of the
    # pdf file to eBook resolution. This means that the resolution of all images
    # within the file will be lowered subtly. The difference will be barely noticeable
    # ultimately, so no important details are misses and the quality loss is minimal.
    ruta_salida = "-sOutputFile="
    ruta_salida += x
    # Parameters: /screen: Minimal quality, huge compression rate.
    #             /eBook: Lowered image quality (still very acceptable), noticeable compression rate.
    #             /prepress: Higher quality.
    #             /printer: Original quality
    #             /default: Usually equals /printer quality.
    resultado = subprocess.call(["gswin64c", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dQUIET", "-dBATCH", ruta_salida, y])
    return resultado

# This function is optional, just in case your paths are 
# badly formatted or need backslashes (\) to be escaped
def ruta_digester(a):
    arr = a.split('/')
    return arr[-1]

# Header. This asks for the path to the config.json file in order to load it.
if __name__ == '__main__':
    ruta = input('Ingresa la ruta del archivo config.json: ')
    main(ruta)