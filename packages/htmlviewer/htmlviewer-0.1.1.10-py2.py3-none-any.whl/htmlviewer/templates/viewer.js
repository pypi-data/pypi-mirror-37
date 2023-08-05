$(function () {
    $(".table").colResizable({
        liveDrag: true,
        resizeMode: 'overflow'
    });
});

makeTable(config);

function makeTable(config){
    const colList = getColList(config.data);

    let table = document.createElement('table');
    table.className = 'table table-striped table-bordered';
    
    let thead = document.createElement('thead');
    let tr = document.createElement('tr');

    colList.forEach(key=>{
        let th = document.createElement('th');
        th.scope = 'col';
        th.className = 'wrapped';
        th.style.maxWidth = config.maxColWidth + 'px';

        if (config.colWidths[key]){
            th.style.width = config.colWidths[key] + 'px';
            th.style.maxWidth = (screen.width / 2) + 'px';
        }

        th.textContent = key;
        tr.appendChild(th);
    });

    thead.appendChild(tr);
    table.appendChild(thead);

    let tbody = document.createElement('tbody');

    config.data.forEach(record=>{
        let tr = document.createElement('tr');

        colList.forEach(key=>{
            let td = document.createElement('td');

            let wrapped = document.createElement('div');
            wrapped.className = 'wrapped'

            let wrapper = document.createElement('div');
            wrapper.className = 'wrapper'

            wrapper.appendChild(wrapped);
            td.appendChild(wrapper);

            switch(whatIsIt(record[key])){
                case "Object":
                    wrapped.textContent = JSON.stringify(record[key], null, 2);
                    break;
                case "Array":
                    wrapped.textContent = JSON.stringify(record[key]);
                    break;
                case "number":
                    wrapped.textContent = record[key];
                    break;
                case "String":
                    if (config.renderers[key] === 'html') {
                        wrapped.innerHTML = record[key];
                    } else {
                        wrapped.textContent = record[key];
                    }
                    break;
                default:
                    if(record[key]) wrapped.textContent = record[key];
            }

            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    table.appendChild(tbody);
    document.getElementById('tableArea').appendChild(table);

    let style = document.createElement('style');
    document.head.appendChild(style);
    style.sheet.insertRule('.wrapper { max-height: '+ config.maxRowHeight + 'px !important; }', 0);
}

function getColList(data){
    let colList = [];

    data.forEach(record=>{
        Object.keys(record).forEach(key=>{
            if(colList.indexOf(key) === -1){
                colList.push(key);
            }
        });
    });

    let rowHeader;

    if(colList.indexOf(config.rowHeader) !== -1){
        rowHeader = config.rowHeader;
    } else {
        for(let key of colList){
            if(/^id(?=[\W_]|$)/i.test(key) || /(?:(?=[\W_]|^).|^)id$/i.test(key)){
                rowHeader = key;
                break;
            }
        }
    }

    if(rowHeader){
        colList.splice(colList.indexOf(rowHeader), 1);
        colList.splice(0, 0, rowHeader);
    }

    return colList;
}

function whatIsIt(object) {
    var stringConstructor = "test".constructor;
    var arrayConstructor = [].constructor;
    var objectConstructor = {}.constructor;

    if (object === null) {
        return "null";
    }
    else if (object === undefined) {
        return "undefined";
    }
    else if (object.constructor === stringConstructor) {
        return "String";
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
