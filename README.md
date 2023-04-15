# Proyecto integrador:
Lenguaje: Python.\
Especialidad: Analytic.

![Analytic banner](Info/braille.jpg)

# Traductor Braille.
Un Flash Crash es un evento muy poco frecuente que se da en los mercados financieros en el que un activo, en este caso una criptomoneda, cae rápidamente de valor
(caída de más del 1% en menos de 1 minuto).\
La aplicación permite monitorear el precio de una determinada criptomoneda y en caso de detectar un flash crash de la misma se lo notifica al usuario vía SMS,
registra el evento completo(minuto previo y posterior al evento) en una BD y posibilita exportarlo a una archivo .csv para un posterior análisis(Data Analytic). 

[![](https://markdown-videos.deta.dev/youtube/JQS-9QosLnw)](https://youtu.be/JQS-9QosLnw)

# Entrada del sistema.
Desde la pantalla de inicio se invita al usuario a ingresar la criptomoneda a monitorear, luego, la app consumirá una API de Binance
(uno de los exchanges más grandes del mundo) donde obtendrá el precio de dicha criptomoneda y lo ira graficando a tiempo real dentro de una ventana de tiempo
de 1 minuto(Trending).\
-A modo de prueba(test) durante el trending de la criptomoneda es posible forzar su flash crash pulsando la letra (t).

![Analytic banner](Info/braillee.jpg)


# Salida del sistema.
En caso de detectarse el flash crash de la criptomoneda ingresada se enviara al usuario una notificación por SMS(*).

![Juego banner](/sms.jpg)

El trending continuara durante un 1 minuto más y el grafico se cerrara automáticamente al completarse el registro en la BD.


# Nota.
En este proyecto está orientado a integrar en una aplicación los conocimientos adquiridos durante el cursado de los 11 módulos de la especialidad Python Analytic.


# Contacto.
Discord ID: PabloP#2073
