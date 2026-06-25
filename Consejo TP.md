
### Etapa 2: Análisis y Diseño (grupal, obligatorio)

Ahora tienen que procesar toda la información que consiguieron y tomar decisiones.

#### Qué tienen que hacer:

- Lean toda la conversación y saquen las ideas principales
- Identifiquen **al menos 4 módulos funcionales** que el sistema necesita tener
- Decidan qué va a hacer cada módulo y escriban una descripción clara
- **Documenten cada decisión:** ¿de dónde salió esa funcionalidad? ¿en qué parte de la charla con el cliente apareció ese problema?
- Si asumieron algo que el cliente no dijo explícitamente, anótenlo como "supuesto"

**Ejemplo de módulo bien documentado:**

**Módulo:** Registro de clientes

**Funcionalidad:** Permite dar de alta clientes nuevos guardando nombre, teléfono, dirección y tipo de cliente (particular/empresa)

**Justificación:** El cliente mencionó que "anota los datos en un cuaderno y después no encuentra nada". También dijo que necesita diferenciar entre clientes particulares y empresas porque no les cobra igual.

**Supuesto:** Asumimos que el DNI no es obligatorio porque el cliente nunca lo mencionó como un dato que necesite.

### Etapa 3: Desarrollo

Hora de programar. Van a construir los módulos que identificaron.

#### Qué tienen que hacer:

- Escriban el código en Python de cada módulo
- Cada módulo tiene que ser funcional: debe hacer lo que dijeron que iba a hacer
- El código tiene que reflejar lo que entendieron del negocio (nombres de variables, funciones, lógica)
- Pueden dividirse los módulos entre integrantes del grupo, o hacerlo todo juntos
- Prueben que funciona antes de entregar

**✅ Consejo:** Es mejor tener 4 módulos simples que funcionen bien, que 8 módulos complejos a medio hacer. La calidad importa más que la cantidad.

## 📦 ¿Qué tienen que entregar?

1

#### Conversación completa con el referente

Exportación del chat o capturas de pantalla donde se vea toda la conversación. Tiene que estar claro quiénes preguntaron qué y qué respondió el cliente.

2

#### Documento de relevamiento y análisis

Puede ser un PDF, un Word, un Markdown, lo que quieran. Tiene que incluir:

- Descripción del negocio (¿a qué se dedica? ¿qué problemas tiene?)
- Los 4+ módulos identificados con descripción de cada uno
- Justificación: ¿por qué cada módulo? ¿qué parte de la conversación lo motivó?
- Supuestos: ¿qué cosas decidieron sin que el cliente lo dijera?

3

#### Código fuente del sistema

Archivos `.py` con el código de cada módulo. Bien comentado, prolijo, funcional.

4

#### README del proyecto

Un archivo que explique:

- Cómo ejecutar el sistema
- Qué hace cada módulo
- Qué librerías se necesitan (si usan alguna)
- Limitaciones conocidas


## ✅ ¿Cómo se evalúa?

No se busca que todos lleguen a la misma solución. Se busca que puedan **justificar la suya** a partir de lo que entendieron.

✓

**Calidad del relevamiento**

¿Hicieron buenas preguntas? ¿Fueron atrás de los detalles? ¿Entendieron el problema real o se quedaron en la superficie?

✓

**Identificación de problemas**

¿Los módulos que proponen resuelven problemas reales del negocio? ¿Priorizaron bien? ¿Se nota que entendieron qué era importante?

✓

**Documentación de decisiones**

¿Justificaron cada módulo? ¿Citaron fragmentos de la conversación? ¿Dejaron claro qué asumieron y qué les dijeron explícitamente?

✓

**Coherencia entre relevamiento y código**

¿El código refleja lo que entendieron? ¿Los nombres de funciones y variables tienen sentido con el negocio? ¿Hay lógica entre lo documentado y lo programado?

✓

**Funcionamiento del código**

¿El código corre? ¿Hace lo que dice que hace? ¿Está prolijo y comentado? ¿Se puede entender qué hace cada parte?

✓

**Claridad en la entrega**

¿El README está completo? ¿Se puede ejecutar el sistema siguiendo las instrucciones? ¿La documentación es clara?