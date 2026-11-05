#!/usr/bin/env python3
"""Valida o APK oficial do Cineluvra e cria o manifesto público de atualizações."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib
from urllib.parse import quote
import zipfile

APP_ID = "br.com.dennyximenes.cineluvra"
REPOSITORY = "SrDanvers/cineluvra-atualizacoes"
CERT_SHA256 = "269da380880d92774b52213e3621c3927a222eb2593c6360bfc07de493066568"

def fail(message):
    raise SystemExit("FALHA: " + message)

def axml_attributes(data):
    def u16(at):
        return struct.unpack_from("<H", data, at)[0]
    def u32(at):
        return struct.unpack_from("<I", data, at)[0]
    strings = []
    offset = 8
    while offset < len(data):
        typ, header_size, size = struct.unpack_from("<HHI", data, offset)
        if size < header_size or size < 8 or offset + size > len(data):
            fail("AndroidManifest.xml inválido")
        if typ == 0x0001:
            flags = u32(offset + 16)
            if flags & 0x100:
                fail("Manifesto com pool de strings UTF-8 não suportado")
            count = u32(offset + 8)
            start = u32(offset + 20)
            for i in range(count):
                pos = offset + start + u32(offset + header_size + 4 * i)
                length = u16(pos)
                if length & 0x8000:
                    length = ((length & 0x7fff) << 16) | u16(pos + 2)
                    pos += 4
                else:
                    pos += 2
                strings.append(data[pos:pos + length * 2].decode("utf-16le"))
        if typ == 0x0102 and strings and strings[u32(offset + 20)] == "manifest":
            attr_start, attr_size, count = struct.unpack_from("<HHH", data, offset + 24)
            result = {}
            for i in range(count):
                pos = offset + 16 + attr_start + attr_size * i
                ns, name, raw, value_size, reserved, value_type, value = struct.unpack_from("<IIIHBBI", data, pos)
                key = strings[name]
                if value_type == 0x03:
                    result[key] = strings[value]
                elif value_type == 0x10:
                    result[key] = value
                elif raw != 0xffffffff:
                    result[key] = strings[raw]
            return result
        offset += size
    fail("Não foi possível ler o AndroidManifest.xml")


def verify_dex(dex):
    """Impede publicação de DEX inválido, inclusive strings fora de ordem."""
    if not dex.startswith(b"dex\n") or len(dex) < 112:
        fail("Arquivo classes.dex inválido")
    if struct.unpack_from("<I", dex, 8)[0] != (zlib.adler32(dex[12:]) & 0xffffffff):
        fail("Checksum DEX inválido")
    if dex[12:32] != hashlib.sha1(dex[32:]).digest():
        fail("SHA-1 DEX inválido")
    count, base = struct.unpack_from("<II", dex, 0x38)
    if not 0 < count < 200000 or base + count * 4 > len(dex):
        fail("Tabela de strings DEX inválida")
    last = None
    for i in range(count):
        pos = struct.unpack_from("<I", dex, base + i*4)[0]
        if pos >= len(dex):
            fail("Offset DEX inválido")
        while pos < len(dex) and dex[pos] >= 128:
            pos += 1
        pos += 1
        if pos >= len(dex):
            fail("Comprimento de string DEX inválido")
        try:
            end = dex.index(0, pos)
            value = dex[pos:end].decode("utf-8", errors="replace")
        except ValueError:
            fail("Terminação de string DEX ausente")
        if last is not None and last > value:
            fail("Tabela de strings DEX fora de ordem; aplicativo pode não iniciar")
        last = value

p = argparse.ArgumentParser()
p.add_argument("--apk", required=True)
p.add_argument("--tag", required=True)
p.add_argument("--notes-file", required=True)
p.add_argument("--apksigner-output-file", required=True)
p.add_argument("--existing", default="update.json")
p.add_argument("--out", default="update.json")
p.add_argument("--repository", default=REPOSITORY)
args = p.parse_args()

if args.repository != REPOSITORY:
    fail("Repositório não autorizado")
if not re.fullmatch(r"v\d+\.\d+\.\d+", args.tag):
    fail("Tag precisa ser vX.Y.Z")
version = args.tag[1:]
filename = "Cineluvra-" + version + ".apk"
apk = Path(args.apk)
if apk.name != filename:
    fail("Nome de arquivo incorreto; esperado " + filename)
if not apk.is_file() or not (100_000 <= apk.stat().st_size <= 150_000_000):
    fail("APK ausente ou com tamanho inválido")

with zipfile.ZipFile(apk) as z:
    if z.testzip() is not None:
        fail("APK danificado")
    entries = set(z.namelist())
    if not {"AndroidManifest.xml", "classes.dex", "assets/index.html"} <= entries:
        fail("Entradas obrigatórias ausentes")
    if any(n.lower().endswith((".p12", ".jks", ".keystore", "storepass.txt")) for n in entries):
        fail("Material de assinatura dentro do APK")
    attrs = axml_attributes(z.read("AndroidManifest.xml"))
    if attrs.get("package") != APP_ID:
        fail("Identificador do aplicativo incorreto")
    if attrs.get("versionName") != version:
        fail("Versão do aplicativo diferente da tag")
    code = attrs.get("versionCode")
    if not isinstance(code, int) or code < 4:
        fail("versionCode precisa ser maior ou igual a 4")
    verify_dex(z.read("classes.dex"))
    html = z.read("assets/index.html")
    if len(html) < 300000 or version.encode("utf-8") not in html:
        fail("Conteúdo da versão ausente ou inesperado")

signer_output = Path(args.apksigner_output_file).read_text(encoding="utf-8")
m = re.search(r"(?:Signer #1|V2 Signer):? certificate SHA-256 digest:\s*([a-fA-F0-9]{64})", signer_output)
if not m or m.group(1).lower() != CERT_SHA256:
    fail("Assinatura diferente da original")
sha256 = hashlib.sha256(apk.read_bytes()).hexdigest()
old = Path(args.existing)
if old.exists():
    prev = json.loads(old.read_text(encoding="utf-8"))
    old_code = int(prev.get("latestVersionCode", 0))
    if code < old_code or (code == old_code and prev.get("sha256") != sha256):
        fail("Versão retrocedida ou APK alterado sem aumentar versionCode")
notes = Path(args.notes_file).read_text(encoding="utf-8").strip()[:2000]
payload = {
    "schema": 1,
    "applicationId": APP_ID,
    "latestVersionCode": code,
    "latestVersionName": version,
    "webVersion": version,
    "apkUrl": f"https://github.com/{REPOSITORY}/releases/download/{args.tag}/{quote(filename)}",
    "sha256": sha256,
    "releaseUrl": f"https://github.com/{REPOSITORY}/releases/tag/{args.tag}",
    "releaseNotes": notes or ("Atualização " + version),
    "publishedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
}
Path(args.out).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"versao": version, "versionCode": code, "sha256": sha256}, indent=2))
