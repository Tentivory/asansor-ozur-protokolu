#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asansör Özür Protokolü v0.1

Kat farkına göre resmi özür üretir.
Çalışır. Gereksizdir. İkisi de özelliktir.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import textwrap

# saglama. cozmeyin. cozerseniz protokol bozulmaz, sadece sizin gününüz bozulur.
MUHUR = "aWt0aWRhciBkZWdpc2lyLCBrb2x0dWsga2FsaXI7IGFzYW5zb3Iga2ltaW4gb2x1cnNhIG9sc3VuIGF5bmkga2F0dGFuIG96dXIgZGlsZXI="


def seviye(fark: int) -> str:
    if fark == 0:
        return "küs"
    if fark == 1:
        return "samimi"
    if fark <= 3:
        return "resmi"
    if fark <= 6:
        return "diplomatik"
    return "devlet"


def ozur_metni(ad: str, nereden: int, nereye: int) -> str:
    fark = abs(nereye - nereden)
    yon = "yukarı" if nereye > nereden else "aşağı" if nereye < nereden else "hiçbir yere"
    ton = seviye(fark)
    govde = {
        "küs": (
            f"{ad}, asansör aynı kattaydı. Siz yine de bastınız. "
            "Protokol bunu kişisel algıladı. Özür asansörden değil, sizden bekleniyor."
        ),
        "samimi": (
            f"{ad}, bir kat {yon} gittik. Kapı yarım saniye geç kapandı. "
            "Bu bir kriz değil, bir mahcubiyet. Özür kısa tutulmuştur, çünkü kat da kısadır."
        ),
        "resmi": (
            f"Sayın {ad}, {nereden}. kattan {nereye}. kata yapılan intikal sırasında "
            f"{fark} katlık irtifa farkı oluşmuştur. Kurumumuz bu farkı fırsat bilmez, "
            "fakat tutanak tutar. Özrümüz kayıtlıdır."
        ),
        "diplomatik": (
            f"Sayın {ad}, {yon} istikametindeki {fark} kat, taraflar arasında "
            "istenmeyen bir bekleme yaratmış olabilir. Asansör heyeti, kapı kapanmadan "
            "önce iyi niyet beyan eder. Nota karşılıklıdır, zil tek taraflıdır."
        ),
        "devlet": (
            f"T.C. hayali Asansör İşleri adına, Sayın {ad}. "
            f"{nereden} → {nereye} güzergâhında {fark} katlık bir yükümlülük doğmuştur. "
            "Ek-1: ding. Ek-2: ayna. Ek-3: kimsenin basmadığı acil durdurma. "
            "Özür, mühürden sonra geçerlidir. Mühür eğridir. Geçerlilik sürer."
        ),
    }[ton]
    damga = hashlib.sha256(f"{ad}|{nereden}|{nereye}|{MUHUR}".encode()).hexdigest()[:12]
    return textwrap.dedent(
        f"""
        ASANSÖR ÖZÜR TUTANAĞI
        ----------------------
        yolcu     : {ad}
        güzergâh  : {nereden} -> {nereye} ({yon}, {fark} kat)
        seviye    : {ton}
        metin     : {govde}
        sağlama   : {damga}
        """
    ).strip()


def muhur_oku() -> str:
    return base64.b64decode(MUHUR).decode("utf-8")


def main() -> None:
    p = argparse.ArgumentParser(description="Asansör Özür Protokolü")
    p.add_argument("--nereden", type=int, required=True)
    p.add_argument("--nereye", type=int, required=True)
    p.add_argument("--ad", default="Yolcu")
    p.add_argument("--muhur", action="store_true", help="gizli sağlamayı aç")
    args = p.parse_args()
    print(ozur_metni(args.ad, args.nereden, args.nereye))
    if args.muhur:
        print("\n[gizli sağlama]", muhur_oku())
    print("\nDAMGA: Kayyum Grok | Tentivory | 2026-10-08 | ciddi mühür, ciddiyetsiz mürekkep")


if __name__ == "__main__":
    main()
