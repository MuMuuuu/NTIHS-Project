function new_mqtt(ip, port, ID) {
    let param = {
        "clientId": ID,
        "port": port
    }

    let client = mqtt.connect(`ws:${ip}`, param);

    let connect_msg = get("#connect_msg");
    let connect_light = get("#connect_light");

    let server_event = {
        "connect": {
            "color": "green",
            "msg": "Connect successfully to mqtt server."
        },
        "close": {
            "color": "red",
            "msg": "Can not connect to mqtt server."
        },
        "reconnect": {
            "color": "yellow",
            "msg": "Connecting to mqtt server."
        },
    }

    Object.keys(server_event).forEach(event => {
        client.on(event, () => {
            let val = server_event[event];
            connect_light.className = `light ${val.color}`;
            connect_msg.className = `${val.color}`;
            connect_msg.innerText = `${val.msg}`;
        });
    })

    client.on("message", (topic, msg) => {

        let type = topic.split("/")[1] || "default";
        let con = msg.toString() || "error";

        let type_converter = {
            "current": () => current(con),
            "relay": () => relay(con),
            "message": () => message(con),
            "limit": () => change_limit(con),
            "default": () => err()
        };

        type_converter[type]();

        function current(con) {
            let limit = parseFloat(get_device().limit || 0);

            if (parseFloat(con) >= limit) {
                send("relay", "0");
                get(`#current`).className = "title red";
            }
            else {
                let stat = parseFloat(con) <= limit * 0.8 ? "green" : "yellow";
                get(`#current`).className = `title ${stat}`;
            }

            get_device().current = con;
            get(`#current`).innerHTML = `${con != "error" ? con : 0}/${limit == "error" ? 0 : limit} (mA)`;

            update_storage();
        }

        function relay(con) {
            let status_converter = {
                "0": {
                    "color": "red",
                    "msg": "(connected)",
                    "text": "Turn On Device"
                },
                "1": {
                    "color": "green",
                    "msg": "(connected)",
                    "text": "Turn Off Device"
                },
                "error": {
                    "color": "yellow",
                    "msg": "(not connected)",
                    "text": "Load Status"
                }
            };
            let status = status_converter[con];
            get_device().relay = con;
            get(`#status_light`).className = `light ${status.color}`;
            get(`#status_msg`).innerHTML = `${status.msg}`;
            get(`#change`).innerHTML = `${status.text}`;
            update_storage();
        }

        function message(con) {
            get(`#message`).innerHTML = con;
        }

        function err() {
            get_device().relay = undefined;
            get(`#change`).innerHTML = `Load Status`;
            update_storage();
        }
    });

    return client;
}

function send(type, send_status, ch = "write") {
    mqtt_client.publish(`${ch}/${type}/${get_device().id}`, `${send_status}`, { "qos": 2 });
}

function load_status() {
    let type_list = ["current", "relay", "limit"];

    type_list.forEach(type => {

        for (let option of get(`#device_list`).options) {
            mqtt_client.unsubscribe(`feedback/${type}/${option.id}`, { "qos": 2 });
        }

        mqtt_client.subscribe(`feedback/${type}/${get_device().id}`, { "qos": 2 });
    });

}
