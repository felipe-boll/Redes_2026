import os
import socket
import sys

import requests

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:5000")
CONTAINER_IP = socket.gethostbyname(socket.gethostname())

RECADOS = [
    {"name": "Alice",              "text": "Olá a todos! Este é meu primeiro recado.",                "ip_client": "203.0.113.10"},
    {"name": "Bob",                "text": "Sistema funcionando perfeitamente, parabéns!",            "ip_client": "203.0.113.20"},
    {"name": "Container de Teste", "text": "Recado inserido automaticamente pelo container de teste.", "ip_client": CONTAINER_IP},
]


def ok(label: str) -> None:
    print(f"  [OK] {label}")


def fail(label: str, detail: str = "") -> None:
    print(f"  [FALHA] {label}" + (f": {detail}" if detail else ""))
    sys.exit(1)


def main() -> None:
    print("=== Iniciando testes de integração ===\n")

    # healthcheck
    resp = requests.get(f"{BACKEND_URL}/healthcheck", timeout=5)
    if resp.status_code == 200 and resp.json().get("status") == "ok":
        ok("healthcheck respondeu corretamente")
    else:
        fail("healthcheck", str(resp.status_code))

    # inserção de recados
    print()
    ids = []
    for recado in RECADOS:
        resp = requests.post(f"{BACKEND_URL}/messages", json=recado, timeout=5)
        if resp.status_code == 201:
            ids.append(resp.json()["id"])
            ok(f"Recado postado por '{recado['name']}' (id={ids[-1]})")
        else:
            fail(f"POST /messages por '{recado['name']}'", str(resp.status_code))

    # listagem e validação
    print()
    resp = requests.get(f"{BACKEND_URL}/messages", timeout=5)
    if resp.status_code != 200:
        fail("GET /messages", str(resp.status_code))

    data = resp.json()
    ok(f"Total de recados no banco: {len(data)}")

    names_found = {m["name"] for m in data}
    for recado in RECADOS:
        if recado["name"] in names_found:
            ok(f"Recado de '{recado['name']}' encontrado na listagem")
        else:
            fail(f"Recado de '{recado['name']}' não encontrado")

    # validação de campo obrigatório
    print()
    resp = requests.post(f"{BACKEND_URL}/messages", json={"name": ""}, timeout=5)
    if resp.status_code == 400:
        ok("Validação de campos obrigatórios funcionando (400 para payload inválido)")
    else:
        fail("Validação de payload", f"esperado 400, recebido {resp.status_code}")

    print("\n=== Todos os testes passaram! ===")
    print("\nRecados registrados:")
    for m in sorted(data, key=lambda x: x["created_at"]):
        ip_client = m.get("ip_client") or "—"
        ip_origin = m.get("ip_origin") or "—"
        print(f"  [{m['created_at'][:19].replace('T', ' ')}] {m['name']}: {m['text']}")
        print(f"    cliente={ip_client}  origem={ip_origin}")


if __name__ == "__main__":
    main()
