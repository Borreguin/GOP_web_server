import sys, os
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_path)
sys.path.append("C:\inetpub\wwwroot\Gop_WebServer_production")
from my_lib.calculations import calculos as cal
cal.reserva_de_generacion()
