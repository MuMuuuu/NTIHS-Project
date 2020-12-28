const mqtt_client = new_mqtt("219.68.154.148", "8083", `Ketagalan Barefoot ${Math.floor(Math.random() * 2147483647).toString(16)}`);
if (mqtt_client.connected) {
	mqtt_client.reconnect();
}

async function page_init() {

	get(`#mode_button`).mode = 0;

	get(`#mode_button`).addEventListener("click", () => switch_bg(get(`#mode_button`).mode));

	get(`#device_list`).addEventListener("change", () => load_status());

	get(`#add_device`).addEventListener("click", () => add_new_device());

	get(`#change`).addEventListener("click", () => {
		if (get_device().relay == undefined) load_status();
		else send("relay", ["1", "0"][parseInt(get_device().relay)]);
	});

	get(`#set`).addEventListener("click", () => {
		let val = parseFloat(get(`#input_limit`).value);
		change_limit(val);
		send("limit", val);
	});

	get(`#delete`).addEventListener("click", () => {
		if (confirm(`Delete ${get_device().value} ?`)) {
			get(`#device_list`).remove(get_device().index);
			load_status();
			update_storage();
			check_list();
		}
	});

	["name", "id", "limit"].forEach(type => {
		get(`#input_${type}`).invalid = true;
		get(`#input_${type}`).addEventListener("input", () => check_input(get(`#input_${type}`)));
	});

}

function switch_bg(mode) {

	let modes = ["light", "dark"];
	get(`body`).className = `${modes[mode]}_mode`;
	get(`#mode_button`).mode = (mode + 1) % 2;
	get(`#mode_button`).innerHTML = `${modes[(mode + 1) % 2]} mode`;

}

page_init();

setTimeout(load_storage, 500);

check_list();

