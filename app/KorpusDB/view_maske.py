from django.shortcuts import render , render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import Count, Q
import datetime
import json
from .models import sys_presettags
import KorpusDB.models as KorpusDB
import PersonenDB.models as PersonenDB

def view_maske(request,ipk=0,apk=0):
	aFormular = 'korpusdbmaske/start_formular.html'
	test = ''
	error = ''
	apk=int(apk)
	ipk=int(ipk)
	if apk>0 and ipk>0:
		if 'save' in request.POST:
			if request.POST.get('save') == 'ErhInfAufgaben':
				saveErhInfAufgaben = KorpusDB.tbl_erhinfaufgaben.objects.get(pk=int(request.POST.get('pk')))
				saveErhInfAufgaben.start_Aufgabe = datetime.timedelta(microseconds=int(float(request.POST.get('start_Aufgabe') if request.POST.get('start_Aufgabe') else 0)*1000000))
				saveErhInfAufgaben.stop_Aufgabe = datetime.timedelta(microseconds=int(float(request.POST.get('stop_Aufgabe') if request.POST.get('stop_Aufgabe') else 0)*1000000))
				saveErhInfAufgaben.save()
				aFormular = 'korpusdbmaske/audio_formular.html'
			elif request.POST.get('save') == 'Aufgaben':
				for aAntwort in json.loads(request.POST.get('aufgaben')):
					if 'delit' in aAntwort:		# Löschen
						aDelAntwort = KorpusDB.tbl_antworten.objects.get(pk=aAntwort['id_Antwort'])
						test+=str(aDelAntwort)+' Löschen!<br>'
						if aDelAntwort.ist_Satz:
							aDelAntwort.ist_Satz.delete()
							test+='Satz gelöscht<br>'
						aDelAntwort.delete()
						test+='<hr>'
					else:						# Speichern/Erstellen
						if aAntwort['Kommentar'] or aAntwort['ist_Satz_Standardorth'] or aAntwort['ist_bfl'] or aAntwort['bfl_durch_S'] or aAntwort['ist_Satz_Transkript'] or aAntwort['start_Antwort'] or aAntwort['stop_Antwort'] or aAntwort['tags']:
							if int(aAntwort['id_Antwort']) > 0:		# Speichern
								aSaveAntwort = KorpusDB.tbl_antworten.objects.get(pk=aAntwort['id_Antwort'])
								sTyp = ' gespeichert!<br>'
							else:									# Erstellen
								aSaveAntwort = KorpusDB.tbl_antworten()
								sTyp = ' erstellt!<br>'
							aSaveAntwort.ist_gewaehlt = False
							aSaveAntwort.ist_nat = False
							aSaveAntwort.von_Inf = PersonenDB.tbl_informanten.objects.get(pk=int(aAntwort['von_Inf']))
							aSaveAntwort.zu_Aufgabe = KorpusDB.tbl_aufgaben.objects.get(pk=int(aAntwort['zu_Aufgabe']))
							aSaveAntwort.Reihung = int(aAntwort['reihung'])
							aSaveAntwort.ist_bfl = aAntwort['ist_bfl']
							aSaveAntwort.bfl_durch_S = aAntwort['bfl_durch_S']
							aSaveAntwort.start_Antwort = datetime.timedelta(microseconds=int(float(aAntwort['start_Antwort'] if aAntwort['start_Antwort'] else 0)*1000000))
							aSaveAntwort.stop_Antwort = datetime.timedelta(microseconds=int(float(aAntwort['stop_Antwort'] if aAntwort['stop_Antwort'] else 0)*1000000))
							aSaveAntwort.Kommentar = aAntwort['Kommentar']
							if int(aAntwort['ist_Satz_pk']) > 0:	# Satz bearbeiten
								asSatz = KorpusDB.tbl_saetze.objects.get(pk=aAntwort['ist_Satz_pk'])
								ssTyp = ' gespeichert!<br>'
							else:									# Satz erstellen
								asSatz = KorpusDB.tbl_saetze()
								ssTyp = ' erstellt!<br>'
							asSatz.Transkript = aAntwort['ist_Satz_Transkript']
							asSatz.Standardorth = aAntwort['ist_Satz_Standardorth']
							asSatz.save()
							aSaveAntwort.ist_Satz = asSatz
							test+= 'Satz "'+str(aSaveAntwort.ist_Satz)+'" (PK: '+str(aSaveAntwort.ist_Satz.pk)+')'+ssTyp
							aSaveAntwort.save()
							for asTag in aAntwort['tags']:
								if int(asTag['id_tag'])==0 or int(asTag['id_TagEbene'])==0:
									if int(asTag['pk']) > 0:
										aDelAntwortenTag = KorpusDB.tbl_antwortentags.objects.get(pk=int(asTag['pk']))
										test+= 'AntwortenTag "'+str(aDelAntwortenTag)+'" (PK: '+str(aDelAntwortenTag.pk)+') gelöscht!<br>'
										aDelAntwortenTag.delete()
								else:
									if int(asTag['pk']) > 0:		# Tag bearbeiten
										asAntwortenTag = KorpusDB.tbl_antwortentags.objects.get(pk=int(asTag['pk']))
										stTyp = ' gespeichert!<br>'
									else:							# Tag erstellen
										asAntwortenTag = KorpusDB.tbl_antwortentags()
										stTyp = ' erstellt!<br>'
									asAntwortenTag.id_Antwort = aSaveAntwort
									asAntwortenTag.id_Tag =  KorpusDB.tbl_tags.objects.get(pk=int(asTag['id_tag']))
									asAntwortenTag.id_TagEbene =  KorpusDB.tbl_tagebene.objects.get(pk=int(asTag['id_TagEbene']))
									asAntwortenTag.Reihung =  int(asTag['reihung'])
									asAntwortenTag.save()
									test+= 'AntwortenTag "'+str(asAntwortenTag)+'" (PK: '+str(asAntwortenTag.pk)+')'+stTyp
							test+= 'Antwort "'+str(aSaveAntwort)+'" (PK: '+str(aSaveAntwort.pk)+')'+sTyp+'<hr>'
				aFormular = 'korpusdbmaske/antworten_formular.html'
		Informant = PersonenDB.tbl_informanten.objects.get(pk=ipk)
		Aufgabe = KorpusDB.tbl_aufgaben.objects.get(pk=apk)
		eAntwort = KorpusDB.tbl_antworten()
		eAntwort.von_Inf = Informant
		eAntwort.zu_Aufgabe = Aufgabe
		TagEbenen = KorpusDB.tbl_tagebene.objects.all()
		TagsList = getTagList(KorpusDB.tbl_tags,None)
		Antworten = []
		for val in KorpusDB.tbl_antworten.objects.filter(von_Inf=ipk,zu_Aufgabe=apk).order_by('Reihung'):
			xtags = []
			for xval in KorpusDB.tbl_antwortentags.objects.filter(id_Antwort=val.pk).values('id_TagEbene').annotate(total=Count('id_TagEbene')).order_by('id_TagEbene'):
				xtags.append({'ebene':KorpusDB.tbl_tagebene.objects.filter(pk=xval['id_TagEbene']), 'tags':getTagFamilie(KorpusDB.tbl_antwortentags.objects.filter(id_Antwort=val.pk, id_TagEbene=xval['id_TagEbene']).order_by('Reihung'))})
			Antworten.append({'model':val, 'xtags':xtags})
		Antworten.append(eAntwort)
		ErhInfAufgaben = KorpusDB.tbl_erhinfaufgaben.objects.filter(id_Aufgabe=apk,id_InfErh__ID_Inf__pk=ipk)
		aPresetTags = []
		for val in sys_presettags.objects.filter(Q(sys_presettagszuaufgabe__id_Aufgabe = Aufgabe) | Q(sys_presettagszuaufgabe__id_Aufgabe = None)).distinct():
			aPresetTags.append({'model':val,'tagfamilie':getTagFamiliePT([tzpval.id_Tag for tzpval in val.sys_tagszupresettags_set.all()])})
		return render_to_response(aFormular,
			RequestContext(request, {'Informant':Informant,'Aufgabe':Aufgabe,'Antworten':Antworten, 'TagEbenen':TagEbenen ,'TagsList':TagsList,'ErhInfAufgaben':ErhInfAufgaben,'PresetTags':aPresetTags,'test':test,'error':error}),)
	# aErhebung = 0		; Erhebungen = [{'model':val,'Acount':KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhinfaufgaben__id_InfErh__ID_Erh__pk = val.pk).values('pk').annotate(Count('pk')).count()} for val in KorpusDB.tbl_erhebungen.objects.all()]
	aErhebung = 0		; Erhebungen = [{'model':val,'Acount':KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk = val.pk).values('pk').annotate(Count('pk')).count()} for val in KorpusDB.tbl_erhebungen.objects.filter(Art_Erhebung__gt = 2)]
	aAufgabenset = 0	; Aufgabensets = None
	aAufgabe = 0		; Aufgaben = None
	Informanten = None
	aErhebung = int(request.POST.get('aerhebung')) if 'aaufgabenset' in request.POST else 0
	if aErhebung:
		InformantenCount=PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk = aErhebung).count()
		Aufgabensets = []
		for val in KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk = aErhebung).distinct():
			Aufgabensets.append({'model':val,'Acount':KorpusDB.tbl_aufgaben.objects.filter(von_ASet = val.pk,tbl_erhebung_mit_aufgaben__id_Erh__pk = aErhebung).count()})
		aAufgabenset = int(request.POST.get('aaufgabenset')) if 'aaufgabenset' in request.POST else 0
		if KorpusDB.tbl_aufgabensets.objects.filter(pk=aAufgabenset,tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk = aErhebung).count() == 0:
			aAufgabenset = 0
		if aAufgabenset:
			aAufgabe = int(request.POST.get('aaufgabe')) if 'aaufgabenset' in request.POST else 0
			if 'infantreset' in request.POST:		# InformantenAntwortenUpdate
				# aResponse = HttpResponse(str({str(val.pk):str(KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).count()) for val in PersonenDB.tbl_informanten.objects.all()}).replace("'",'"'))
				# aResponse['Content-Type'] = 'text/text'
				# return aResponse
				Informanten = [{'model':val,'count':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).count(),'tags':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).exclude(tbl_antwortentags=None).count(),'qtag':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe,tbl_antwortentags__id_Tag=35).count()} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk = aErhebung).order_by('inf_sigle')]
				return render_to_response('korpusdbmaske/lmfa-l_informanten.html',
					RequestContext(request, {'aErhebung':aErhebung,'aAufgabenset':aAufgabenset,'aAufgabe':aAufgabe,'Informanten':Informanten}),)
			if aAufgabenset == int(request.POST.get('laufgabenset')):
				Informanten = [{'model':val,'count':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).count(),'tags':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).exclude(tbl_antwortentags=None).count(),'qtag':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe,tbl_antwortentags__id_Tag=35).count()} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk = aErhebung).order_by('inf_sigle')]
			Aufgaben = []
			for val in KorpusDB.tbl_aufgaben.objects.filter(von_ASet=aAufgabenset,tbl_erhebung_mit_aufgaben__id_Erh__pk = aErhebung):
				(aproz,atags,aqtags) = val.status()
				aproz = 100/InformantenCount*aproz
				Aufgaben.append({'model':val, 'aProz': aproz, 'aTags': atags, 'aQTags': aqtags})
	# Ausgabe der Seite
	return render_to_response('korpusdbmaske/start.html',
		RequestContext(request, {'aErhebung':aErhebung,'Erhebungen':Erhebungen,'aAufgabenset':aAufgabenset,'Aufgabensets':Aufgabensets,'aAufgabe':aAufgabe,'Aufgaben':Aufgaben,'Informanten':Informanten,'test':test}),)

### Funktionen: ###

# getTagFamilie für AntwortenTags
def getTagFamilie(Tags):
	afam = []
	aGen = 0
	oTags = []
	for value in Tags:
		pClose = 0
		try:
			while not value.id_Tag.id_ChildTag.filter(id_ParentTag=afam[-1].pk):
				aGen-=1
				pClose+=1
				del afam[-1]
		except:
			pass
		#print(''.rjust(aGen,'-')+'|'+str(value.id_Tag.Tag)+' ('+str(value.id_Tag.pk)+' | '+str([val.pk for val in afam])+' | '+str(aGen)+' | '+str(pClose)+')')
		oTags.append({'aTag':value,'aGen':aGen,'pClose':pClose, 'pChilds':value.id_Tag.id_ParentTag.all().count()})
		afam.append(value.id_Tag)
		aGen+=1
	return oTags

# getTagFamilie für PresetTags
def getTagFamiliePT(Tags):
	afam = []
	aGen = 0
	oTags = []
	for value in Tags:
		pClose = 0
		try:
			while not value.id_ChildTag.filter(id_ParentTag=afam[-1].pk):
				aGen-=1
				pClose+=1
				del afam[-1]
		except:
			pass
		#print(''.rjust(aGen,'-')+'|'+str(value.Tag)+' ('+str(value.pk)+' | '+str([val.pk for val in afam])+' | '+str(aGen)+' | '+str(pClose)+')')
		oTags.append({'aTag':value,'aGen':aGen,'pClose':pClose, 'pChilds':value.id_ParentTag.all().count()})
		afam.append(value)
		aGen+=1
	return oTags

def getTagList(Tags,TagPK):
	TagData = []
	if TagPK == None:
		for value in Tags.objects.filter(id_ChildTag=None):
			child=getTagList(Tags,value.pk)
			TagData.append({'model':value,'child':child})
	else:
		for value in Tags.objects.filter(id_ChildTag__id_ParentTag=TagPK):
			child=getTagList(Tags,value.pk)
			TagData.append({'model':value,'child':child})
	return TagData