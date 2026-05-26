# Horarios UCJC

Aplicación web de gestión y generación automática de horarios académicos para la Escuela Politécnica de la Universidad Camilo José Cela. Desarrollada como proyecto fin de asignatura en el curso 2025-26.

Desplegada en producción en Railway: https://web-production-c66aa.up.railway.app

---

## Descripcion

El problema de construir un horario universitario a mano es tedioso, propenso a errores y difícil de mantener cuando los datos cambian. Este proyecto automatiza ese proceso mediante un algoritmo greedy con restricciones que distribuye las sesiones de cada asignatura a lo largo de la semana respetando las reglas del plan de estudios.

La aplicacion cubre cuatro titulaciones: Ingenieria Informatica (II), Ingenieria Robotica (IR), Ingenieria Telematica (IT) y el Doble Grado II+IR (DG, cinco anos). Cada una tiene sus propios cursos, asignaturas, profesores y restricciones horarias. El sistema permite generar, revisar, aprobar y exportar los horarios sin necesidad de tocar una hoja de calculo.

---

## Funcionalidades implementadas

**Gestion academica**
- Catalogo completo de titulaciones, cursos y asignaturas con sus atributos (semestre, alumnos matriculados, si es compartida entre titulaciones).
- Asignacion de un profesor a cada asignatura.
- Disponibilidad y bloqueos de profesores.

**Generacion de horarios**
- Algoritmo greedy CSP que respeta: bloques de 2 horas, 2 sesiones por semana, cursos de manana o tarde segun el ano, asignaturas compartidas en el mismo slot entre titulaciones, y ausencia de solapamientos de profesor entre titulaciones.
- Flujo de estados: Borrador, En revision, Aprobado, Rechazado.
- Deteccion de conflictos al revisar un horario ya generado.

**Vistas y roles**
- Control de acceso basado en roles: Decano, IT, Consultor, Profesor y Estudiante.
- Vista personal del profesor con todas sus sesiones agrupadas por horario.
- Los alumnos solo ven los horarios en estado Aprobado.

**Exportacion**
- Descarga en PDF (ReportLab) y en Excel (openpyxl) desde la seccion Informes.

**Interfaz**
- Diseno oscuro con tokens de color propios sobre Tailwind CSS.
- Alternancia entre tema oscuro y tema claro con persistencia en localStorage.

---

## Stack tecnico

| Capa | Tecnologia |
|---|---|
| Backend | Django 5.2 |
| Base de datos | PostgreSQL (Railway) / SQLite (local) |
| Frontend | Tailwind CSS, Material Symbols |
| Servidor | Gunicorn + WhiteNoise |
| Despliegue | Railway (nixpacks, auto-deploy desde GitHub) |
| Exportacion | ReportLab, openpyxl |

---

## Despliegue local

```bash
git clone https://github.com/sebasxblanco/horario_ucjc.git
cd horario_ucjc
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_datos
python manage.py seed_admin
python manage.py seed_profesores
python manage.py runserver
```

Accede en `http://localhost:8000` con usuario `sebas` y contrasena `sebas2025`.

---

## Aprendizajes

Antes de este proyecto no habia construido nunca una aplicacion web completa de principio a fin. Las cosas que mas me han aportado:

**Django ORM y modelos relacionales.** Disenar el esquema con ForeignKey, OneToOneField y las restricciones de unicidad me obligo a pensar con cuidado en como los datos se relacionan entre si. El error mas comun fue olvidar el `select_related` y generar consultas N+1 en las vistas de la tabla del horario.

**Algoritmos con restricciones.** El generador de horarios empieza siendo algo simple, asignar un bloque libre, y se complica enseguida cuando aparecen las restricciones cruzadas: asignaturas compartidas entre titulaciones, profesores que dan clase en varios grados, cursos con horario hibrido. Aprendi que un greedy bien ordenado (primero las asignaturas mas restringidas) produce resultados aceptables sin necesidad de backtracking completo.

**Control de acceso.** Implementar RBAC desde cero con un decorador `rol_requerido` me hizo entender por que los frameworks de permisos existen. Es facil equivocarse en los casos borde, como un superusuario que no tiene perfil de profesor y accede a la vista de mi horario.

**Despliegue en produccion.** La diferencia entre que algo funcione en local y que funcione en Railway con PostgreSQL, variables de entorno, WhiteNoise para estaticos y migraciones automaticas en el arranque fue la parte que mas tiempo me llevo y la que mas aprendi. El patron `start.sh` con `set -e` que aborta si algo falla resulto esencial.

**CSS sin frameworks de componentes.** Usar Tailwind con tokens de color propios en lugar de Bootstrap me dio mucho control sobre el diseno pero tambien mucha responsabilidad. Aprendi que los temas claros/oscuros con CSS compilado requieren overrides explicitos porque no hay variables en tiempo de ejecucion.

---

## Conclusiones

El proyecto cumple los requisitos funcionales del documento de especificacion: cuatro titulaciones, generacion automatica respetando las restricciones horarias, flujo de aprobacion, exportacion y control de acceso por roles.

Lo que mas me sorprendio fue que la parte tecnica dificil no fue el algoritmo sino la integracion: conseguir que la base de datos, el servidor, los estaticos y los seeds funcionasen juntos en un entorno que no controlo totalmente. Eso es lo que diferencia tener codigo que funciona de tener una aplicacion que funciona.

---

## Puntos de mejora

**Algoritmo.** El greedy actual no garantiza una solucion optima ni detecta cuando es imposible satisfacer todas las restricciones antes de intentarlo. Un solver de tipo backtracking o un enfoque con OR-Tools produciria horarios mas equilibrados y evitaria dias con muchas horas seguidas del mismo grupo.

**Edicion manual de sesiones (RF-07).** El documento de requisitos contempla poder mover sesiones individuales arrastrando en la vista del horario. Esta funcionalidad no esta implementada; el usuario solo puede regenerar el horario completo.

**Disponibilidad del profesor (RF-08).** El modelo `DisponibilidadProfesor` existe en base de datos pero no tiene interfaz. El algoritmo tampoco la usa todavia como restriccion hard.

**Notificaciones (RF-10).** No hay sistema de notificaciones cuando un horario cambia de estado o cuando se asigna una nueva sesion a un profesor.

**Tests automaticos.** No se han escrito tests unitarios ni de integracion. En un proyecto con un algoritmo con muchas restricciones, los tests habrian detectado varios bugs antes de que llegaran a produccion.

**Seguridad.** Las contrasenas del seed son triviales y predecibles. En produccion real habria que forzar un primer cambio de contrasena o integrar autenticacion institucional (LDAP o SAML).
