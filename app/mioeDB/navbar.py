from django.core.urlresolvers import reverse


def navbar(request):
	anav = []
	if request.user.is_authenticated():
		asub = []
		if request.user.has_perm('mioeDB.mioe_maskView'):
			asub.append({'sort': 0, 'titel': 'Volkszählungsdaten', 'url': reverse('mioeDB:vz')})
			asub.append({'sort': 1, 'titel': 'Institutions Daten', 'url': reverse('mioeDB:inst')})
			asub.append({'sort': 2, 'titel': 'MiÖ-Orte', 'url': reverse('mioeDB:orte')})
			asub.append({'sort': 3, 'titel': 'Institutionen', 'url': reverse('mioeDB:institutionen')})
			asub.append({'sort': 4, 'titel': 'MiÖ-Orte mit Institutionen', 'url': reverse('mioeDB:mortinstitutionen')})
			asub.append({'sort': 6, 'titel': 'Wenkerbogen', 'url': reverse('mioeDB:wb')})
			asub.append({'sort': 7, 'titel': 'Varietäten', 'url': reverse('mioeDB:varietaet')})
			asub.append({'sort': 8, 'titel': 'Literatur', 'url': reverse('mioeDB:literatur')})
			asub.append({'sort': 9, 'titel': 'Verlage', 'url': reverse('mioeDB:verlage')})
			asub.append({'sort': 10, 'titel': 'Quellen', 'url': reverse('mioeDB:quelle')})
			asub.append({'sort': 11, 'titel': 'Arten in Quelle', 'url': reverse('mioeDB:artInQuelle')})
			asub.append({'sort': 12, 'titel': 'Religionen', 'url': reverse('mioeDB:religion')})
			asub.append({'sort': 40, 'titel': 'Auswertung', 'url': reverse('mioeDB:auswertung')})
			asub.append({'sort': 45, 'titel': 'Mioe Auswertung', 'url': reverse('mioeDB:mioeAuswertung')})
		if asub:
			anav.append({'sort': 15, 'titel': 'MioeDB', 'url': '#', 'sub': asub})
	return anav
