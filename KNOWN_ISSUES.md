# Limitaciones conocidas (Known Issues)

Documento de limitaciones del sistema según el plan de contingencia (proyecto.md 5.3).
Cuando la detección de pose falla, la GUI mostrará un mensaje indicando cómo re-posicionarse.

## Iluminación

- **Baja luz:** La detección puede degradarse o fallar en entornos poco iluminados.
- **Contraluces:** Ventanas o fuentes de luz detrás del usuario pueden afectar la estabilidad de los landmarks.
- **Recomendación:** Usar iluminación uniforme frontal o lateral.

## Oclusión

- **Manos u objetos:** Si la mano u otro objeto tapa hombro o codo, el sistema puede reportar ángulos incorrectos o no detectar la pose.
- **Vestimenta:** Ropa muy holgada o que oculte los puntos anatómicos puede reducir la precisión.

## Rango de poses

- **Perfil lateral:** Si el usuario está muy de perfil respecto a la cámara, la estimación 2D puede perder precisión.
- **Distancia:** El protocolo recomienda ~2 m de la cámara; variaciones pueden afectar la escala.

## Tecnología

- **Modelo:** Se usa `pose_landmarker_lite.task` de MediaPipe (Tasks API). Versiones ligeras priorizan velocidad sobre precisión.
- **Sistema operativo:** En macOS, el acceso a la cámara desde Docker es limitado; usar ejecución local o `--headless --video` para pruebas.

## Entorno controlado

Las validaciones se realizan en condiciones controladas. La robustez en entornos domésticos diversos (distintas habitaciones, iluminación cambiante) no ha sido evaluada de forma exhaustiva.
