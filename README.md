# busca-padroes

Comparação de busca de padrões — algoritmo ingênuo (`naive`) vs. KMP — em C e Python.

Cada implementação devolve `count` (ocorrências, com sobreposição) e `checksum`
(soma das posições 0-based mod 2^32); os testes exigem que as 4 implementações concordem.

## Uso

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
source .venv/bin/activate
make data    # gera data/ (seed 42, não versionado)
make build   # compila c/bin/{bench,cli}
make test    # pytest: C naive/kmp, Python naive/kmp vs. oráculo str.find
make bench   # results/c.csv e results/python.csv
make plots   # plots/output/*.png
make all
```

CLI de um caso: `c/bin/cli <naive|kmp> T.txt P.txt` imprime `count checksum`.

## Experimentos

- **exp1**: varia n (1e3…1e6), m=100; casos `random`, `worst`, `best`.
- **exp2**: varia m (10…1000), n=1e5, pior caso.
- **edge**: casos de borda usados nos testes.

Pior caso: `T = a^n`, `P = a^(m-1)b`. Melhor caso do naive: `T = a^n`, `P = b^m`.

## Resultados

![exp1](plots/output/exp1_varia_n.png)
![exp2](plots/output/exp2_varia_m.png)
