// this script requires jQuery
$(document).ready(function() {
    Footnotes.setup();
});

var Footnotes = {
    footnotetimeout: false,
    setup: function() {
        var footnotelinks = $(".footnote-ref")
        
        footnotelinks.unbind('mouseover',Footnotes.footnoteover);
        footnotelinks.unbind('mouseout',Footnotes.footnoteoout);
        
        footnotelinks.bind('mouseover',Footnotes.footnoteover);
        footnotelinks.bind('mouseout',Footnotes.footnoteoout);

		footnotelinks.html('<i class="fa fa-question"></i>')
    },
    footnoteover: function() {
        clearTimeout(Footnotes.footnotetimeout);
        $('#footnotediv').stop();
        $('#footnotediv').remove();
        
        var id = $(this).attr('href').substr(1);
        var position = $(this).offset();
    
        var div = $(document.createElement('div'));
        div.attr('id','footnotediv');
        div.bind('mouseover',Footnotes.divover);
        div.bind('mouseout',Footnotes.footnoteoout);

        var el = document.getElementById(id);
        div.html($(el).html());
        
        div.css({
            position:'absolute',
            width:'300px',
      		background:'white',
      		border:'solid 1px',
      		'font-size':'90%',
      		'line-height':1.4,
      		'-moz-border-radius':'.5em',
      		'-webkit-border-radius':'.5em',
      		'border-radius':'.5em',
      		opacity:0.95
        });
        $(document.body).append(div);

        var left = position.left;
        if(left + 420  > $('.FixedHeightContainerText').width())
            left = $('.FixedHeightContainerText').width() - 220;
        var top = position.top+20;
        if(top + div.height() > $('.FixedHeightContainerText').height())
            top = position.top - div.height() - 15;
        div.css({
            left:left,
            top:top
        });
    },
    footnoteoout: function() {
        Footnotes.footnotetimeout = setTimeout(function() {
            $('#footnotediv').animate({
                opacity: 0
            }, 600, function() {
                $('#footnotediv').remove();
            });
        },100);
    },
    divover: function() {
        clearTimeout(Footnotes.footnotetimeout);
        $('#footnotediv').stop();
        $('#footnotediv').css({
                opacity: 0.9
        });
    }
}	