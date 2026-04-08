import requests
import json

SONAR_URL = ""
PROJECT_KEY = ""
SEVERITIES = ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]  # Puedes ajustar según tus necesidades
CONTEXT_LINES = 5  # Líneas de contexto antes y después del issue

cookies = {
    'JWT-SESSION': '',
    'XSRF-TOKEN': ''
}


# ── Paso 1: Obtener issues ──────────────────────────────────────────────────
print("Obteniendo issues...")
issues_response = requests.get(
    f"{SONAR_URL}/api/issues/search",
    params={
        "componentKeys": PROJECT_KEY,
        "severities": ",".join(SEVERITIES),  # Ej: "BLOCKER,CRITICAL,MAJOR"
        "ps": 500
    },
    cookies=cookies
).json()

issues = issues_response.get("issues", [])
print(f"  → {len(issues)} issues encontrados")

# ── Paso 2: Cachear títulos de reglas (evita llamadas repetidas) ────────────
print("Obteniendo títulos de reglas...")
rules_cache = {}

for issue in issues:
    rule_key = issue.get("rule")
    if rule_key and rule_key not in rules_cache:
        rule_response = requests.get(
            f"{SONAR_URL}/api/rules/show",
            params={"key": rule_key},
            cookies=cookies
        )
        if rule_response.status_code == 200:
            rule_data = rule_response.json().get("rule", {})
            rules_cache[rule_key] = rule_data.get("name", "Sin título")
        else:
            rules_cache[rule_key] = "Sin título"

print(f"  → {len(rules_cache)} reglas únicas obtenidas")

# ── Paso 3: Obtener fragmento de código fuente por issue ───────────────────
print("Obteniendo fragmentos de código fuente...")
report_issues = []

for issue in issues:
    component = issue.get("component")   # Clave interna del archivo
    line      = issue.get("line")
    rule_key  = issue.get("rule")

    # Extraer ruta relativa del archivo (quitar el prefijo del proyecto)
    # Ej: "openmrs-module-FUA:src/main/java/..." → "src/main/java/..."
    file_path = component.split(":", 1)[-1] if component else "Desconocido"

    # Obtener código fuente
    source_snippet = None
    if component and line:
        from_line = max(1, line - CONTEXT_LINES)
        to_line   = line + CONTEXT_LINES

        source_response = requests.get(
            f"{SONAR_URL}/api/sources/show",
            params={"key": component, "from": from_line, "to": to_line},
            cookies=cookies
        )
        if source_response.status_code == 200:
            sources = source_response.json().get("sources", [])
            # Formato: número de línea + contenido
            source_snippet = "\n".join(
                f"{src[0]:4}: {src[1]}" for src in sources
            )

    report_issues.append({
        "message":      issue.get("message"),           # Descripción del issue
        "file":         file_path,                      # Ruta del archivo
        "line":         line,                           # Línea del problema
        "rule_key":     rule_key,                       # Ej: java:S2259
        "rule_title":   rules_cache.get(rule_key, ""),  # Ej: Null pointers should not be...
        "severity":     issue.get("severity", ""),       # BLOCKER, CRITICAL, MAJOR
        "type":         issue.get("type"),              # BUG, VULNERABILITY, CODE_SMELL
        "source_code":  source_snippet                  # Fragmento de código
    })

# ── Paso 4: Exportar JSON ───────────────────────────────────────────────────
output = {
    "project":      PROJECT_KEY,
    "total_issues": len(report_issues),
    "issues":       report_issues
}

with open(f"sonarqube_report_data-{PROJECT_KEY}.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n✅ Exportación completada: sonarqube_report_data.json")
print(f"   Total issues exportados: {len(report_issues)}")

# issues = issues_response.get("issues", [])