function getComputedTranslateXY(obj)
{
	const transArr = [];
    if(!window.getComputedStyle) return;
    const style = getComputedStyle(obj),
        transform = style.transform || style.webkitTransform || style.mozTransform;
    let mat = transform.match(/^matrix3d\((.+)\)$/);    
    if(mat) return parseFloat(mat[1].split(', ')[13]);
    mat = transform.match(/^matrix\((.+)\)$/);
    mat ? transArr.push(parseFloat(mat[1].split(', ')[4])) : 0;
    mat ? transArr.push(parseFloat(mat[1].split(', ')[5])) : 0;
    return transArr;
}


var createMapThumbnail = function(obj_id) {
    var xmap = ($('.leaflet-tile-pane')[0] != undefined ? $('.leaflet-tile-pane') : $('#mapstore2-embedded'));
    height = $('#mapstore2-embedded').height();
    width = $('#mapstore2-embedded').width();
    xOffset = Math.abs((width - 512)/2);
    var map = xmap.clone();
    let styleMap = ($(".leaflet-map-pane").attr('style') || "" ).replace(/transform: translate3d\(([^,a-b]+)[^)] ([^,a-b]+)[^)]*\)/g,  (s, p1, p2) => {
        return `left: ${parseInt(p1) - xOffset}px; top: ${parseInt(p2)}px;`;
    } );
    map.find('*').each(function(i) {
        e = $(this);
        if(e.css('display') === 'none' ||
            // leaflet
            ($('.leaflet-tile-pane')[0] != undefined && e.attr("class") !== undefined &&
                ((e.attr("class").indexOf('leaflet-layer') < 0 && e.attr("class").indexOf('leaflet-tile') < 0) ||
                 e.attr("class").indexOf('x-') >= 0)) ||
            // OpenLayers
            ($('.olMapViewport')[0] != undefined && e.attr("class") !== undefined &&
                (e.attr("class").indexOf('olControl') >= 0 ||
                 e.attr("class").indexOf('olImageLoadError') >= 0 ||
                 e.attr("class").indexOf('ol-overlaycontainer') >= 0 ||
                 e.attr("class").indexOf('x-') >= 0))
        ) {
            e.remove();
        } else if (e.attr('src') !== undefined) {
            if (e.attr('src').indexOf('images/default') > 0 || e.attr('src').indexOf('default/img') > 0) {
                e.remove();
            }
            if (!e.attr('src').startsWith("http")) {
                var href = e.attr('src');
                e.attr('src', 'http:' + href);
            }
            let style = e.attr('style').replace(/transform: translate3d\(([^,a-b]+)[^)] ([^,a-b]+)[^)]*\)/g,  (s, p1, p2) => {
                    return `left: ${parseInt(p1)}px; top: ${parseInt(p2)}px;`;
                } );
            e.attr('style', style);
            e.css({
                "visibility":"inherit",
                "position":"absolute",
                
            });
        }else if (e.attr("class").indexOf('leaflet-tile-container') >= 0) {
            let style = e.attr('style').replace(/transform: translate3d\(([^,]+)[^)] ([^,]+)[^)]*\)/g,(s, p1, p2) => {
                return `left: ${parseInt(p1)}px; top: ${parseInt(p2)}px;`;
            });
            e.attr('style', style);
            e.css({
                "visibility":"inherit",
                "position":"absolute"        
            });
        }else {
            e.removeAttr("id");
        }
    });

    var url = window.location.pathname.replace('/view', '');
        url = url.replace('/edit', '');
        url = url.replace('/metadata', '');
        url = url.replace('/metadata#', '');

    if (typeof obj_id != 'undefined' && url.indexOf('new')){
        url = url.replace('new', obj_id);
    }

    url += '/thumbnail';
    var body = `<div style='overflow: hidden; position:absolute; top:0px; left:0px; height: ${height}px; width: ${width}px;'><div style="position: absolute; ${styleMap}">${map.html()}<div/></div>`;
    // wnd =window.open("about:blank", "", "_blank");
    // wnd.document.write(body);
    $.ajax({
        type: "POST",
        url: url,
        data: body,
        async: true,
        cache: false,
        beforeSend: function(){
             // Handle the beforeSend event
             try {
                 $("#_thumbnail_processing").modal("show");
             } catch(err) {
                 console.log(err);
             }
        },
        complete: function(){
             // Handle the complete event
             try {
                 $("#_thumbnail_processing").modal("hide");
             } catch(err) {
                 console.log(err);
             }
        },
        success: function(data, status, jqXHR) {
            try {
                $("#_thumbnail_feedbacks").find('.modal-title').text(status);
                $("#_thumbnail_feedbacks").find('.modal-body').text(data);
                $("#_thumbnail_feedbacks").modal("show");
            } catch(err) {
                console.log(err);
            } finally {
                return true;
            }
        },
        error: function(jqXHR, textStatus){
            try {
                if(textStatus === 'timeout')
                {
                    $("#_thumbnail_feedbacks").find('.modal-title').text('Timeout');
                    $("#_thumbnail_feedbacks").find('.modal-body').text('Failed from timeout: Could not create Thumbnail');
                    $("#_thumbnail_feedbacks").modal("show");
                } else {
                    $("#_thumbnail_feedbacks").find('.modal-title').text('Error: ' + textStatus);
                    $("#_thumbnail_feedbacks").find('.modal-body').text('Could not create Thumbnail');
                    $("#_thumbnail_feedbacks").modal("show");
                }
            } catch(err) {
                console.log(err);
            } finally {
                return true;
            }
        },
        timeout: 60000 // sets timeout to 60 seconds
    });
    return true;
};
