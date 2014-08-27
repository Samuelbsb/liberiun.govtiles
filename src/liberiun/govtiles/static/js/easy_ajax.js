$(document).ready(function () {
    $(document).on('click', 'a[ajax-id]', function(ev){
        ev.preventDefault();
        
        var $this = $(this),
            url = $this.attr('ajax-url'),
            ajax_id = $this.attr('ajax-id'),
            ajax_filter = $this.attr('ajax-filter'),
            ajax_evaljs = $this.attr('ajax-evaljs');
        
        if(ajax_id) {
            $container_ajax = $('[ajax-content="'+ajax_id+'"]');

            $.ajax({
                url: url,
                success: function(data){
                    if(ajax_filter) {
                    	try{
                    		var dom = $.parseHTML(data);
                    	}catch (e) {
                    		var dom = $(data);
						}
                    	data = $('[ajax-content="'+ajax_filter+'"]', dom)
                    	if (!data) {
                    		data = dom.filter('[ajax-content="'+ajax_filter+'"]')
                    	}
                        data = data.contents();
                    }
                    
                    if(ajax_evaljs) {
                        $.get(ajax_evaljs, function(result){
                           $.globalEval(result); 
                        });
                    }
                    
                    $container_ajax.html(data);
                }
            });
        }
    });
});