String.prototype.hashCode = function() {
    var hash = 0, i, chr;
    if (this.length === 0) return hash;
    for (i = 0; i < this.length; i++) {
      chr   = this.charCodeAt(i);
      hash  = ((hash << 5) - hash) + chr;
      hash |= 0; // Convert to 32bit integer
    }
    return hash;
};

defaultConfig = {
    maxColWidth: 400,
    minColWidth: 50
}

Object.assign(config, defaultConfig);
Object.keys(config).forEach(key=>{
    if(key.charAt(key.length - 1) === 's'){
        config[key.slice(0, -1)] = config[key]
    }
});

$(function () {
    $('.table').colResizable({
        liveDrag: true,
        resizeMode: 'overflow',
        onDrag: ()=>{
            const $body = $('body');
            const maxWidth = $(this).width();
            if($body.width() < maxWidth){
                $body.width(maxWidth);
            }
        }
    });

    // $('body').removeAttr('style');
});

makeTable(config);

function makeTable(config){
    const colHeader = config.colHeader;

    let table = document.createElement('table');
    table.className = 'table table-striped table-bordered';
    
    let thead = document.createElement('thead');
    let tr = document.createElement('tr');

    colHeader.forEach(key=>{
        let th = document.createElement('th');
        th.scope = 'col';
        th.id = 'col' + key.hashCode();

        switch(whatIsIt(config.maxColWidth)){
            case "Object":
                th.style.maxWidth = config.maxColWidth[key] + 'px';
                break;
            case "string":
                th.style.maxWidth = config.maxColWidth;
                break;
            case "number":
                th.style.maxWidth = config.maxColWidth + 'px';
                break;
        }

        switch(whatIsIt(config.minColWidth)){
            case "Object":
                th.style.minWidth = config.minColWidth[key] + 'px';
                break;
            case "string":
                th.style.minWidth = config.minColWidth;
                break;
            case "number":
                th.style.minWidth = config.minColWidth + 'px';
                break;
        }

        if (config.colWidth[key]){
            th.style.maxWidth = (screen.width / 2) + 'px';
        }

        th.innerHTML = key;
        tr.appendChild(th);
    });

    thead.appendChild(tr);
    table.appendChild(thead);

    let tbody = document.createElement('tbody');

    config.data.forEach(record=>{
        let tr = document.createElement('tr');

        colHeader.forEach(key=>{
            let td = document.createElement('td');

            let wrapped = document.createElement('div');
            wrapped.className = 'wrapped'

            let wrapper = document.createElement('div');
            wrapper.className = 'wrapper'

            wrapper.appendChild(wrapped);
            td.appendChild(wrapper);

            switch(whatIsIt(record[key])){
                case "Object":
                    wrapped.innerHTML = '<pre>' + JSON.stringify(record[key], null, 2) + '</pre>';
                    break;
                case "Array":
                    wrapped.innerHTML = '<pre>' + JSON.stringify(record[key]) + '</pre>';
                    break;
                case "number":
                    wrapped.textContent = record[key];
                    break;
                case "string":
                    switch(whatIsIt(config.renderer)){
                        case "Object":
                            switch(config.renderer[key]){
                                case 'html':
                                    wrapped.innerHTML = record[key];
                                    break;
                                default:
                                    wrapped.innerHTML = textToHTML(record[key]);
                            }
                            break;
                        case "string":
                            switch(config.renderer) {
                                case 'html':
                                    wrapped.innerHTML = record[key];
                                    break;
                                default:
                                    wrapped.innerHTML = textToHTML(record[key]);
                            }
                            break;
                        default:
                            wrapped.innerHTML = textToHTML(record[key]);
                    }
                    break;
                default:
                    if(record[key]) wrapped.innerHTML = textToHTML(record[key]);
            }

            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    table.appendChild(tbody);
    document.getElementById('tableArea').appendChild(table);

    let style = document.createElement('style');
    document.head.appendChild(style);
    style.sheet.insertRule(`
    .wrapper {
        max-height: ${config.maxRowHeight}px;
    }
    `, 0);

    let totalWidth = 0;
    
    colHeader.forEach(key=>{
        const el = document.getElementById('col' + key.hashCode());

        if (config.colWidth[key]){
            el.style.width = config.colWidth[key] + 'px';
            totalWidth += config.colWidth[key];
        } else {
            let width = el.clientWidth;

            const maxWidth = parseFloat(el.style.maxWidth);
            const minWidth = parseFloat(getComputedStyle(el).fontSize) * el.textContent.length;
            if (width > maxWidth) width = maxWidth;
            else if (width < minWidth) width = minWidth;

            el.style.width = width + 'px';
            totalWidth += width;
        }
    });

    document.getElementById('body').style.width = totalWidth + 'px';
}

function whatIsIt(object) {
    var arrayConstructor = [].constructor;
    var objectConstructor = {}.constructor;

    if (object === null) {
        return "null";
    } 
    else if (object === undefined) {
        return "undefined";
    }
    else if (object.constructor === arrayConstructor) {
        return "Array";
    }
    else if (object.constructor === objectConstructor) {
        return "Object";
    }
    else {
        return typeof object;
    }
}

function textToHTML(text)
{
    return ((text || "") + "")  // make sure it is a string;
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\t/g, "    ")
        .replace(/ /g, "&#8203;&nbsp;&#8203;")
        .replace(/\r\n|\r|\n/g, "<br />");
}
