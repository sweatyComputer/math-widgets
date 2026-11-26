import sys,json,yaml,numpy as np,colour
D=sys.argv[1]; OUT=sys.argv[2]
wl=np.arange(380,781,5)
def load(f):
    y=yaml.safe_load(open(f"{D}/{f}"))
    rows=np.array([[float(v) for v in l.split()] for l in y["DATA"][0]["data"].strip().splitlines()])
    lo,hi=rows[:,0].min()*1000,rows[:,0].max()*1000
    n=np.interp(wl/1000,rows[:,0],rows[:,1]); k=np.interp(wl/1000,rows[:,0],rows[:,2])
    return n,k,lo,hi
M=[ # id, name, file, kind, source, note
("fe","Iron","Fe.yml","pure","Johnson & Christy 1974","Evaporated thin film; may read darker than polished bulk."),
("cr","Chromium (film)","Cr.yml","pure","Johnson & Christy 1974","Evaporated film: reads ~15% darker than polished chrome. Prefer the Rakić version."),
("cr_r","Chromium","Cr_Rakic.yml","pure","Rakić et al. 1998 (model fit)",""),
("ni","Nickel","Ni.yml","pure","Johnson & Christy 1974","Evaporated thin film."),
("ni_r","Nickel (Rakić)","Ni_Rakic.yml","pure","Rakić et al. 1998 (model fit)",""),
("cu","Copper","CuQ.yml","pure","Querry 1985","Same lab as the brass data, so best for brass comparisons."),
("cu_r","Copper (Rakić)","Cu_Rakic.yml","pure","Rakić et al. 1998 (model fit)",""),
("zn","Zinc","Zn.yml","pure","Werner et al. 2009","Querry's zinc data is excluded: it gives an impossible n≈13."),
("au","Gold","Rioux-Au100Ag0.yml","pure","Rioux et al. 2014",""),
("ag","Silver","Rioux-Au0Ag100.yml","pure","Rioux et al. 2014",""),
("al","Aluminium","Al_Rakic.yml","pure","Rakić 1995",""),
("ti","Titanium","Ti_Johnson.yml","pure","Johnson & Christy 1974","Evaporated thin film."),
("pt","Platinum","Pt_Werner.yml","pure","Werner et al. 2009","Partly computed (DFT), not purely measured."),
("w","Tungsten","W_Werner.yml","pure","Werner et al. 2009","Partly computed (DFT), not purely measured."),
("co","Cobalt","Co_Johnson.yml","pure","Johnson & Christy 1974","Evaporated thin film."),
("pd","Palladium","Pd_Johnson.yml","pure","Johnson & Christy 1974","Evaporated thin film."),
("mo","Molybdenum","Mo_Werner.yml","pure","Werner et al. 2009","Partly computed (DFT), not purely measured."),
("ss_aus","Stainless steel, austenitic (304/316 type)","Karlsson-austenitic.yml","alloy","Karlsson & Ribbing 1982","Polished bulk samples. Typical kitchen/architectural stainless."),
("ss_fer","Stainless steel, ferritic (430 type)","Karlsson-ferritic.yml","alloy","Karlsson & Ribbing 1982","Polished bulk samples. Iron + chromium, no nickel."),
("brass70","Brass 70/30 (cartridge brass)","Querry-Cu70Zn30.yml","alloy","Querry 1985",""),
("brass85","Brass 85/15 (red brass)","Querry-Cu85Zn15.yml","alloy","Querry 1985",""),
("brass90","Brass 90/10 (gilding metal)","Querry-Cu90Zn10.yml","alloy","Querry 1985",""),
("nife","Permalloy (nickel–iron)","NiFe.yml","alloy","Tikuišis et al. 2017","150 nm film."),
]
for a in (90,80,70,60,50,40,30,20,10):
    M.append((f"auag{a}",f"Gold–silver {a}/{100-a}",f"Rioux-Au{a}Ag{100-a}.yml","alloy","Rioux et al. 2014",""))
# composition of alloys in terms of pure ids (fractions), for the mixing bench
COMP={"ss_aus":{"fe":0.72,"cr_r":0.18,"ni":0.10},"ss_fer":{"fe":0.83,"cr_r":0.17},"brass70":{"cu":0.70,"zn":0.30},"brass85":{"cu":0.85,"zn":0.15},"brass90":{"cu":0.90,"zn":0.10},"nife":{"ni":0.80,"fe":0.20}}
for a in (90,80,70,60,50,40,30,20,10): COMP[f"auag{a}"]={"au":a/100,"ag":1-a/100}
metals=[]
for id_,name,f,kind,src,note in M:
    n,k,lo,hi=load(f)
    cov="" if lo<=380 and hi>=780 else f"Data covers {lo:.0f}–{hi:.0f} nm; values outside are held flat."
    metals.append(dict(id=id_,name=name,kind=kind,source=src,note=" ".join(x for x in (note,cov) if x),n=np.round(n,4).tolist(),k=np.round(k,4).tolist(),comp=COMP.get(id_)))
shape=colour.SpectralShape(380,780,5)
cm=colour.MSDS_CMFS["CIE 1931 2 Degree Standard Observer"].copy().align(shape)
il=colour.SDS_ILLUMINANTS["D65"].copy().align(shape)
wp=colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["D65"]
srgb=colour.RGB_COLOURSPACES["sRGB"].matrix_XYZ_to_RGB
# XYZ(D65) -> ACEScg with Bradford adaptation: compose
M_cat=colour.adaptation.matrix_chromatic_adaptation_VonKries(colour.xy_to_XYZ(wp),colour.xy_to_XYZ(colour.RGB_COLOURSPACES["ACEScg"].whitepoint),"Bradford")
acescg=colour.RGB_COLOURSPACES["ACEScg"].matrix_XYZ_to_RGB@M_cat
print("check white->acescg",acescg@colour.xy_to_XYZ(wp))
data=dict(wl=wl.tolist(),xbar=np.round(cm.values[:,0],6).tolist(),ybar=np.round(cm.values[:,1],6).tolist(),zbar=np.round(cm.values[:,2],6).tolist(),
  d65=np.round(il.values,4).tolist(),whiteXYZ=colour.xy_to_XYZ(wp).tolist(),M_srgb=np.round(srgb,7).tolist(),M_acescg=np.round(acescg,7).tolist(),metals=metals)
json.dump(data,open(OUT,"w"),separators=(",",":"))
print(len(metals),"metals; bytes",len(json.dumps(data)))
