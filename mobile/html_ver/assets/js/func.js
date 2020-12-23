function new_node(tagname, { classlist = [], ...properties }) {
    let node = document.createElement(tagname);
    if (classlist.length) classlist.forEach(name => node.classList.add(name));
    if (properties) {
        Object.keys(properties).forEach(property => {
            node[property] = properties[property];
        });
    }
    return node;
}

function get(selector) {
    let list = document.querySelectorAll(selector);
    if (list.length == 1) return list[0];
    else return list;
}

function load_storage() {
    if (!localStorage.data || localStorage.data.length <= 2) return;
    let data = JSON.parse(localStorage.data);

    Object.keys(data).forEach(id => {

        add_new_device(data[id].name, id);

        Object.keys(data[id]).forEach(property => {
            get_device()[property] = data[id][property];
        });

    });

    load_status();

}

function update_storage() {
    let data = {};

    for (let option of get(`#device_list`).options) {
        data[option.id] = {};

        let type_list = ["current", "relay", "limit"];
        type_list.forEach(type => {
            if (option[type]) data[option.id][type] = option[type];
        });

        data[option.id].name = option.name;
    }

    localStorage.data = JSON.stringify(data);

    if (!get(`#device_list`).length) get(`#delete`).disabled = true;
    else get(`#delete`).disabled = false;
}