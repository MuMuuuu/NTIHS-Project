const mqtt_client = new_mqtt("219.68.154.148", "8083", `Ketagalan Barefoot ${Math.floor(Math.random() * 2147483647).toString(16)}`);
if (mqtt_client.connected) {
	mqtt_client.reconnect();
}

async function page_init() {

	let input_name = get(`#input_name`);
	let input_id = get(`#input_id`);
	let input_limit = get(`#input_limit`);
	let add_device = get(`#add_device`);
	let change = get(`#change`);
	let set = get(`#set`);
	let combobox = get(`#device_list`);

	[input_name, input_id, input_limit].forEach(input => {
		input.addEventListener("input", () => input_check(input));
	});

	combobox.addEventListener("change", () => load_status());

	add_device.addEventListener("click", () => add_new_device());

	change.addEventListener("click", () => {
		if (get("#status").status == undefined) load_status();
		else send("relay", ["1", "0"][parseInt(get(`#status`).status)]);
	});

	set.addEventListener("click", () => {
		let val = get(`#input_limit`).value;
		get(`#current`).limit = val;
		get(`#current`).innerHTML = `0/${get(`#current`).limit} (mA)`;
		send("limit", val);
	});

}

function send(type, send_status) {
	mqtt_client.publish(`write/${type}/${get_id()}`, `${send_status}`, { "qos": 2 });
}

function load_status() {
	let type_list = ["current", "relay", "message"];

	type_list.forEach(type => {
		for (let option of get(`#device_list`).options) {
			mqtt_client.unsubscribe(`feedback/${type}/${option.id}`, { "qos": 2 });
		}

		mqtt_client.subscribe(`feedback/${type}/${get_id()}`, { "qos": 2 });
	});


}

function input_check(input) {
	let type = input.id.split("_")[1];
	let err_msg = check(input.value, type);

	input.style.border = `2px solid ${err_msg ? "red" : "black"}`;
	input.invalid = err_msg ? true : false;
	get(`#${type}_err_msg`).innerHTML = err_msg;


	get(`#add_device`).disabled = get(`#input_name`).invalid || get(`#input_id`).invalid;
	get(`#set`).disabled = get(`#input_limit`).invalid;


	function check(str, type) {

		let reg = {
			"name": /^[A-Za-z0-9]{4,16}$/,
			"id": /^[0-4]$/,
			"limit": /^[0-9]{1,}.{0,1}[0-9]{0,}$/
		};

		let err = {
			"name": "4~16 alphanumeric",
			"id": "1~4 integer",
			"limit": "number (mA)"
		}

		if (!str.match(reg[type])) return err[type];
		else return "";
	}
}

function add_new_device() {

	let input_name = get(`#input_name`);
	let input_id = get(`#input_id`);
	let combobox = get(`#device_list`);

	let repeated = [];
	for (let option of combobox.options) {
		if (option.id == input_id.value) repeated.push("id");
		if (option.innerHTML.split("(")[0] == input_name.value) repeated.push("name");
	}

	if (repeated.length) {
		repeated.forEach(type => {
			get(`#${type}_err_msg`).innerHTML = `repeated ${type}`;
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

function get(selector) {
	let list = document.querySelectorAll(selector);
	if (list.length == 1) return list[0];
	else return list;
}

function get_id() {
	let combobox_option = get(`#device_list`).selectedOptions[0];
	return combobox_option ? combobox_option.id : "err";
}

function new_mqtt(ip, port, ID) {
	let param = {
		"clientId": ID,
		"port": port
	}

	let client = mqtt.connect(`ws:${ip}`, param);

	let connect_msg = get("#connect_msg");

	client.on("connect", () => {
		connect_msg.className = "green";
		connect_msg.innerText = "🔴Connect successfully.";
	});

	client.on("close", () => {
		connect_msg.className = "red";
		connect_msg.innerText = "🔴Connection closed.";
	});

	client.on("reconnect", () => {
		connect_msg.className = "yellow";
		connect_msg.innerText = "🔴Reconnecting.";
	});


	client.on("message", (topic, msg) => {

		let type = topic.split("/")[1] || "default";
		let con = msg || "error";

		let type_converter = {
			"current": () => current(con),
			"relay": () => relay(con),
			"message": () => message(con),
			"default": () => err()
		};

		type_converter[type]();

		function current(con) {
			let limit = parseFloat(get(`#current`).limit);

			if (parseFloat(con) >= limit) {
				send("relay", "0");
				get(`#current`).className = "title red";
			}
			else if (parseFloat(con) <= limit * 0.8) {
				get(`#current`).className = "title green";
			}
			else {
				get(`#current`).className = "title yellow";
			}

			get(`#current`).innerHTML = `${con != "error" ? con : 0}/${get(`#current`).limit || 0} (mA)`;

		}

		function relay(con) {
			let status_converter = {
				0: {
					"color": "red",
					"text": "Turn On Device"
				},
				1: {
					"color": "green",
					"text": "Turn Off Device"
				},
				"error": {
					"color": "red",
					"text": "Load Status"
				}
			};
			let status = status_converter[con];
			get(`#status`).status = con;
			get(`#status`).className = `title ${status.color}`;
			get(`#change`).innerHTML = `${status.text}`;
		}

		function message(con) {
			get(`#message`).innerHTML = con;
		}

		function err() {
			get(`#status`).status = undefined;
			get(`#change`).innerHTML = `Load Status`;
		}
	});

	return client;
}

page_init();