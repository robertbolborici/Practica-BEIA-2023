var T = msg.payload.temperature + 273.15;

var speed = msg.payload.wind_speed * 0.27778;

var double_humidity = msg.payload.humidity_level * 2;

msg.payload = {T,
speed,
double_humidity
};

return msg;
