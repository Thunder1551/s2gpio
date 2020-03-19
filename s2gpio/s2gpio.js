(function (ext) {
    var socket = null;

    var connected = false;

    // an array to hold possible digital input values for the reporter block
    var digital_inputs = new Array(32);
    var myStatus = 1; // initially yellow
    var myMsg = 'not_ready';
    
    var temp = 2;
    var hum = 3;
    
    var gas_data = 0;
    var flame_data = 0;
    var water_data = 0;
    var sound_data = 0;

    var pressure = 10;
    var altitude = 12;
    var direction = 'undefined';

    ext.cnct = function (callback) {
        window.socket = new WebSocket("ws://127.0.0.1:9000");
        window.socket.onopen = function () {
            var msg = JSON.stringify({
                "command": "ready"
            });
            window.socket.send(msg);
            myStatus = 2;

            // change status light from yellow to green
            myMsg = 'ready';
            connected = true;

            // initialize the reporter buffer
            digital_inputs.fill('0');

            // give the connection time establish
            window.setTimeout(function() {
            callback();
        }, 1000);

        };

        window.socket.onmessage = function (message) {
            var msg = JSON.parse(message.data);

            // handle the only reporter message from the server
            // for changes in digital input state
            var reporter = msg['report'];
            if(reporter === 'digital_input_change') {
                var pin = msg['pin'];
                temp = 4;
                digital_inputs[parseInt(pin)] = msg['level'];
            }
            if(reporter === 'digital_input_change2') {
                var pin = msg['pin'];
                temp = 4;
            }
            if(reporter === 'digital_input_change3') {
                var pin = msg['pin'];
                temp = parseInt(pin);
                hum = 5;
            }
            if(reporter === 'write_return') {
                //var pin = msg['pin'];
                //var temporary = msg['level'];
                //temp = 4;
                var tempo = msg['pin'];
                var humtemp = msg['level'];        
                temp = parseInt(tempo);
                hum = parseInt(humtemp);
            }       
            if(reporter === 'temp_data') {
                var temperature = msg['temp'];
                temp = parseInt(temperature);
            }
            if(reporter === 'joystick_data') {
                var temp_direction = msg['direction'];
                direction = temp_direction;
            }
            if(reporter === 'bmp_data') {
                var temp_pressure = msg['pressure'];
                var temp_altitude = msg['altitude'];
                pressure = parseInt(temp_pressure);
                altitude = parseInt(temp_altitude);
            }
            if(reporter === 'gas_data') {
                var gas = msg['gas_value'];
                gas_data = parseInt(gas);
            }
            if(reporter === 'flame_data') {
                var flame = msg['flame_value'];
                flame_data = parseInt(flame);
            }
            if(reporter === 'water_data') {
                var water = msg['water_value'];
                water_data = parseInt(water);
            }
            if(reporter === 'sound_data') {
                var sound = msg['sound_value'];
                sound_data = parseInt(sound);
            }
            console.log(message.data);
        };
        window.socket.onclose = function (e) {
            console.log("Connection closed.");
            socket = null;
            connected = false;
            myStatus = 1;
            myMsg = 'not_ready';
        };
    };

    // Cleanup function when the extension is unloaded
    ext._shutdown = function () {
        var msg = JSON.stringify({
            "command": "shutdown"
        });
        window.socket.send(msg);
    };

    // Status reporting code
    // Use this to report missing hardware, plugin or unsupported browser
    ext._getStatus = function (status, msg) {
        return {status: myStatus, msg: myMsg};
    };

    // when the connect to server block is executed
    ext.input = function (pin) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        // validate the pin number for the mode
        if (validatePin(pin)) {
            var msg = JSON.stringify({
                "command": 'input', 'pin': pin
            });
            window.socket.send(msg);
        }
    };

    // when the digital write block is executed
    ext.digital_write = function (pin, state) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("digital write");
        // validate the pin number for the mode
        if (validatePin(pin)) {
            var msg = JSON.stringify({
                "command": 'digital_write', 'pin': pin, 'state': state
            });
            console.log(msg);
            window.socket.send(msg);
        }
    };
    
    // copied digital write block
    ext.digital_write2 = function (pin, state) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("digital write2");
        // validate the pin number for the mode
        if (validatePin(pin)) {
            var msg = JSON.stringify({
                "command": 'digital_write2', 'pin': pin, 'state': state
            });
            console.log(msg);
            window.socket.send(msg);
        }
    };
    // call websever to return pin number    
    ext.write = function (pin, state) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("write");
        // validate the pin number for the mode
        if (validatePin(pin)) {
            var msg = JSON.stringify({
                "command": 'write', 'pin': pin, 'state': state
            });
            console.log(msg);
            window.socket.send(msg);
        }
    };


    // when the PWM block is executed
    ext.analog_write = function (pin, value) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("analog write");
        // validate the pin number for the mode
        if (validatePin(pin)) {
            // validate value to be between 0 and 255
            if (value === 'VAL') {
                alert("PWM Value must be in the range of 0 - 255");
            }
            else {
                value = parseInt(value);
                if (value < 0 || value > 255) {
                    alert("PWM Value must be in the range of 0 - 255");
                }
                else {
                    var msg = JSON.stringify({
                        "command": 'analog_write', 'pin': pin, 'value': value
                    });
                    console.log(msg);
                    window.socket.send(msg);
                }
            }
        }
    };
    // ***Hackeduca --> when the Servo block is executed
    ext.servo = function (pin, value) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("servo");
        // validate the pin number for the mode
        if (validatePin(pin)) {
            // validate value to be between 0° and 180°
            if (value === 'VAL') {
                alert("Servo Value must be in the range of 0° - 180°");
            }
            else {
                value = parseInt(value);
                if (value < 0 || value > 180) {
                    alert("Servo Value must be in the range of 0° - 180°");
                }
                else {
                    var msg = JSON.stringify({
                        "command": 'servo', 'pin': pin, 'value': value
                    });
                    console.log(msg);
                    window.socket.send(msg);
                }
            }
        }
    };

    // when the play tone block is executed
    ext.play_tone = function (pin, frequency) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        // validate the pin number for the mode
        if (validatePin(pin)) {
            var msg = JSON.stringify({
                "command": 'tone', 'pin': pin, 'frequency': frequency
            });
            console.log(msg);
            window.socket.send(msg);
        }
    };

    // when the digital read reporter block is executed
    ext.digital_read = function (pin) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        else {
            return digital_inputs[parseInt(pin)];

        }
    };

     // when the analog read reporter block is executed
    ext.analog_read = function (pin) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        else {
            return digital_inputs[parseInt(pin)];

        }
    };

    // when the DHT11 sensor value read reporter block is executed
    ext.temperature = function (pin) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("temperature");
        //validate the pin number for the mode
        if (validatePin(pin)){
            var msg = JSON.stringify({
                "command": 'temperature2', 'pin': pin
            });
            console.log(msg);
            //window.socket.send(msg);
        window.setTimeout(function() {
            callback();
        }, 1000);
            return temp;
        }
    };
    
    // return value of var hum originally 3 and set by write block
    ext.humidity = function (pin) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("temperature");
        //validate the pin number for the mode
        if (validatePin(pin)){
            var msg = JSON.stringify({
                "command": 'humidity', 'pin': pin
            });
            console.log(msg);
            //window.socket.send(msg);
        window.setTimeout(function() {
            callback();
        }, 1000);
            return hum;
        }
    };

    ext.temp_command = function (pin) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("temp command");
        //validate the pin number for the mode
        if (validatePin(pin)){
            var msg = JSON.stringify({
                "command": 'temperature', 'pin': pin
            });
            console.log(msg);
            window.socket.send(msg);
    
        }
    };
    
    // when the DHT11 sensor value read reporter block is executed
    ext.dht11read = function (pin, callback) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("DHT11 read");
        //validate the pin number for the mode
        if (validatePin(pin)){
            var msg = JSON.stringify({
                "command": "temperature", 'pin': pin
            });
            console.log(msg);
            window.socket.send(msg);
            //window.setTimeout(function() {
            //callback();
            //}, 2000);
        }
    };
    // when the DHT11 sensor value read reporter block is executed
    ext.dht11return = function () {
        return temp;
    };
    // when the Joystick read reporter block is executed
    ext.joystick = function (bool) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("Joystick read");
        //validate the pin number for the mode
        if (bool === 'No'){
            alert("Please check if Joystick is connected via channel 0x77");
    }
    else {
            var msg = JSON.stringify({
                "command": "joystick_read", 'bool': bool
            });
            console.log(msg);
            window.socket.send(msg);
            return direction;
        }
    };
    
    // when the LCD1602 Block is executed
    ext.lcd1602 = function (text, line, bool) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("write to lcd1602 display");
        //validate the pin number for the mode
        if (bool === 'No'){
            alert("Please check if Display is connected via channel 0x27");
    }
    else if (text === 'TEXT'){
        alert("Please input your Text to display");
    }
    else {
            var msg = JSON.stringify({
                "command": "lcd1602_write", 'text': text, 'line': line
            });
            console.log(msg);
            window.socket.send(msg);
        }
    };

    // when the BMP180 sensor value read reporter block is executed
    ext.bmp180read = function (bool) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("bmp180 read");
        //validate the pin number for the mode
        if (bool === 'No'){
        alert("Please check if BMP sensor is connected via channel 0x77");
    }
    else {
            var msg = JSON.stringify({
                "command": "bmp_read", 'bool': bool
            });
            console.log(msg);
            window.socket.send(msg);
        }
    };

    // return the BMP180 sensor value
    ext.bmp180return = function () {
        return pressure;
    };

    // general block to return a value of a chosen sensor model
    ext.sensor_return = function (model) {
        if (model === 'MODEL') {
            alert("Choose a sensor model.");
        }
        else if (model === 'bmp180') {
            return pressure;
        }
        else if (model === 'dht11') {
            return temp;
        }
        else if (model === 'joystick') {
            return direction;
        }
    };
    
    //when the gas sensor command block is executed
    ext.gas_read = function (adc, pin, callback) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("gas_sensor read");
        //validate the adc module
         if (adc === 'PCF8591') {
            //validate input pin is between 0-3
            if (pin > 3 ) {
                alert("PCF8591 input pin has to be in range 0-3");
            }
        }
        var msg = JSON.stringify({
                "command": "gas_sensor", 'adc': adc, 'pin': pin
            });
        console.log(msg);
        window.socket.send(msg);
    };
    
    // when the gas sensor value read reporter block is executed
    ext.gas_return = function () {
        return gas_data;
    };
    
    // when the flame sensor command block is executed
    ext.flame_read = function (adc, pin, callback) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("flame_sensor read");
        //validate the adc module
         if (adc === 'PCF8591') {
            //validate input pin is between 0-3
            if (pin > 3 ) {
                alert("PCF8591 input pin has to be in range 0-3");
            }
        }
        var msg = JSON.stringify({
            "command": "flame_sensor", 'adc': adc, 'pin': pin
        });
        console.log(msg);
        window.socket.send(msg);
    };
    
    // when the flame sensor value read reporter block is executed
    ext.flame_return = function () {
        return flame_data;
    };
    
    // when the water sensor command block is executed
    ext.water_read = function (adc, pin, callback) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("water_sensor read");
        //validate the adc module
        if (adc === 'PCF8591') {
            //validate input pin is between 0-3
            if (pin > 3 ) {
                alert("PCF8591 input pin has to be in range 0-3");
            }
        }
        var msg = JSON.stringify({
                    "command": "water_sensor", 'adc': adc, 'pin': pin
                });
        console.log(msg);
        window.socket.send(msg);
    };
    
    // when the water sensor value read reporter block is executed
    ext.water_return = function () {
        return water_data;
    };
    
    // when the sound sensor command block is executed
    ext.sound_read = function (adc, pin, callback) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("sound_sensor read");
        //validate the adc module
         if (adc === 'PCF8591') {
            //validate input pin is between 0-3
            if (pin > 3 ) {
                alert("PCF8591 input pin has to be in range 0-3");
            }
        }
        var msg = JSON.stringify({
            "command": "sound_sensor", 'adc': adc, 'pin': pin
                });
        console.log(msg);
        window.socket.send(msg);
    };
    
    // when the sound sensor value read reporter block is executed
    ext.sound_return = function () {
        return sound_data;
    };
    
    // when the summend analog sensor command block is executed
    ext.analog_sensor_read = function (sensor, adc, pin, callback) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("analog sensor read");
        var sensor_model = 'undefined';
        //validate sensor model
        switch (sensor) {
            case 'MODEL':
                alert("Choose sensor model");
                break;
            case 'Gas':
                sensor_model = 'gas_sensor';
                break;
            case 'Water':
                sensor_model = 'water_sensor';
                break;
            case 'Flame':
                sensor_model = 'flame_sensor';
                break;
            case 'Sound':
                sensor_model = 'sound_sensor';
                break;
        }
        //validate the adc module
        if (adc === 'PCF8591') {
            //validate input pin is between 0-3
            if (pin > 3 ) {
                alert("PCF8591 input pin has to be in range 0-3");
            }
        }
        var msg = JSON.stringify({
                    "command": sensor_model, 'adc': adc, 'pin': pin
                });
        console.log(msg);
        window.socket.send(msg);
        // give the server time to receive/answer the message
        //Todo: Check for connection closure due to too many messages during loops
        window.setTimeout(function() {
        callback();
        }, 1000);
    };
    
    // when the summed analog sensor value read reporter block is executed
    ext.analog_sensor_return = function (sensor) {
        switch (sensor) {
            case 'MODEL':
                alert("Choose sensor model");
                break;
            case 'Gas':
                return gas_data;
            case 'Water':
                return water_data;
            case 'Flame':
                return flame_data;
            case 'Sound':
                return sound_data;
        }
    };
    
    // general function to validate the pin value
    function validatePin(pin) {
        var rValue = true;
        if (pin === 'PIN') {
            alert("Insert a valid BCM pin number.");
            rValue = false;
        }
        else {
            var pinInt = parseInt(pin);
            if (pinInt < 0 || pinInt > 31) {
                alert("BCM pin number must be in the range of 0-31.");
                rValue = false;
            }
        }
        return rValue;
    }

 var descriptor = {
        blocks: [
            // Block type, block name, function name
            ["w", 'Connect to s2gpio server.', 'cnct'],
            [" ", 'Set BCM %n as an Input', 'input','PIN'],
            [" ", "Set BCM %n Output to %m.high_low", "digital_write", "PIN", "0"],
            [" ", "Set variable temp to 4 %m.high_low", "digital_write2", "PIN", "0"],
            [" ", "Set variable hum to input pin BCM %n %m.high_low", "write", "PIN", "0"],
            [" ", "Set BCM PWM Out %n to %n", "analog_write", "PIN", "VAL"],
            [" ", "Set BCM %n as Servo with angle = %n (0° - 180°)", "servo", "PIN", "0"],     // ***Hackeduca --> Block for Servo
            [" ", "Tone: BCM %n HZ: %n", "play_tone", "PIN", 1000],
            ["r", "Read Digital Pin %n", "digital_read", "PIN"],
            ["r", "Read Analog Pin %n", "analog_read", "PIN"],
            ["r", 'return variable temp %n', 'temperature', 'PIN'],
            ["r", 'return variable hum %n', 'humidity', 'PIN'],
            [" ", 'Read DHT11 sensor value %n', 'dht11read', 'PIN'],
            ["r", 'Return DHT11 sensor value', 'dht11return'],
            ["r", 'Read Joystick on channel 0x77 %m.yes_no', 'joystick', 'No'],
            [" ", "Read sensor value of BMP180 on channel 0x77 %m.yes_no", "bmp180read", "No"],
            ["r", "Return BMP180 sensor value", "bmp180return"],
            [" ", "Write %n on line %m.high_low LCD1602 Display on 0x27 %m.yes_no", "lcd1602", "TEXT", "0", "No"],
            [" ", "send command %n", "temp_command", "PIN"],
            ["r", "Return %m.sensor_model sensor value", "sensor_return", "MODEL"],
            [" ", "Read gas sensor value at %m.adc input Pin %m.ain", "gas_read", "PCF8591", "1"],
            ["r", "Return gas sensor value", "gas_return"],
            [" ", "Read flame sensor value at %m.adc input Pin %m.ain", "flame_read", "PCF8591", "1"],
            ["r", "Return flame sensor value", "flame_return"],
            [" ", "Read water sensor value at %m.adc input Pin %m.ain", "water_read", "PCF8591", "1"],
            ["r", "Return water sensor value", "water_return"], 
            [" ", "Read sound sensor value at %m.adc input Pin %m.ain", "sound_read", "PCF8591", "1"],
            ["r", "Return sound sensor value", "sound_return"],
            [" ", "Read %m.analog_sensor sensor value at %m.adc input Pin %m.ain", "analog_sensor_read", "MODEL", "PCF8591", "1"],
            ["r", "Return %m.analog_sensor sensor value", "analog_sensor_return", "MODEL"],

            

        ],
        "menus": {
            "high_low": ["0", "1"],
            "yes_no": ["No", "Yes"],
            "adc": ["PCF8591", "MCP3008"],
            "ain": ["0", "1", "2", "3", "4", "5", "6", "7"],
            "sensor_model": ["MODEL", "bmp180", "dht11", "joystick"],
            "analog_sensor": ["MODEL", "Flame", "Gas", "Sound", "Water"]

        },
        url: 'https://github.com/Thunder1551/s2gpio'
    };

    // Register the extension
    ScratchExtensions.register('s2gpio', descriptor, ext);
})({});
