/**
 Copyright (c) 2016, 2017 Alan Yorinks All right reserved.

 Python Banyan is free software; you can redistribute it and/or
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
    
    var temp = 2;
    var hum = 3;

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
                digital_inputs[parseInt(pin)] = msg['level']
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
                return digital_inputs[parseInt(pin)]

        }
    };
	
     // when the analog read reporter block is executed
    ext.analog_read = function (pin) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        else {
                return digital_inputs[parseInt(pin)]

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
	#    window.setTimeout(function() {
        #    callback();
        #}, 2000);
        }
    };	
		// when the DHT11 sensor value read reporter block is executed
    ext.dht11return = function () {
        return temp
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
    ext.bmp180 = function (bool) {
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
	    window.setTimeout(function() {
            callback();
        }, 2000);
           return pressure;
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

    // Block and block menu descriptions
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
            ["r", 'Read DHT11 sensor value %n', 'dht11return'],
		["r", 'Read Joystick on channel 0x77 %m.yes_no', 'joystick', 'No'],
		["R", "Read sensor value of BMP on channel 0x77 %m.yes_no", "bmp180", "No"],
		[" ", "Write %n on line %m.high_low LCD1602 Display on 0x27 %m.yes_no", "lcd1602", "TEXT", "0", "No"],
		[" ", "send command %n", "temp_command", "PIN"]

        ],
        "menus": {
            "high_low": ["0", "1"],
            "yes_no": ["No", "Yes"]

        },
        url: 'https://github.com/Thunder1551/s2gpio'
    };

    // Register the extension
    ScratchExtensions.register('s2gpio', descriptor, ext);
})({});

