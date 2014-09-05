$(document).ready(function () {
	
	$('div.rating').raty({ 
        starType: 'i',
        hints: ['péssimo', 'ruim', 'regular', 'bom', 'ótimo']
    });
	
	$('div.rating-geral').raty('set', {'readOnly': true});
	
	$('div.my-rating').raty('set', {'click': function(value, ev){
		var url = $(this).attr('data-url');

		$.ajax({
		   url: url,
		   data: {'rate': value},
		   success: function(data){
			   var $dom = $(data);
			   $.get('++resource++liberiun.govtiles/js/contentrating.js', function(result){ 
				   $.globalEval(result); 
			   });
			   $('.rate-container').html($dom.find('.rate-container').contents());
		   }
		});
	}});
	
	$('div.rating')
	.each(function(){
		$(this).raty('set', {'score': $(this).attr('data-rating')});
	});
	
});