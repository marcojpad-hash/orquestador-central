# Pruebas

Ejecutar desde la raíz:

```sh
cd runtime
python -m unittest discover -s ../tests -v
```

Las pruebas usan una base SQLite temporal y no modifican datos persistentes.
