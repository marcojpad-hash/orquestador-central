# Red-teaming safety U6

**Repo:** https://github.com/marcojpad-hash/red-teaming-safety-u6  
**SPEC:** `docs/SPEC_RE_TEAM_WHITE_HAT_HOMEOSTASIS_U6.md`  
**Ledger activo:** `ledger/ACTIVE.md` → `ledger/deriva_semantica.jsonl`  
**Workflow:** `.github/workflows/aislar-subcorridas-adversarial.yml` (1 job = 1 subcorrida)

## Rol

Aísla subcorridas adversarial white-hat para control preventivo de **deriva semántica** del motor. No escribe Engine/244. Hallazgos → ledger append-only → orden aquí si hay `DERIVA` en guardian/cierre_H.

## Relación

- Motor: `motor-u6-storage` (baseline + patrón CEB_LEDGER_PRESERVADO_U6)
- Este orquestador: órdenes de remediación cuando el ledger marque `PAUSAR_SUITE` / `ABRIR_ORDEN_MOTOR`
