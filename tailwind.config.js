/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './academic/templates/**/*.html',
    './accounts/templates/**/*.html',
    './scheduler/templates/**/*.html',
    './timetable/templates/**/*.html',
    './reports/templates/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        /* ── Fondos ─────────────────────────────── */
        bg:      '#121212',   /* Negro mate principal     */
        surface: '#1E1E1E',   /* Cards / sidebar          */
        raised:  '#2A2A2A',   /* Hover / superficies altas*/
        deep:    '#2D0A14',   /* Active nav (tinte burg.) */
        stroke:  '#2E2E2E',   /* Bordes                   */

        /* ── Texto ──────────────────────────────── */
        ink:     '#F8E2E2',   /* Blanco rosado principal  */
        dim:     '#C4C4C4',   /* Plata — texto secundario */

        /* ── Marca ──────────────────────────────── */
        burg: {
          DEFAULT: '#800020', /* Burgundy clásico         */
          light:   '#A85D5D', /* Coral / acento hover     */
          dark:    '#5C0016', /* Burgundy profundo        */
        },

        /* ── Aliases semánticos ─────────────────── */
        primario:   '#800020', /* = burg DEFAULT           */
        secundario: '#A85D5D', /* = burg light             */
        alerta:     '#C4441C', /* Naranja rojizo            */
        exito:      '#2D6A4F', /* Verde oscuro              */
        neutro:     '#2E2E2E', /* = stroke                  */
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
