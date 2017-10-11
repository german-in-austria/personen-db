from django.shortcuts import get_object_or_404 , render , render_to_response , redirect
from django.template import RequestContext, loader
from DB.funktionenDB import formularView, findDicValInList
from DB.funktionenAuswertung import auswertungView
from .models import sys_presettags
import KorpusDB.models as KorpusDB

def aufgabensets(request):
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'KorpusDB'
	tabelle_name = 'tbl_aufgabensets'
	permName = 'aufgabensets'
	primaerId = 'aufgabenset'
	aktueberschrift = 'Aufgabensets'
	asurl = '/korpusdb/aufgabensets/'
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [
		{'titel':'Aufgabenset','app':'KorpusDB','tabelle':'tbl_aufgabensets','id':'aufgabenset','optionen':['einzeln'],
		 'felder':['+id','Kuerzel','Name_Aset','Fokus','Art_ASet','Kommentar','zu_Phaenomen','|zusammengestellt_als=aufgabenzusammenstellung:id'],
		 'sub':[
			{'titel':'Aufgaben','app':'KorpusDB','tabelle':'tbl_aufgaben','id':'aufgabe','optionen':['liste'],
			 'felder':['+id','Variante','ist_dialekt','Beschreibung_Aufgabe','|von_ASet=parent:id'],
			 'sub':[
				{'titel':'Antwortmoeglichkeiten','app':'KorpusDB','tabelle':'tbl_antwortmoeglichkeiten','id':'antwortmoeglichkeit','optionen':['liste'],
				 'felder':['+id','Kuerzel','frei','|Reihung=auto:reihung','|zu_Aufgabe=parent:id']},
				{'titel':'Aufgabenfiles','app':'KorpusDB','tabelle':'tbl_aufgabenfiles','id':'aufgabenfiles','optionen':['liste'],
				 'felder':['+id','id_Mediatyp','ist_Anweisung','File_Link','Kommentar','|Reihung=auto:reihung','|id_Aufgabe=parent:id']}
			 ]
			},
			{'titel':'Aufgabenzusammenstellung','app':'KorpusDB','tabelle':'tbl_aufgabenzusammenstellungen','id':'aufgabenzusammenstellung','optionen':['einzeln'],
			 'felder':['+id=parent:zusammengestellt_als','Bezeichnung_AZus','Kommentar','AZusCol'],
			 'sub':[
				{'titel':'Beinhaltete Medientypen','app':'KorpusDB','tabelle':'tbl_azusbeinhaltetmedien','id':'azusbeinhaltetmedien','optionen':['liste'],
				 'felder':['+id','id_Mediatyp','|Reihung=auto:reihung','|id_AZus=parent:id']}
			 ]
			}
		 ]
		}
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)

def tagsedit(request):
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'KorpusDB'
	tabelle_name = 'tbl_tags'
	permName = 'tags'
	primaerId = 'tags'
	aktueberschrift = 'Tags'
	asurl = '/korpusdb/tagsedit/'
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [
		{'titel':'Tag','titel_plural':'Tags','app':'KorpusDB','tabelle':'tbl_tags','id':'tags','optionen':['einzeln','elementFrameless'],
		 'felder':['+id','Tag','Tag_lang','zu_Phaenomen','Kommentar','Generation','AReihung'],
		 'sub':[
			{'titel':'Tag Familie - Parent','titel_plural':'Tag Familie - Parents','app':'KorpusDB','tabelle':'tbl_tagfamilie','id':'tagfamilieparents','optionen':['liste','elementeclosed'],
			 'felder':['+id','|id_ChildTag=parent:id','id_ParentTag'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_ParentTag">{% getFeldVal aData.felder \'id_ParentTag\' %}</span>',
			},
			{'titel':'Tag Familie - Child','titel_plural':'Tag Familie - Childs','app':'KorpusDB','tabelle':'tbl_tagfamilie','id':'tagfamiliechilds','optionen':['liste','elementeclosed'],
			 'felder':['+id','|id_ParentTag=parent:id','id_ChildTag'],
#			 'feldoptionen':{'id_ChildTag':{'foreignkey_select':{'data':{'generation':'Generation'},'select_data':{'tagedit':'+1','taggentar':'#fid_Generation_1_1'}},}},
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_ChildTag">{% getFeldVal aData.felder \'id_ChildTag\' %}</span>',
			},
			{'titel':'Tag Ebene zu Tag','titel_plural':'Tag Ebenen zu Tag','app':'KorpusDB','tabelle':'tbl_tagebenezutag','id':'tagebenezutag','optionen':['liste','elementeclosed'],
			 'felder':['+id','|id_Tag=parent:id','id_TagEbene'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_TagEbene">{% getFeldVal aData.felder \'id_TagEbene\' %}</span>',
			},
		 ],
		 'suboption':['tab'],
#		 'addJS':[{'static':'korpusdbmaske/js/tagedit.js'},],
		},
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)

def presettagsedit(request):
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'KorpusDB'
	tabelle_name = 'sys_presettags'
	permName = 'presettags'
	primaerId = 'presettags'
	aktueberschrift = 'Tags'
	asurl = '/korpusdb/presettagsedit/'
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [
		{'titel':'Preset Tags','titel_plural':'Presets Tags','app':'KorpusDB','tabelle':'sys_presettags','id':'presettags','optionen':['einzeln','elementFrameless'],
		 'felder':['+id','Bezeichnung','Kommentar','Reihung'],
		 'sub':[
			{'titel':'Tag zu Preset Tags','titel_plural':'Tags zu Preset Tags','app':'KorpusDB','tabelle':'sys_tagszupresettags','id':'tagszupresettags','optionen':['liste','elementeclosed'],
			 'felder':['+id','|id_PresetTags=parent:id','id_Tag','|Reihung=auto:reihung'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_Tag">{% getFeldVal aData.felder \'id_Tag\' %}</span>',
			},
			{'titel':'Tag Ebene zu Preset Tags','titel_plural':'Tag Ebenen zu Preset Tags','app':'KorpusDB','tabelle':'sys_tagebenezupresettags','id':'tagebenezupresettags','optionen':['liste','elementeclosed'],
			 'felder':['+id','|id_PresetTags=parent:id','id_TagEbene'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_TagEbene">{% getFeldVal aData.felder \'id_TagEbene\' %}</span>',
			},
			{'titel':'Preset Tags zu Aufgabe','titel_plural':'Presets Tags zu Aufgabe','app':'KorpusDB','tabelle':'sys_presettagszuaufgabe','id':'presettagszuaufgabe','optionen':['liste','elementeclosed'],
			 'felder':['+id','|id_PresetTags=parent:id','id_Aufgabe'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_Aufgabe">{% getFeldVal aData.felder \'id_Aufgabe\' %}</span>',
			},
		 ],
		 'suboption':['tab']
		}
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)

def inferhebung(request):
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'KorpusDB'
	tabelle_name = 'tbl_inferhebung'
	permName = 'aufgabensets'
	primaerId = 'inferhebung'
	aktueberschrift = 'InfErhebungen'
	asurl = '/korpusdb/inferhebung/'
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')
	# erhInfAufgabe für Fragebögen erstellen:
	if 'erhinfaufgabefxfunction' in request.POST and int(request.POST.get('erhinfaufgabefxfunction')) == 1:
		from django.apps import apps
		import datetime
		useArtErhebung = [6,7]
		info+='<b>ErhInfAufgabe aktuallisieren:</b><br>'
		aElement = apps.get_model(app_name, tabelle_name).objects.get(pk=int(request.POST.get('gettableview')))
		for aErhMitAufg in aElement.ID_Erh.tbl_erhebung_mit_aufgaben_set.all():
			info+=str(aErhMitAufg)+' - '
			if KorpusDB.tbl_erhinfaufgaben.objects.filter(id_Aufgabe=aErhMitAufg.id_Aufgabe.pk,id_InfErh=aElement.pk).count()>0:
				info+='<i>bereits vorhanden.</i>'
			else:
				asErhinfaufgaben = KorpusDB.tbl_erhinfaufgaben()
				asErhinfaufgaben.id_Aufgabe = aErhMitAufg.id_Aufgabe
				asErhinfaufgaben.id_InfErh = aElement
				asErhinfaufgaben.start_Aufgabe = datetime.timedelta(microseconds=0)
				asErhinfaufgaben.stop_Aufgabe = datetime.timedelta(microseconds=0)
				asErhinfaufgaben.save()
				info+='<b>erstellt.</b>'
			info+='<br>'

	# Einstellungen:
	InlineAudioPlayer = loader.render_to_string('korpusdbmaske/fxaudioplayer.html',
		RequestContext(request, {'audioDir':'select[name="Dateipfad"]','audioFile':'select[name="Audiofile"]', 'audioPbMarker':['input[name="time_beep"]','input[name="sync_time"]']}),)
	from DB.funktionenDateien import getPermission, scanFiles, scanDir, removeLeftSlash, tree2select
	from django.conf import settings
	import os
	mDir = getattr(settings, 'PRIVATE_STORAGE_ROOT', None)
	if not mDir:
		return HttpResponseServerError('PRIVATE_STORAGE_ROOT wurde nicht gesetzt!')
	def dateipfadFxfunction(aval,siblings,aElement):
		adir = removeLeftSlash(aval['value'])
		adirABS = os.path.normpath(os.path.join(mDir,adir))
		if not os.path.isdir(adirABS):
			aval['feldoptionen']['fxtype']['danger'] = 'Verzeichnis existiert nicht!'
		if not getPermission(adir,mDir,request)>0:
			aval['feldoptionen']['fxtype']['type'] = 'blocked'
		else:
			aselect = tree2select(scanDir(mDir,None,request))
			isInList = False
			aval['value'] = os.path.normpath(removeLeftSlash(aval['value']))
			for aselectitm in aselect:
				if aval['value'] == aselectitm['value']:
					isInList = True
					aval['value'] = aval['value']
					break
			if not isInList:
				aselect = [{'title':os.path.normpath(aval['value']),'value':os.path.normpath(aval['value'])}] + aselect
			aval['feldoptionen']['fxtype']['type'] = 'select'
			aval['feldoptionen']['fxtype']['showValue'] = True
			aval['feldoptionen']['fxtype']['select'] = aselect
		return aval
	def audiofileFxfunction(aval,siblings,aElement):
		aFile = removeLeftSlash(aval['value'])
		aDir = ''
		for aFeld in siblings:
			if aFeld['name']=='Dateipfad':
				aDir = removeLeftSlash(aFeld['value'])
				break
		aFileABS = os.path.normpath(os.path.join(mDir,aDir,aFile))
		if not os.path.isfile(aFileABS):
			aval['feldoptionen']['fxtype']['danger'] = 'Verzeichnis existiert nicht!'
		if not getPermission(aDir,mDir,request)>0:
			aval['feldoptionen']['fxtype']['type'] = 'blocked'
		else:
			aselect = []
			isInList = False
			if os.path.isdir(os.path.normpath(os.path.join(mDir,aDir))):
				for aFile in scanFiles(aDir,mDir,request):
					aselect.append({'title':aFile['name'],'value':aFile['name']})
					if aFile['name'] == aval['value']:
						isInList = True
			if not isInList:
				aselect = [{'title':aval['value'],'value':aval['value']}] + aselect
			aval['feldoptionen']['fxtype']['type'] = 'select'
			aval['feldoptionen']['fxtype']['select'] = aselect
		return aval
	# erhInfAufgabe für Fragebögen:
	def erhInfAufgabeFxfunction(aval,siblings,aElement):
		aView_html = '<div></div>'
		useArtErhebung = [6,7]
		aErh = findDicValInList(siblings,'name','ID_Erh')
		if 'value' in aErh and aErh['value'] and aErh['value'].Art_Erhebung.pk in useArtErhebung:
			# ErhInfAufgaben
			aView_html = loader.render_to_string('inferhebung/erhinfaufgabefxfunction0.html',
				RequestContext(request, {'erhinfaufgabenCount':aElement.tbl_erhinfaufgaben_set.count(),'erhebungMitAufgabenCount':aErh['value'].tbl_erhebung_mit_aufgaben_set.count()}),)
		aval['feldoptionen'] = {'view_html':aView_html,'edit_html':'<div></div>'}
		return aval
	dateipfadFxType = {'fxtype':{'fxfunction':dateipfadFxfunction},'nl':True}
	audiofileFxType = {'fxtype':{'fxfunction':audiofileFxfunction},'nl':True}
	erhInfAufgabeFxType = {'fxtype':{'fxfunction':erhInfAufgabeFxfunction},'nl':True,'view_html':'<div></div>','edit_html':'<div></div>'}
	aufgabenform = [
		{'titel':'InfErhebung','titel_plural':'InfErhebungen','app':'KorpusDB','tabelle':'tbl_inferhebung','id':'inferhebung','optionen':['einzeln','elementFrameless'],
		 'felder':['+id','ID_Erh','ID_Inf','Datum','Explorator','Kommentar','Dateipfad','Audiofile','time_beep','sync_time','Logfile','Ort','Besonderheiten','!Audioplayer','!ErhInfAufgabe'],
		 'feldoptionen':{'Audioplayer':{'view_html':'<div></div>','edit_html':InlineAudioPlayer},'Dateipfad':dateipfadFxType,'Audiofile':audiofileFxType,'ErhInfAufgabe':erhInfAufgabeFxType,},
		 'addCSS':[{'static':'korpusdbmaske/css/fxaudioplayer.css'},],
		 'addJS':[{'static':'korpusdbmaske/js/fxaudioplayer.js'},{'static':'korpusdbmaske/js/fxerhinfaufgabe.js'},],
		 'import':{
		 	'enabled':True,
			'csvImportData':{
				'selectby':'tableField',
				'selectField':'ID_Erh__Art_Erhebung__pk',
				'select':{
					3:{
						'cols':{
							'ID_Aufgabe':{				# Aufgaben ID
								'errorCheck': [{'type':'pkInTable','app':'KorpusDB','table':'tbl_aufgaben'}]
							},
							'count_BlackKon':{			# Reihenfolge der Aufgabe
								'convert': [{'type':'int'}]
							},
							'datetime': {				# Zeitpunkt der Erhebung
								'convert': [{'type':'datetime'}],
								'errorCheck': [{'type':'datetime'},{'type':'colAlwaysSame'}]
							},
							'logfile': {				# Eigener Filename; sollte hinweis geben, zu welchem Ort die Erhebung ist, und zu welcher Person (letzte drei Ziffern = Inf_Sigle)
								'convert': [{'type':'trim'}],
								'errorCheck': [{'type':'colAlwaysSame'}]
							},
							'subject_nr': {				# Inf_sigle (sollte Inf_sigle von Inf_erh entsprechen)
								'convert': [{'type':'trim'}],
								'errorCheck': [{'type':'colAlwaysSame'}]
							},
							'time_Blackscreen': {		# Das ist die Zeit einer Einzelaufgabe; also Startzeit der Einzelaufgabe; als Endzeit nehme ich dann immer die Zeit der nächsten Aufgabe; außer bei der letzten, da rechen ich einfach + 2 Sekunden (man könnte bis zum Aufnahmeende machen); die Startzeit stimmt nicht, wenn die Aufgabe wiederholt wurde; bzw. muss die Endzeit von der übernächsten Zeile (also wenn es eine andere Aufgabe ist) genommen werden
								'convert': [{'type':'duration'}]
							},
							'time_Blackscreen_1': {		# das ist nur für das erste SET die Zeiten
								'convert': [{'type':'duration'}],
								'errorCheck': [{'type':'convert'}]
							},
							'time_Logg_all': {			# Ich denke, auch das könnte als Endzeitpunkt für eine Einzelaufgabe genommen werden; ist vielleicht sogar exakter; müssen wir ausprobieren, sieht aber relativ gut aus
								'convert': [{'type':'duration'}],
								'errorCheck': [{'type':'convert'}]
							},
							'time_beep': {				# TIME_BEEP! Das so in tbl_inferhebung übernehmen; die Synctime müssen die Leute selbst eingeben
								'convert': [{'type':'duration'}],
								'errorCheck': [{'type':'convert'},{'type':'colAlwaysSame'}]
							}
						},
						'import':{
							'once': [
								{
									'type':'update',
									'table':'!this',
									'errorCheck':[{'type':'issame','is':'!this__ID_Inf__inf_sigle=subject_nr|rjust:4,0','warning':True}],
									'fields':{
										'Datum':'datetime',
										'time_beep':'time_beep',
										'Logfile':'logfile',
									}
								}
							],
							'perrow': [
								{
									'type':'new',
									'table':'KorpusDB>tbl_erhinfaufgaben',
									'errorCheck':[{'type':'notInDB','fields':{'id_InfErh_id','id_Aufgabe_id'},'warning':True}],
									'fields':{
										'id_InfErh_id':'!this__pk',
										'id_Aufgabe_id':'ID_Aufgabe',
										'Reihung':'count_BlackKon',
										'start_Aufgabe':'firstVal|time_Blackscreen,time_Blackscreen_1',
										'stop_Aufgabe':'time_Logg_all',
									}
								}
							]
						}
					}
				}
			}
		 },
		},
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)

# Eingabemaske: EingabeSPT - ipk=tbl_informanten, apk=tbl_aufgaben
def maske(request,ipk=0,apk=0):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dissdb_login')
	if not request.user.has_perm('KorpusDB.antworten_maskEdit'):
		return redirect('Startseite:start')
	from .view_maske import view_maske
	return view_maske(request,ipk,apk)

# Eingabemaske: EingabeFB - ipk=tbl_informanten, apk=tbl_aufgaben
def maske2(request,ipk=0,apk=0):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dissdb_login')
	if not request.user.has_perm('KorpusDB.antworten_maskEdit'):
		return redirect('Startseite:start')
	from .view_maske2 import view_maske2
	return view_maske2(request,ipk,apk)

# Auswertung
def auswertung(request):
	info = ''
	error = ''
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dissdb_login')
	if not request.user.has_perm('KorpusDB.auswertung'):
		return redirect('Startseite:start')
	asurl = '/korpusdb/auswertung/'
	auswertungen = [{'id':'antworten','titel':'Antworten','app_name':'KorpusDB','tabelle_name':'tbl_antworten',
					 'felder':['id','ist_bfl','bfl_durch_S','ist_Satz_id','ist_Satz__Transkript','ist_Satz__Standardorth','ist_Satz__Kommentar','tbl_antwortentags_set__!TagListeF','tbl_antwortentags_set__!TagListeFid','von_Inf_id','von_Inf__inf_sigle','von_Inf__id_person__geb_datum','von_Inf__id_person__weiblich','von_Inf__inf_gruppe__gruppe_bez','von_Inf__inf_ort','Kommentar','zu_Aufgabe_id','zu_Aufgabe__Beschreibung_Aufgabe','zu_Aufgabe__von_ASet_id','zu_Aufgabe__von_ASet__Kuerzel'],
					 'filter':[[{'id':'erhebungen','field':'>KorpusDB|tbl_erhebungen','type':'select','selectFilter':{'Art_Erhebung__gt':2},'queryFilter':'zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__pk','verbose_name':'Erhebung'},
								{'id':'aufgabenset','field':'zu_Aufgabe__von_ASet','type':'select','selectFilter':{'tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk':'!erhebungen'},'queryFilter':'zu_Aufgabe__von_ASet__pk','verbose_name':'Aufgabenset'},
								#{'field':'zu_Aufgabe','type':'select','selectFilter':{'zu_Aufgabe__von_ASet':'!aufgabenset'},'queryFilter':'zu_Aufgabe__pk','verbose_name':'Aufgabe'}
							  ]],
					 #'orderby':{'id':['id']},
					},
					{'id':'antwortenTagEbenen','titel':'Antworten (Tag Ebenen)','app_name':'KorpusDB','tabelle_name':'tbl_antworten',
					 'felder':['id','ist_bfl','bfl_durch_S','ist_Satz_id','ist_Satz__Transkript','ist_Satz__Standardorth','ist_Satz__Kommentar','tbl_antwortentags_set__!TagEbenenF','tbl_antwortentags_set__!TagEbenenFid','von_Inf_id','von_Inf__inf_sigle','von_Inf__id_person__geb_datum','von_Inf__id_person__weiblich','von_Inf__inf_gruppe__gruppe_bez','von_Inf__inf_ort','Kommentar','zu_Aufgabe_id','zu_Aufgabe__Beschreibung_Aufgabe','zu_Aufgabe__von_ASet_id','zu_Aufgabe__von_ASet__Kuerzel'],
					 'filter':[[{'id':'erhebungen','field':'>KorpusDB|tbl_erhebungen','type':'select','selectFilter':{'Art_Erhebung__gt':2},'queryFilter':'zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__pk','verbose_name':'Erhebung'},
								{'id':'aufgabenset','field':'zu_Aufgabe__von_ASet','type':'select','selectFilter':{'tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk':'!erhebungen'},'queryFilter':'zu_Aufgabe__von_ASet__pk','verbose_name':'Aufgabenset'},
							  ]],
					},
					# {'id':'informantenErhoben','titel':'Informanten (Erhoben)','app_name':'PersonenDB','tabelle_name':'tbl_informanten',
					#  'felder':['id','inf_sigle'],
					#  'sub':[
					#  	{'app_name':'KorpusDB','tabelle_name':'tbl_aufgaben','where':['tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk=parent:id'],
					# 	 'felder':['id','Beschreibung_Aufgabe'],
					# 	},
					#  ]
					# },
				   ]
	return auswertungView(auswertungen,asurl,request,info,error)

def erhobeneInformanten(request,xls='0'):
	import PersonenDB.models as PersonenDB
	info = ''
	error = ''
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dissdb_login')

	xls=int(xls)
	lines = [['Inf. Id','Inf. Sigle','Aufg. ID','Aufgaben Beschreibung','Antworten']]
	adg=0
	for aInf in PersonenDB.tbl_informanten.objects.all():
		aLine = [aInf.id,aInf.inf_sigle]
		for aAufgabe in KorpusDB.tbl_aufgaben.objects.filter(tbl_erhinfaufgaben__id_InfErh__ID_Inf = aInf.id).order_by('Beschreibung_Aufgabe'):
			aAntwortenCount = KorpusDB.tbl_antworten.objects.filter(zu_Aufgabe=aAufgabe.id,von_Inf=aInf.id).count()
			lines.append(aLine + [aAufgabe.id,aAufgabe.Beschreibung_Aufgabe,aAntwortenCount])
			adg+=1
			if adg > 29 and xls == 0:
				break
		if adg > 29 and xls == 0:
			break
	if xls == 1:
		from django.http import HttpResponse, HttpResponseNotFound
		import xlwt
		response = HttpResponse(content_type='text/ms-excel')
		response['Content-Disposition'] = 'attachment; filename="erhobene_informanten.xls"'
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet('Erhobene Informanten')
		row_num = 0
		font_style = xlwt.XFStyle()
		for obj in lines:
			row_num += 1
			row = obj
			for col_num in range(len(row)):
				ws.write(row_num, col_num, row[col_num], font_style)
		wb.save(response)
		return response
	# Ausgabe der Seite
	return render_to_response('korpusdbmaske/erhobene_informanten.html',
		RequestContext(request, {'lines':lines,'error':error,'info':info}),)


### Funktionen: ###
