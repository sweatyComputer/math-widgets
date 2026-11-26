"""Download the n,k datasets this widget uses from the refractiveindex.info database (CC0).
Usage: python fetch_data.py raw_data
"""
import sys, os, urllib.request
BASE = "https://raw.githubusercontent.com/polyanskiy/refractiveindex.info-database/master/database/data/"
FILES = {
    "Fe.yml": "main/Fe/nk/Johnson.yml", "Cr.yml": "main/Cr/nk/Johnson.yml", "Cr_Rakic.yml": "main/Cr/nk/Rakic-LD.yml",
    "Ni.yml": "main/Ni/nk/Johnson.yml", "Ni_Rakic.yml": "main/Ni/nk/Rakic-LD.yml", "CuQ.yml": "main/Cu/nk/Querry.yml",
    "Cu_Rakic.yml": "main/Cu/nk/Rakic-LD.yml", "Zn.yml": "main/Zn/nk/Werner.yml", "Al_Rakic.yml": "main/Al/nk/Rakic.yml",
    "Ti_Johnson.yml": "main/Ti/nk/Johnson.yml", "Pt_Werner.yml": "main/Pt/nk/Werner.yml", "W_Werner.yml": "main/W/nk/Werner.yml",
    "Co_Johnson.yml": "main/Co/nk/Johnson.yml", "Pd_Johnson.yml": "main/Pd/nk/Johnson.yml", "Mo_Werner.yml": "main/Mo/nk/Werner.yml",
    "Karlsson-austenitic.yml": "other/alloys/stainless steel/nk/Karlsson-austenitic.yml",
    "Karlsson-ferritic.yml": "other/alloys/stainless steel/nk/Karlsson-ferritic.yml",
    "Querry-Cu70Zn30.yml": "other/alloys/Cu-Zn/nk/Querry-Cu70Zn30.yml", "Querry-Cu85Zn15.yml": "other/alloys/Cu-Zn/nk/Querry-Cu85Zn15.yml",
    "Querry-Cu90Zn10.yml": "other/alloys/Cu-Zn/nk/Querry-Cu90Zn10.yml", "NiFe.yml": "other/alloys/Ni-Fe/nk/Tikuisis_bare150nm.yml",
}
for a in range(0, 101, 10):
    FILES[f"Rioux-Au{a}Ag{100-a}.yml"] = f"other/alloys/Au-Ag/nk/Rioux-Au{a}Ag{100-a}.yml"
out = sys.argv[1] if len(sys.argv) > 1 else "raw_data"
os.makedirs(out, exist_ok=True)
for name, path in FILES.items():
    urllib.request.urlretrieve(BASE + path.replace(" ", "%20"), os.path.join(out, name))
    print("got", name)
