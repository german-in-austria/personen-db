/* Variablen */
var unsavedAntworten = 0;
var unsavedEIAufgabe = 0;

(function($){jQuery(document).ready(function($){
	/* Inits */
	loadMitErhebungen()
	setMitErhebungen()
	resetReihungAntworten()

	/* Tastenkürzel */
	Mousetrap.bind('ctrl+e', function(e) { return false; })
	Mousetrap.bind('ctrl+s', function(e) { $('#antwortensave').click(); return false; })

	/* On */
	/* Allgemein */
	window.onbeforeunload = function () {
		if(unsavedAntworten!=0 || unsavedEIAufgabe!=0) {
			return 'Es gibt noch ungespeicherte Veränderungen! Wirklich verwerfen?'
		}
	}
	$(document).on('click','.lmfabc',function(e){
		e.preventDefault()
		if((unsavedAntworten==0 && unsavedEIAufgabe==0) || confirm('Es gibt noch ungespeicherte veränderungen! Wirklich verwerfen?')) {
			unsavedAntworten=0
			unsavedEIAufgabe=0
			$('.lmfabc').removeClass('open')
			$(this).addClass('open')
			$.post($(this).attr('href'),{ csrfmiddlewaretoken: csrf }, function(d) {
				$('.mcon').html(d)
			}).fail(function(d) {
				alert( "error" )
				console.log(d)
			})
		}
	})
	$(document).on('change','#mitErhebungen',setMitErhebungen)
	$(document).on('change','#ainformantErhebung',updateAinformantErhebung)
	/* Formular */
	$(document).on('click','.antwort .antwortreihunghoch:not(.disabled), .antwort .antwortreihungrunter:not(.disabled)',antwortReihungHochRunterClick)
	$(document).on('change','#selaufgabe select:not(.noupdate)',ausgewaehlteAufgabeChange)
	$(document).on('click','#erhinfaufgaben',erhInfAufgabenClick)
	$(document).on('click','#antwortensave:not(.disabled)',antwortenSpeichernClick)

});})(jQuery);
