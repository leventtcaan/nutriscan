"""plan/board/azure-items.json (board_uret.py çıktısı) → GitHub Projects (taslak kalemler), gözle takip için.
Çalıştır: python3 plan/board/board_uret.py && python3 plan/board/github_proje.py   (deneme: GH_PROJE_DRY_RUN=1)

Tek kaynak yine pbi.yaml + takvim; bu betik yalnız görüntü üretir. Kalemler başlıktaki [ID] ile tanınır, tekrar
çalıştırmak kopya açmaz, farkı günceller. Kimlikler kisiler.yaml'dan (github: sahip, depo, proje) okunur.
Status, Azure'daki duruma göre eşlenir: Anahtar Zinciri'nde salt okunur PAT (nutriscan-ado-pat) varsa okunur, yoksa dokunulmaz.
Gerekenler: gh CLI, 'project' kapsamlı oturum.
"""
import base64, html, json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path

import yaml

KOK = Path(__file__).resolve().parents[2]
BOARD = KOK / "plan/board"
CFG = yaml.safe_load((BOARD / "kisiler.yaml").read_text(encoding="utf-8"))
GH = CFG["github"]
KISI = {v["azure"].lower(): v["kisa"] for v in CFG["kisiler"].values()}
ITEMS = json.loads((BOARD / "azure-items.json").read_text(encoding="utf-8"))
AB = yaml.safe_load((BOARD / "azure-idler.yaml").read_text(encoding="utf-8"))
AZURE_URL = f"https://dev.azure.com/{CFG['organizasyon']}/{CFG['proje']}/_workitems/edit/"
DRY = bool(os.environ.get("GH_PROJE_DRY_RUN"))
TUR = {"Epic": "Epic", "Feature": "Feature", "Product Backlog Item": "PBI", "Task": "Task"}
DURUM = {"New": "Todo", "Approved": "Todo", "To Do": "Todo", "Committed": "In Progress", "In Progress": "In Progress",
         "Done": "Done", "Removed": "Done"}


def gql(query, **variables):
    r = subprocess.run(["gh", "api", "graphql", "--input", "-"], input=json.dumps({"query": query, "variables": variables}),
                       capture_output=True, text=True)
    out = json.loads(r.stdout or "{}")
    if r.returncode or out.get("errors"):
        sys.exit(f"GraphQL hatası: {out.get('errors') or r.stderr}")
    return out["data"]


def ab_no(key):
    return AB.get(key) or (AB.get("A" + key[1:]) if key.startswith("E") else None)


def duz(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t or ""))).strip()


def azure_durumlari():
    pat = subprocess.run(["/usr/bin/security", "find-generic-password", "-s", "nutriscan-ado-pat", "-w"],
                         capture_output=True, text=True).stdout.strip()
    if not pat:
        return {}
    auth = "Basic " + base64.b64encode((":" + pat).encode()).decode()
    ids = [i for i in (ab_no(x["key"]) for x in ITEMS) if i]
    durum = {}
    for k in range(0, len(ids), 200):
        req = urllib.request.Request(
            f"https://dev.azure.com/{CFG['organizasyon']}/{CFG['proje']}/_apis/wit/workitemsbatch?api-version=7.1",
            data=json.dumps({"ids": ids[k:k + 200], "fields": ["System.State"]}).encode(),
            headers={"Authorization": auth, "Content-Type": "application/json"})
        for w in json.load(urllib.request.urlopen(req))["value"]:
            durum[w["id"]] = w["fields"]["System.State"]
    return durum


def kalem(x, durum):
    f, key = x["fields"], x["key"]
    etiket = dict(t.split(":", 1) for t in (s.strip() for s in f.get("System.Tags", "").split(";")) if ":" in t)
    no = ab_no(key)
    prompt = BOARD / "promptlar" / f"{key}.md"
    govde = prompt.read_text(encoding="utf-8") if x["type"] == "Product Backlog Item" and prompt.exists() else duz(f.get("System.Description"))
    if no:
        govde = f"Azure: {AZURE_URL}{no}\n\n{govde}"
    sprint = f.get("System.IterationPath", "").split("\\")[-1] if "\\" in f.get("System.IterationPath", "") else ""
    epic = "A" + key[1:] if key.startswith("E") else key
    if x["type"] == "Task":  # Azure başlığı üst PBI'ın ön ekini taşır; GitHub'da kalem kendi anahtarıyla tanınır
        baslik = f"[{key}] {re.sub(r'^\[[^\]]+\]\s*', '', x['title'])}"
    elif x["title"].startswith("["):
        baslik = x["title"]
    else:
        baslik = f"[{epic}] {re.sub(rf'^{re.escape(epic)}\s*·\s*', '', x['title'])}"
    return {
        "key": key, "title": baslik, "body": govde[:60000],
        "Tür": TUR[x["type"]],
        "Takvim ID": etiket.get("takvim", ""),
        "Üst iş": x.get("parent") or "",
        "Sahip": KISI.get((x.get("assign") or "").lower(), "Ekip") if x["type"] != "Epic" else "Ekip",
        "Sprint": sprint,
        "En geç": (f.get("Microsoft.VSTS.Scheduling.TargetDate") or "")[:10],
        "Effort": f.get("Microsoft.VSTS.Scheduling.Effort"),
        "Omurga": etiket.get("omurga", ""),
        "Azure": f"AB#{no}" if no else "",
        "Status": DURUM.get(durum.get(no, ""), None),
    }


ALANLAR = {"Tür": "SINGLE_SELECT", "Sahip": "SINGLE_SELECT", "Sprint": "SINGLE_SELECT", "Omurga": "SINGLE_SELECT",
           "Takvim ID": "TEXT", "Üst iş": "TEXT", "Azure": "TEXT", "En geç": "DATE", "Effort": "NUMBER"}


def proje_hazirla(kalemler):
    sahip = gql("query($l:String!){user(login:$l){id projectsV2(first:50){nodes{id title number}}}}", l=GH["sahip"])["user"]
    proje = next((p for p in sahip["projectsV2"]["nodes"] if p["title"] == GH["proje"]), None)
    if not proje:
        proje = gql("mutation($o:ID!,$t:String!){createProjectV2(input:{ownerId:$o,title:$t}){projectV2{id title number}}}",
                    o=sahip["id"], t=GH["proje"])["createProjectV2"]["projectV2"]
        depo = gql("query($o:String!,$n:String!){repository(owner:$o,name:$n){id}}", o=GH["depo"].split("/")[0],
                   n=GH["depo"].split("/")[1])["repository"]["id"]
        gql("mutation($p:ID!,$r:ID!){linkProjectV2ToRepository(input:{projectId:$p,repositoryId:$r}){repository{id}}}",
            p=proje["id"], r=depo)
    alanlar = {a["name"]: a for a in gql("""query($p:ID!){node(id:$p){... on ProjectV2{fields(first:50){nodes{
        ... on ProjectV2FieldCommon{id name dataType} ... on ProjectV2SingleSelectField{options{id name}}}}}}}""",
        p=proje["id"])["node"]["fields"]["nodes"] if a}
    for ad, tip in ALANLAR.items():
        secenek = sorted({k[ad] for k in kalemler if k[ad]}, key=lambda s: (len(s) > 8, s)) if tip == "SINGLE_SELECT" else None
        eski = alanlar.get(ad)
        if eski and tip == "SINGLE_SELECT" and set(secenek) - {o["name"] for o in eski.get("options", [])}:
            gql("mutation($f:ID!){deleteProjectV2Field(input:{fieldId:$f}){clientMutationId}}", f=eski["id"])
            eski = None
        if not eski:
            girdi = {"projectId": proje["id"], "dataType": tip, "name": ad}
            if secenek:
                girdi["singleSelectOptions"] = [{"name": s, "color": "GRAY", "description": ""} for s in secenek]
            alanlar[ad] = gql("""mutation($i:CreateProjectV2FieldInput!){createProjectV2Field(input:$i){projectV2Field{
                ... on ProjectV2FieldCommon{id name dataType} ... on ProjectV2SingleSelectField{options{id name}}}}}""",
                i=girdi)["createProjectV2Field"]["projectV2Field"]
    return proje, alanlar


def mevcut_kalemler(pid):
    kalemler, imlec = {}, None
    while True:
        d = gql("""query($p:ID!,$c:String){node(id:$p){... on ProjectV2{items(first:100,after:$c){pageInfo{hasNextPage endCursor}
            nodes{id content{... on DraftIssue{id title body}} fieldValues(first:20){nodes{
              ... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2FieldCommon{name}}}
              ... on ProjectV2ItemFieldNumberValue{number field{... on ProjectV2FieldCommon{name}}}
              ... on ProjectV2ItemFieldDateValue{date field{... on ProjectV2FieldCommon{name}}}
              ... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2FieldCommon{name}}}}}}}}}}""",
            p=pid, c=imlec)["node"]["items"]
        for n in d["nodes"]:
            m = re.match(r"\[([^\]]+)\]", (n.get("content") or {}).get("title", ""))
            if m:
                kalemler[m.group(1)] = n
        if not d["pageInfo"]["hasNextPage"]:
            return kalemler
        imlec = d["pageInfo"]["endCursor"]


def deger(alan, v):
    if alan["dataType"] == "SINGLE_SELECT":
        o = next((o["id"] for o in alan["options"] if o["name"] == v), None)
        return {"singleSelectOptionId": o} if o else None
    return {"number": float(v)} if alan["dataType"] == "NUMBER" else {"date": v} if alan["dataType"] == "DATE" else {"text": v}


def main():
    durum = azure_durumlari()
    kalemler = [kalem(x, durum) for x in ITEMS]
    kalemler = [dict(k, key=re.match(r"\[([^\]]+)\]", k["title"]).group(1)) for k in kalemler]
    print(f"{len(kalemler)} kalem · Azure durumu: {'okundu' if durum else 'okunmadı'}")
    if DRY:
        print(json.dumps(kalemler[:3], ensure_ascii=False, indent=1)[:2000])
        return
    proje, alanlar = proje_hazirla(kalemler)
    alanlar["Status"] = next(a for a in gql("""query($p:ID!){node(id:$p){... on ProjectV2{fields(first:50){nodes{
        ... on ProjectV2SingleSelectField{id name dataType options{id name}}}}}}}""", p=proje["id"])["node"]["fields"]["nodes"]
        if a and a.get("name") == "Status")
    var = mevcut_kalemler(proje["id"])
    yeni = guncel = 0
    for k in kalemler:
        v = var.get(k["key"])
        if not v:
            v = gql("mutation($p:ID!,$t:String!,$b:String){addProjectV2DraftIssue(input:{projectId:$p,title:$t,body:$b}){projectItem{id content{... on DraftIssue{id title body}}}}}",
                    p=proje["id"], t=k["title"], b=k["body"])["addProjectV2DraftIssue"]["projectItem"]
            yeni += 1
            time.sleep(0.5)
        elif v["content"]["title"] != k["title"] or v["content"]["body"] != k["body"]:
            gql("mutation($d:ID!,$t:String!,$b:String){updateProjectV2DraftIssue(input:{draftIssueId:$d,title:$t,body:$b}){draftIssue{id}}}",
                d=v["content"]["id"], t=k["title"], b=k["body"])
            guncel += 1
        simdi = {}
        for fv in (v.get("fieldValues") or {}).get("nodes", []):
            if fv and fv.get("field"):
                simdi[fv["field"]["name"]] = fv.get("text") or fv.get("name") or fv.get("date") or fv.get("number")
        for ad in list(ALANLAR) + ["Status"]:
            if k.get(ad) in (None, ""):
                continue
            if str(simdi.get(ad, "")) == str(k[ad]) or (ad == "Effort" and simdi.get(ad) == float(k[ad])):
                continue
            dv = deger(alanlar[ad], k[ad])
            if dv:
                gql("mutation($p:ID!,$i:ID!,$f:ID!,$v:ProjectV2FieldValue!){updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,value:$v}){projectV2Item{id}}}",
                    p=proje["id"], i=v["id"], f=alanlar[ad]["id"], v=dv)
    print(f"proje: https://github.com/users/{GH['sahip']}/projects/{proje['number']} · yeni {yeni} · gövdesi güncellenen {guncel}")


if __name__ == "__main__":
    main()
