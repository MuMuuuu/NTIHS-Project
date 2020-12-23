function add_new_device(input_name = "", input_id = "") {

    let combobox = get(`#device_list`);
    let input = {
        "name": input_name || get(`#input_name`).value,
        "id": input_id || get(`#input_id`).value
    }

    let repeated = [];
    ["name", "id"].forEach(type => {
        for (let option of combobox.options) {
            if (input[type] == option[type]) repeated.push(type);
        }
    });


    if (repeated.length) {
        repeated.forEach(type => {
            get(`#${type}_err_msg`).innerHTML = `repeated ${type}`;
        });
        return;
    }


    let param = {
        "id": input.id,
        "name": input.name,
        "innerHTML": `${input.name}(${input.id})`
    };
    let option = new_node("option", param);

    combobox.add(option);
    combobox.value = param.innerHTML;

    load_status();
    update_storage();
    get(`#change`).disabled = false;
    get(`#set`).disabled = false;
}

function get_device() {
    let device = get(`#device_list`).selectedOptions[0];
    if (!device) return {};
    else return device;
}

function change_limit(val) {
    val == "error" ? val = 0 : val;
    get_device().limit = val;
    get(`#input_limit`).value = val;
    get(`#current`).innerHTML = `0/${val} (mA)`;
    update_storage();
}

function check_input(input) {
    let type = input.id.split("_")[1];
    let err_msg = check(input.value, type);

    input.style.border = `2px solid ${err_msg ? "red" : "black"}`;
    input.invalid = err_msg ? true : false;
    get(`#${type}_err_msg`).innerHTML = err_msg;


    if (type == "name" || type == "id") get(`#add_device`).disabled = get(`#input_name`).invalid || get(`#input_id`).invalid;
    else if (type == "limit") get(`#set`).disabled = get(`#input_limit`).invalid;


    function check(str, type) {

        let reg = {
            "name": /^[A-Za-z0-9 \+\-\*\/\_]{4,30}$/,
            "id": /^[0-4]$/,
            "limit": /^[0-9]{1,}\.{0,1}[0-9]{0,}$/
        };

        let err = {
            "name": "4~30 alphanumeric",
            "id": "1~4 integer",
            "limit": "number (mA)"
        }

        if (!str.match(reg[type])) return err[type];
        else return "";
    }
}

function check_list() {
    if (!get(`#device_list`).length) {
        get(`#add_device`).disabled = true;
        get(`#delete`).disabled = true;
        get(`#change`).disabled = true;
        get(`#set`).disabled = true;
    }
}