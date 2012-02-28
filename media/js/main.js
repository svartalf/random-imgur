$(document).ready(function() {

    (function() {
        var image = $('#image');
        var container = $('#image-container');
        var loader = $('h1').find('small');

        image.bind('load', function() {
            loader.removeClass('loading');
        });

        function update(event) {
            event.preventDefault();
            loader.addClass('loading');
            $.getJSON('/random/', function(response) {
                container.attr('href', response.url);
                image.attr('src', response.image);
                _gaq.push(['_trackEvent', 'images', 'random', response.image]);
            });
        }
        container.bind('click', update);
    })();

    // Check for NSFW cookie
    (function() {
        var cookies = document.cookie.split('; ');
        for (var i=0, cookie; cookie = cookies[i] && cookies[i].split('='); i++) {
            if (cookie[0] == 'show') {
                return;
            }
        }
        // Cookie doesnt exists, showing a warning
        var message = $('#warning');
        var background = $('#warning-bg');
        background.css('width', $(document).width());
        background.css('height', $(window).height());
        message.show();
        background.show();
        message.css('left', ($(document).width()/2)-message.width()/2);
        message.css('top', $(window).height()/2-message.height()/2);
        message.find('button').bind('click', function() {
            message.hide();
            background.hide();
            var date = new Date();
            date.setYear(date.getYear()+1);
            document.cookie = ['show=true', 'expires='+date.toUTCString(), 'path=/', 'domain='].join(';');
        });
    })();

});
