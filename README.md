# Push OK — Demo con GitHub Actions

Pequeño ejemplo de **GitHub Actions** que se ejecuta en cada `git push` a la rama `main`, imprime un mensaje de **OK** en los logs y publica un **resumen** en la pestaña *Summary* del job.

## 📦 ¿Qué hace este repo?

- Dispara un **workflow** en eventos de:
  - `push` a `main`
  - `workflow_dispatch` (disparo manual desde la UI)
- Ejecuta un job sencillo que:
  - Muestra en consola: `✅ OK: se ejecutó el workflow...`
  - Publica un **resumen** (panel “Build OK”) usando `GITHUB_STEP_SUMMARY`.
- Incluye:
  - `permissions: contents: read` como buena práctica por defecto.
  - `concurrency` para **cancelar ejecuciones obsoletas** si haces múltiples pushes seguidos.

---

## 🚀 Empezar

1. **Crea el repo** (o usa uno existente) en GitHub.
2. **Activa GitHub Actions** (está activo por defecto en repos públicos; en privados, revisa *Settings → Actions*).
3. **Agrega el workflow** en la ruta exacta:
   ```
   .github/workflows/push-ok.yml
   ```

Contenido recomendado para `push-ok.yml`:

```yaml
name: Push OK

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: "push-ok-${{ github.ref }}"
  cancel-in-progress: true

jobs:
  say-ok:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Decir OK en consola
        run: |
          echo "✅ OK: se ejecutó el workflow en $GITHUB_REF por $GITHUB_ACTOR"

      - name: Publicar resumen bonito
        run: |
          echo "# ✅ Build OK" >> "$GITHUB_STEP_SUMMARY"
          echo "*Commit:* $GITHUB_SHA" >> "$GITHUB_STEP_SUMMARY"
          echo "*Rama:* $GITHUB_REF_NAME" >> "$GITHUB_STEP_SUMMARY"
```

4. **Haz el primer push**:
   ```bash
   git init
   git branch -M main
   echo "# demo-actions" > README.md
   mkdir -p .github/workflows
   # crea el archivo push-ok.yml con el contenido anterior
   git add .
   git commit -m "feat: workflow push OK"
   git remote add origin git@github.com:<tu-usuario>/<tu-repo>.git
   git push -u origin main
   ```

---

## 👀 Ver los resultados

- Ve a **GitHub → Actions → Push OK**.
- Abre el job `say-ok`:
  - En **Logs** verás la línea con `✅ OK...`.
  - En **Summary** verás el panel con “# ✅ Build OK”, commit y rama.

---

## 🏷️ Badge (opcional)

Agrega este badge al `README.md` para ver el estado:

```md
![Push OK](https://github.com/<owner>/<repo>/actions/workflows/push-ok.yml/badge.svg)
```

> Reemplaza `<owner>` y `<repo>` por los de tu repositorio.

---

## 🧩 ¿Por qué estas configuraciones?

- **`permissions: contents: read`**: principio de privilegios mínimos. Si tu workflow necesita más (p. ej., crear releases), amplíalo puntualmente.
- **`concurrency`**:
  ```yaml
  concurrency:
    group: "push-ok-${{ github.ref }}"
    cancel-in-progress: true
  ```
  Evita que se acumulen ejecuciones viejas cuando haces muchos pushes seguidos a la misma rama.

---

## 🔐 Secrets y variables (no requeridas aquí)

Este demo **no** usa `secrets`. Para despliegues reales, configura credenciales en  
**Settings → Secrets and variables** y referencia con `secrets.MI_TOKEN`.

---

## 🧪 Variantes útiles (copiar/pegar)

**Solo PRs hacia main**
```yaml
on:
  pull_request:
    branches: ["main"]
```

**Limitar por rutas**
```yaml
on:
  push:
    branches: ["main"]
    paths:
      - "src/**"
      - ".github/workflows/**"
```

**Job programado (cron diario 7:00 UTC)**
```yaml
on:
  schedule:
    - cron: "0 7 * * *"
```

**Ejemplo de matriz rápida (Node 18 y 20)**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix: { node: [18, 20] }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: ${{ matrix.node }} }
      - run: node -v
```

---

## 🛠️ Solución de problemas

- **“Invalid workflow file … error in yaml syntax (línea X)”**
  - Asegúrate de:
    - Indentación con **espacios** (no tabs).
    - Comillas **simples**/dobles normales, no “comillas tipográficas”.
    - Guardar el archivo como **UTF-8 sin BOM**.
    - Ruta correcta: `.github/workflows/push-ok.yml`.
  - Si la queja es en la línea del `group`, deja el valor **entre comillas**:
    ```yaml
    group: "push-ok-${{ github.ref }}"
    ```

- **El workflow no se dispara**
  - Verifica que hiciste push a **`main`** (o ajusta `branches`).
  - Revisa *Settings → Actions* por si la organización restringe ejecuciones.
  - Asegúrate de que el archivo está en la ruta exacta.

- **No ves el Summary**
  - El summary sale en el job que ejecuta el `echo` hacia `$GITHUB_STEP_SUMMARY`. Abre ese job y su pestaña *Summary* (arriba).

---

## ✅ Objetivo pedagógico

Este repo sirve como **demo mínimo** para introducir:
- Estructura de un workflow (`on`, `jobs`, `steps`).
- Buenas prácticas simples (`permissions`, `concurrency`).
- Uso de `$GITHUB_STEP_SUMMARY` para **reportes legibles**.
