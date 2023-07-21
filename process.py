// Extract temperature value from the payload
var temperatureCelsius = parseFloat(msg.payload.value);

// Convert temperature from Celsius to Kelvin
var temperatureKelvin = temperatureCelsius + 273.15;

// Update the payload with the converted temperature
msg.payload.value = temperatureKelvin;

// Return the modified message
return msg;
