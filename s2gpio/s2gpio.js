/*
 Copyright (c) 2020 Chris Hammerschmidt All rights reserved.
 
 Note: The basic structure was taken over by Alan Yoricks. The rights to this code remain exclusively with Alan Yoricks.
 All changes made to the program code are clearly marked with "***RoboRasp --->". If not explicitly marked, the code remains under the following copyright:
 
 Copyright (c) 2016, 2017 Alan Yorinks All rights reserved.
 
 For information about the original project with related documentation please refer to
 https://github.com/MrYsLab/s2-pi
 https://mryslab.github.io/s2-pi/
 
 
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.
 
 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

(function (ext) {
    var socket = null;

    var connected = false;

    // an array to hold possible digital input values for the reporter block
    var digital_inputs = new Array(32);
    var myStatus = 1; // initially yellow
    var myMsg = 'not_ready';

    // ***RoboRasp -> variables for sensor values
    var flame_data = 0;
    var gas_data = 0;
    var hall_data = 0;
    var joystick_data = 0;
    var photoresistor_data = 0;
    var sound_data = 0;
    var thermistor_data = 0;
    var rain_data = 0;
    var bmp_pressure = 0;
    var bmp_altitude = 0;
    var dht11_data = 0;

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
                digital_inputs[parseInt(pin)] = msg['level']
            }
            
            // ***RoboRasp ---> Begin of handling reporter messages from the server to write received data
            
            if(reporter === 'temp_data') {
                var temperature = msg['temp'];
                temp = parseInt(temperature);
            }
            if(reporter === 'flame_return') {
                flame_data = msg['flame_data'];
            }
            if(reporter === 'gas_return') {
                gas_data = msg['gas_data'];
            }
            if(reporter === 'hall_return') {
                hall_data = msg['hall_data'];
            }
            if(reporter === 'joystick_return') {
                joystick_data = msg['joystick_data'];
            }
            if(reporter === 'photoresistor_return') {
                photoresistor_data = msg['photoresistor_data'];
            }
            if(reporter === 'rain_return') {
                rain_data = msg['rain_data'];
            }
            if(reporter === 'sound_return') {
                sound_data = msg['sound_data'];
            }
            if(reporter === 'thermistor_return') {
                thermistor_data = msg['thermistor_data'];
            }
            if(reporter === 'bmp_return') {
                bmp_pressure = msg['bmp_pressure'];
                bmp_altitude = msg['bmp_altitude'];
            }
            // ***RoboRasp ---> End of handling reporter messages            
            
            console.log(message.data)
        };
        window.socket.onclose = function (e) {
            console.log("Connection closed.");
            socket = null;
            connected = false;
            myStatus = 1;
            myMsg = 'not_ready'
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
                return digital_inputs[parseInt(pin)]

        }
    };

    /* ***RoboRasp ---> Begin of implemented functions
    *   dht11_read
    *   lcd_initialize
    *   lcd_clear
    *   lcd_single_line
    *   lcd_double_line
    *   i2c_read
    *   pcf_read
    *   mcp_read
    *   joystick_read_pcf8591
    */
    
    // when the dht11_read command block is executed
    ext.dht11read = function (pin, callback) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("DHT11 read");
        //validate the pin number for the mode
        if (validatePin(pin)){
            var msg = JSON.stringify({
                "command": "joystick_read", 'pin': pin
            });
            console.log(msg);
            window.socket.send(msg);
        }
    };
    
    // When the lcd_initialize block is executed
    ext.lcd_initialize = function (channel) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("LCD1602 initialize");
        // Validate channel
        if (channel === 'Channel') {
            alert("Check input channel");
        }
        else {
            var msg = JSON.stringify({
                "command": "lcd_initialize", 'channel': channel
            });
            console.log(msg);
            window.socket.send(msg);
        }
    };

    // When the lcd_clear command block is executed
    ext.lcd_clear = function () {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("LCD1602 clear");
        var msg = JSON.stringify({
            "command": "lcd_clear"
        });
        console.log(msg);
        window.socket.send(msg);
    };
    
    // When the lcd_single_line command block is executed
    ext.lcd_single_line = function (message, line, mode, duration) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("LCD1602 initialize");
        // Validate complete input
        if (message === 'Text' || line === 'Line' || mode === 'Mode' || duration === 'Duration') {
            alert("Check input");
        }
        else {
            var msg = JSON.stringify({
                "command": "lcd_single_line", 'message': message, 'line': line, 'mode': mode, 'duration': duration
            });
            console.log(msg);
            window.socket.send(msg);
        }
    };
    
    // When the lcd_double_line command block is executed
    ext.lcd_double_line = function (message0, message1, mode, duration) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        console.log("LCD1602 initialize");
        // Validate complete input
        if (message0 === 'Text_0' || message1 === 'Text_1' || mode === 'Mode' || duration === 'Duration') {
            alert("Check input");
        }
        else {
            var msg = JSON.stringify({
                "command": "lcd_double_line", 'message0': message0, 'message1': message1, 'mode': mode, 'duration': duration
            });
            console.log(msg);
            window.socket.send(msg);
        }
    };
    
    // when the i2c_read command block is executed
    ext.i2c_read = function (model, channel) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        //validate input model and i2c channel
        else if (channel === 'Channel' || model === 'MODEL') {
            alert("Check input of model and channel");
        }
        else {
            console.log("I2C sensor read");
            var msg = JSON.stringify({
                "command": "i2c_read", 'model': model, 'channel': channel
            });
            console.log(msg);
            window.socket.send(msg);
        }
    };
    
    // when the pcf_read command block is executed to read an analog sensor value with PCF8591 module
    ext.pcf_read = function (model, a_pin) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        else if (model == 'MODEL') {
            alert("Choose a sensor model");
        }
        else if (a_pin == 'PIN') {
            alert("Choose an input pin");
        }
        else {
            console.log("Analog sensor read: " + model);
            var msg = JSON.stringify({
                "command": 'pcf_read', 'model': model, 'a_pin': a_pin
            });
            console.log(msg);
            window.socket.send(msg);
        }
    };
    
    // when the mcp_read command block is executed to read an analog sensor value with MCP3008 module
    ext.mcp_read = function (model, a_pin) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        else if (model == 'MODEL') {
            alert("Choose a sensor model");
        }
        else if (a_pin == 'PIN') {
            alert("Choose an input pin");
        }
        else {
            console.log("Analog sensor read: " + model);
            var msg = JSON.stringify({
                "command": 'mcp_read', 'model': model, 'a_pin': a_pin
            });
            console.log(msg);
            window.socket.send(msg);
        }
    };
    
    // when the joystick_read_pcf8591 command block is executed to read the joystick direction with PCF8591 module
    ext.joystick_read_pcf8591 = function (channel, y_pin, x_pin, bt_pin) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        //validate input pins and i2c channel
        else if (channel === 'Channel' || y_pin === 'y_pin' || x_pin === 'x_pin' || bt_pin === 'bt_pin') {
            alert("Check the input pin declaration");
        }
        else {
            console.log("Joystick (PCF8591) read");
            var msg = JSON.stringify({
                "command": "joystick_read_pcf8591", 'channel': channel, 'y_pin': y_pin, 'x_pin': x_pin, 'bt_pin': bt_pin
            });
            console.log(msg);
            window.socket.send(msg);
        }
    }; 
    // ***RoboRasp ---> End of implemented functions
    
    // ***RoboRasp ---> Begin of read reporter functionality to return a chosen sensor value
    
    // when the sensor_return reporter block is executed to return a value of a chosen sensor model
    ext.sensor_return = function (model) {
        if (model === 'MODEL') {
            alert("Choose a sensor model.");
        }
        else if (model === 'bmp180_Pressure') {
            return bmp_pressure;
        }
        else if (model === 'BMP180_Altitude') {
            return bmp_altitude;
        }
        else if (model === 'DHT11') {
            return dht11_data;
        }
        else if (model === 'Flame') {
            return flame_data;
        }
        else if (model === 'Gas') {
            return gas_data;
        }
        else if (model === 'Hall') {
            return hall_data;
        }
        else if (model === 'Joystick') {
            return joystick_data;
        }
        else if (model === 'Photoresistor') {
            return photoresistor_data;
        }
        else if (model === 'Sound') {
            return sound_data;
        }
        else if (model === 'Thermistor') {
            return thermistor_data;
        }
        else if (model === 'Rain') {
            return rain_data;
        }
    };
    // ***RoboRasp ---> End of reporter block functionality 
    
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

    // Block and block menu descriptions
    var descriptor = {
        blocks: [
            // Block type, block name, function name
            ["w", 'Connect to s2_pi server.', 'cnct'],
            [" ", 'Set BCM %n as an Input', 'input','PIN'],
            [" ", "Set BCM %n Output to %m.high_low", "digital_write", "PIN", "0"],
            [" ", "Set BCM PWM Out %n to %n", "analog_write", "PIN", "VAL"],
			[" ", "Set BCM %n as Servo with angle = %n (0° - 180°)", "servo", "PIN", "0"],     // ***Hackeduca --> Block for Servo 			
            [" ", "Tone: BCM %n HZ: %n", "play_tone", "PIN", 1000],
            ["r", "Read Digital Pin %n", "digital_read", "PIN"],
            
            // ***RoboRasp ---> Begin of implemented block descriptions
            [" ", "PCF8591: Read %m.analog_sensor at %m.pcf_ai0", "pcf_read", "MODEL", "PIN"],
			["r", "Return %m.sensor_model sensor value", "sensor_return", "MODEL"]
            // ***RoboRasp ---> End of implemented block descriptions
        ],
        "menus": {
            "high_low": ["0", "1"]
            
             // ***RoboRasp ---> Begin of implemented menus
            "yes_no": ["No", "Yes"],
            "channel": ["0x27", "0x48", "0x77"],
            "pcf_ai0": ["0", "1", "2", "3"],
            "pcf_ai1": ["0", "1", "2", "3"],
            "pcf_ai2": ["0", "1", "2", "3"],
            "ain": ["0", "1", "2", "3", "4", "5", "6", "7"],
            "i2c_sensor": ["BMP180", "DHT11"],
            "sensor_model": ["BMP180_Altitude", "BMP180_Pressure", "DHT11", "Flame", "Gas", "Hall", "Joystick", "Photoresistor", "Rain", "Sound", "Thermistor"],
            "analog_sensor": ["Flame", "Gas", "Hall", "Joystick", "Photoresitor", "Rain", "Sound", "Thermistor"],
            "lcd_init_clear": ["Initialize", "Clear"],
            "lcd_line": ["single", "double"],
            "lcd_mode": ["normal", "permanent", "right_to_left"]
             // ***RoboRasp ---> End of implemented block descriptions

        },
        url: 'https://github.com/RoboRasp/s2gpio'     // ***RoboRasp ---> url changed
    };

    // Register the extension
    ScratchExtensions.register('s2gpio', descriptor, ext);       // ***RoboRasp ---> name of extension changed
})({});
