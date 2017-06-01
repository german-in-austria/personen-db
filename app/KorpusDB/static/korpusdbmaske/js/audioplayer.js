/* Variablen */
var audio = new Audio('');
var audioisnewset = 1
var audiomarks = []

/* On */
function progressClick(e){
	var parentOffset = $(this).parent().offset();
	azpos = (e.pageX - parentOffset.left - 15) / $(this).width()
	aspos = durationToSeconds($(this).find('.pb-starttime').html())
	aepos = durationToSeconds($(this).find('.pb-endtime').html())
	audio.currentTime = aspos + ((aepos-aspos) * azpos)
}
function playPauseClick(e){
	var aappgi = $(this).find('.glyphicon')
	if(aappgi.hasClass('glyphicon-play')) {
		audio.play();
	} else {
		audio.pause();
	}
}
function fastBackwardClick(e){
	audio.currentTime = durationToSeconds($('#start_ErhInfAufgaben').val())-syncDiff($("#erhinfaufgaben option:selected"))
}
function fastForwardClick(e){
	audio.currentTime = durationToSeconds($('#stop_ErhInfAufgaben').val())-syncDiff($("#erhinfaufgaben option:selected"))
}
function backwardClick(e){
	audio.currentTime = audio.currentTime-5
}
function forwardClick(e){
	audio.currentTime = audio.currentTime+5
}
function sbackwardClick(e){
	audio.currentTime = audio.currentTime-1
}
function sforwardClick(e){
	audio.currentTime = audio.currentTime+1
}
function stepBackwardClick(e){
	if(audiomarks.length>0) {
		gtt=0
		gtts=999999999999999
		for (i = 0; i < audiomarks.length; ++i) {
			if(audiomarks[i]<(audio.currentTime-1)&&audiomarks[i]>gtt) { gtt = audiomarks[i]; }
			if(audiomarks[i]<gtts) { gtts = audiomarks[i]; }
		}
		if(gtt==0) { gtt=gtts; }
		audio.currentTime = gtt
	}
}
function stepForwardClick(e){
	if(audiomarks.length>0) {
		gtt=999999999999999
		gtts=0
		for (i = 0; i < audiomarks.length; ++i) {
			if(audiomarks[i]>(audio.currentTime)&&audiomarks[i]<gtt) { gtt = audiomarks[i]; }
			if(audiomarks[i]>gtts) { gtts = audiomarks[i]; }
		}
		if(gtt==999999999999999) { gtt=gtts; }
		audio.currentTime = gtt
	}
}

/* Funktionen */
function durationToSeconds(hms) {
	var s = 0.0
	if(hms && hms.indexOf(':')>-1) {
		var a = hms.split(':')
		if(a.length>2) { s+=parseFloat(a[a.length-3]) * 60 * 60; }
		if(a.length>1) { s+=parseFloat(a[a.length-2]) * 60; }
		if(a.length>0) { s+=parseFloat(a[a.length-1]); }
	} else {
		s = parseFloat(hms)
		if(isNaN(s)) { s = 0.0 }
	}
	return s
}
function secondsToDuration(sec) {
	var v = ''
	if(sec<0) { sec = -sec; v = '-' }
	var h = parseInt(sec / 3600)
	sec %= 3600;
	var m = parseInt(sec / 60)
	var s = sec % 60
	return v + ("0" + h).slice(-2) + ':' + ("0" + m).slice(-2) + ':' + ("0" + s.toFixed(6)).slice(-9)
}
function syncDiff(adata) {
	if(durationToSeconds(adata.data('sync_time'))>0) {
		return durationToSeconds(adata.data('time_beep'))-durationToSeconds(adata.data('sync_time'))
	}
	return 0
}
function setAudioMarks() {
	audiomarks = []
	$('#aufgabenprogress .markarea,#inferhebungprogress .markarea').remove()
	if($('.antwort').length>0) {
		aeltuasErh = durationToSeconds($('#start_ErhInfAufgaben').val())-syncDiff($("#erhinfaufgaben option:selected"))
		aeltuaeErh = durationToSeconds($('#stop_ErhInfAufgaben').val())-syncDiff($("#erhinfaufgaben option:selected"))
		aeltualErh = aeltuaeErh-aeltuasErh
		$('#inferhebungprogress').append('<div class="markarea" style="left:'+(100/audio.duration*(aeltuasErh))+'%;width:'+(100/audio.duration*(aeltuaeErh-aeltuasErh))+'%"></div>')
		$('.antwort').each(function() {
			asSec = durationToSeconds($(this).find('input[name="start_Antwort"]').val())
			aeSec = durationToSeconds($(this).find('input[name="stop_Antwort"]').val())
			if(asSec>0 && aeSec>0 && aeSec>asSec && aeSec>=aeltuasErh && aeSec<=aeltuaeErh) {
				audiomarks.push(asSec)
				audiomarks.push(aeSec)
				console.log(asSec+' - '+aeSec)
				$('#aufgabenprogress').append('<div class="markarea" style="left:'+(100/aeltualErh*(asSec-aeltuasErh))+'%;width:'+(100/aeltualErh*(aeSec-asSec))+'%"></div>')
			}
		})
	}
	audiomarks.sort()
}
function setAudioPlayer() {
	if($('#audioplayer').children().length>0) {
		aopt = $('#erhinfaufgaben option:selected')
		$('#start_ErhInfAufgaben').val(secondsToDuration(durationToSeconds(aopt.data('start_aufgabe'))))
		$('#stop_ErhInfAufgaben').val(secondsToDuration(durationToSeconds(aopt.data('stop_aufgabe'))))
		$('#sync_time_ErhInfAufgaben').html(secondsToDuration(durationToSeconds(aopt.data('sync_time'))))
		$('#time_beep_ErhInfAufgaben').html(secondsToDuration(durationToSeconds(aopt.data('time_beep'))))
		$('#syncdiff_ErhInfAufgaben').html(secondsToDuration(-syncDiff(aopt)))
		$('#aufgabenprogress .pb-starttime').html(secondsToDuration(durationToSeconds(aopt.data('start_aufgabe'))-syncDiff(aopt)))
		$('#aufgabenprogress .pb-endtime').html(secondsToDuration(durationToSeconds(aopt.data('stop_aufgabe'))-syncDiff(aopt)))
		var aaudiofile = aopt.data('audiofile')
		audio.pause()
		audio.currentTime = 0
		if(aaudiofile) {
			if(aaudiofile.substr(0,1)=='/' && audiodir.substr(-1)=='/') { aaudiofile = aaudiofile.substr(1) };
			var audiofile = audiodir+aaudiofile
			if(audiofile.length>2) {
				audio.src=audiofile
				audio.load()
			}
			$('#audio-play-pause, #audio-fast-backward, #audio-fast-forward, #audio-backward, #audio-forward, #audio-step-backward, #audio-step-forward').removeAttr('disabled').removeClass('disabled')
		} else {
			$('#audio-play-pause, #audio-fast-backward, #audio-fast-forward, #audio-backward, #audio-forward, #audio-step-backward, #audio-step-forward').attr('disabled','disabled').addClass('disabled')
		}
		audioisnewset = 1
		$('#inferhebungprogress .progress-bar,#aufgabenprogress .progress-bar').css('width','0%')
	}
	unsavedEIAufgabe=0
	$('#eiaufgsave').addClass('disabled')
	setAudioMarks()
}
function progressBarUpdate() {
	$('.pb-akttime').html(secondsToDuration(audio.currentTime))
	if(audioisnewset==0) {
		$('#inferhebungprogress .progress-bar').css('width',(100/audio.duration*audio.currentTime)+'%')
		aeltuasErh = durationToSeconds($('#start_ErhInfAufgaben').val())-syncDiff($("#erhinfaufgaben option:selected"))
		aeltuaeErh = durationToSeconds($('#stop_ErhInfAufgaben').val())-syncDiff($("#erhinfaufgaben option:selected"))
		if(audio.currentTime>=aeltuasErh && audio.currentTime<=aeltuaeErh) {
			$('#aufgabenprogress .progress-bar').css('width',(100/(aeltuaeErh-aeltuasErh)*(audio.currentTime-aeltuasErh))+'%')
		} else if(audio.currentTime<aeltuasErh) {
			$('#aufgabenprogress .progress-bar').css('width','0%')
		} else {
			$('#aufgabenprogress .progress-bar').css('width','100%')
		}
	}
}
setInterval(progressBarUpdate, 50);
audio.addEventListener("durationchange", function() {
	$('#inferhebungprogress .pb-endtime').html(secondsToDuration(audio.duration))
}, false);
audio.addEventListener("play", function() {
	if(audioisnewset==1) {
		setTimeout(function() { audio.currentTime = durationToSeconds($('#erhinfaufgaben option:selected').data('start_aufgabe'))-syncDiff($("#erhinfaufgaben option:selected")); setAudioMarks(); }, 100)
		audioisnewset = 0
	}
	$('#aufgabenprogress .progress-bar, #inferhebungprogress .progress-bar').addClass('active')
	$('#audio-play-pause .glyphicon').addClass('glyphicon-pause').removeClass('glyphicon-play')
}, false);
audio.addEventListener("pause", function() {
	$('#aufgabenprogress .progress-bar, #inferhebungprogress .progress-bar').removeClass('active')
	$('#audio-play-pause .glyphicon').addClass('glyphicon-play').removeClass('glyphicon-pause')
}, false);