const mqtt_client = new_mqtt("219.68.154.148", "8083", `Ketagalan Barefoot ${Math.floor(Math.random() * 2147483647).toString(16)}`);
if (mqtt_client.connected) {
	mqtt_client.reconnect();
}

async function page_init() {

	let input_name = get_node(`#input_name`);
	let input_id = get_node(`#input_id`);
	let add_device = get_node(`#add_device`);
	let change = get_node(`#change`);
	let combobox = get_node(`#device_list`);

	[input_name, input_id].forEach(input => {
		input.addEventListener("input", () => input_check(input));
	});

	combobox.addEventListener("change", () => load_status());

	add_device.addEventListener("click", () => add_new_device());

	change.addEventListener("click", () => {
		if (get_node("#status").status == undefined) load_status();
		else change_status();
	});

}

function change_status() {

	let combobox = get_node(`#device_list`);
	let id = combobox.selectedOptions[0].id;

	let send_status = [1, 0][parseInt(get_node(`#status`).status)];

	mqtt_client.publish(`${id}_writein`, send_status, { "qos": 2 });
}

function load_status() {

	let combobox = get_node(`#device_list`);
	let id = combobox.selectedOptions[0].id;

	for (let option of combobox.options) {
		mqtt_client.unsubscribe(`${option.id}_feedback`, { "qos": 2 });
	}

	mqtt_client.subscribe(`${id}_feedback`, { "qos": 2 });

}

function input_check(input) {
	let type = input.id.split("_")[1];
	let err_msg = check(input.value, type);
	if (err_msg) {
		input.style.border = "2px solid red";
		input.valid = false;
		get_node(`#${type}_err_msg`).innerHTML = err_msg;
	}
	else {
		input.style.border = "2px solid black";
		input.valid = true;
		get_node(`#${type}_err_msg`).innerHTML = "";
	}

	if (input_name.valid && input_id.valid) add_device.disabled = false;
	else add_device.disabled = true;

	function check(str, type) {

		let reg = {
			"name": /^[A-Za-z0-9]{4,16}$/,
			"id": /^[0-4]$/
		};

		let err = {
			"name": "4~16 alphanumeric",
			"id": "1~4 integer"
		}

		if (!str.match(reg[type])) return err[type];
		else return "";
	}
}

function add_new_device() {

	let input_name = get_node(`#input_name`);
	let input_id = get_node(`#input_id`);
	let combobox = get_node(`#device_list`);

	let repeated = [];
	for (let option of combobox.options) {
		if (option.id == input_id.value) repeated.push("id");
		if (option.innerHTML.split("(")[0] == input_name.value) repeated.push("name");
	}

	if (repeated.length) {
		repeated.forEach(type => {
			get_node(`#${type}_err_msg`).innerHTML = `repeated ${type}`;
		});
		return;
	}


	let param = {
		"id": input_id.value,
		"HTML": `${input_name.value}(${input_id.value})`
	};
	let option = new_node("option", param);

	combobox.add(option);
	combobox.value = param.HTML;

	load_status();
}


function new_node(tagname, { classlist = [], id = "", HTML = "", text = "" }) {
	let node = document.createElement(tagname);
	if (classlist.length) classlist.forEach(name => node.classList.add(name));
	if (id) node.id = id;
	if (text) node.innerText = text;
	if (HTML) node.innerHTML = HTML;
	return node;
}

function get_node(selector) {
	let list = document.querySelectorAll(selector);
	if (list.length == 1) return list[0];
	else return list;
}


function new_mqtt(ip, port, ID) {
	let param = {
		"clientId": ID,
		"port": port
	}

	let client = mqtt.connect(`ws:${ip}`, param);

	let connect_msg = get_node("#connect_msg");

	client.on("connect", () => {
		connect_msg.classList = ["green"];
		connect_msg.innerText = "🔴Connect successfully.";
	});

	client.on("close", () => {
		connect_msg.classList = ["red"];
		connect_msg.innerText = "🔴Connection closed.";
	});

	client.on("reconnect", () => {
		connect_msg.classList = ["yellow"];
		connect_msg.innerText = "🔴Reconnecting.";
	});


	client.on("message", (topic, msg) => {
		if (msg.toString().match(/^[0-1]$/)) {
			let status_converter = {
				0: {
					"en": "Off",
					"display": "Turn On"
				},
				1: {
					"en": "On",
					"display": "Turn Off "
				}
			};
			let status = status_converter[msg.toString()];
			get_node(`#status`).status = msg.toString();
			get_node(`#status`).innerHTML = `Device Status ${status.en}`;
			get_node(`#change`).innerHTML = `${status.display} Device`;
		}
	});

	return client;
}

page_init();