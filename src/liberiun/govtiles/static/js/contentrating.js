$(document).ready(function () {
	
	$('div.rating').raty({ 
        starType: 'i',
        hints: ['péssimo', 'ruim', 'regular', 'bom', 'ótimo'],
        click: function(rate, ev){
        	
        	
        	
        }
    });
	
	$('div.rating')
	.each(function(){
		$(this).raty('score', $(this).attr('data-rating'));
	});
	
});