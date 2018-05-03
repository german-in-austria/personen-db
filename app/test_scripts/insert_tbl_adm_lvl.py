# python3 manage.py shell < test_scripts/insert_tbl_adm_lvl.py

from mioeDB.models import tbl_adm_lvl
tbl_adm_lvl.objects.all().delete()
tbl_adm_lvl.objects.all()
q = tbl_adm_lvl(pk=4,name="Bundesland")
q.save()
q = tbl_adm_lvl(pk=6, name="Politischer Bezirk")
q.save()
q = tbl_adm_lvl(pk=8, name="Gemeinde")
q.save()
q = tbl_adm_lvl(pk=9, name="Ort")
q.save()
q = tbl_adm_lvl(pk=10, name="Stadtteile")
q.save()
tbl_adm_lvl.objects.all()
tbl_adm_lvl.objects.filter(id=4)

from mioeDB.models import tbl_adm_lvl


