# TP Final – Programación Concurrente (UNAHUR · 1C 2026)

Diagnóstico y corrección de problemas de sincronización en el servidor cliente-servidor
**"TicketFast"** (Python + sockets + threading).

## Contexto

La empresa *TicketFast* implementó un servidor de ventas de entradas mediante sockets que
gestiona un inventario global. Durante las pruebas de carga aparecieron varios problemas de
concurrencia que hay que identificar y resolver.

## Consignas

1. **Diagnóstico** — ejecutar servidor y cliente de pruebas, analizar la salida e identificar
   el/los problema(s) de concurrencia.
2. **Sección crítica** — proteger el inventario para garantizar su integridad (evitar el
   *overbooking*).
3. **Límite de concurrencia** — limitar el procesamiento a un máximo de **3 clientes
   simultáneos** para evitar la sobrecarga.
4. **Restricción de UX** — el tiempo de respuesta al cliente (desde `COMPRAR` hasta el mensaje
   de éxito) no debe verse afectado por la latencia de `enviar_email_confirmacion`.
5. **Desacoplamiento** — separar la lógica de red de la de notificaciones usando inversión de
   control (paso de funciones por parámetro) o procesamiento asíncrono / en segundo plano para
   despachar el correo una vez finalizada la transacción crítica.

### Problemas a atacar
- **Overbooking** — race condition sobre el inventario global.
- **Caídas con muchos clientes simultáneos** — falta de límite de concurrencia.
- **Terminal congelada al procesar emails** — envío bloqueante de correo.
- **Busy-waiting** durante la actualización (`while en_actualizacion: pass`) → alto consumo de CPU.

## Estructura del proyecto

```
.
├── servidor.py    # Servidor TicketFast
├── cliente.py     # Cliente de pruebas (estrés)
├── informe/       # Informe de la entrega
└── README.md
```

## Cómo ejecutar

```bash
# Terminal 1
python servidor.py

# Terminal 2
python cliente.py
```

## Entrega

- **Fecha límite de entrega:** 24/06/2026 (informe y código, por el Campus).
- **Fecha límite de defensa:** 25/06/2026.
- ⚠️ Sin defensa, el TP se considera **no entregado / desaprobado**. Cuenta como segundo parcial.

## Integrantes

- _(completar)_
