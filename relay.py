from flask import Blueprint, render_template
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import wiringpi

relay = Blueprint("relay", __name__, static_folder="static", template_folder="template")

PIN_OFFSET = 65

I2C_ADDR_01 = 0x20
I2C_ADDR_02 = 0x22

wiringpi.wiringPiSetup()
wiringpi.mcp23017Setup(PIN_OFFSET, I2C_ADDR_02)

# dictionary
pins = {
    72: {'name': 'SOCKET_01', 'state': 0},
    71: {'name': 'SOCKET_02', 'state': 0},
    70: {'name': 'SOCKET_03', 'state': 0},
    69: {'name': 'SOCKET_04', 'state': 0},
    68: {'name': 'SOCKET_05', 'state': 0},
    67: {'name': 'SOCKET_06', 'state': 0},
    66: {'name': 'SOCKET_07', 'state': 0},
    65: {'name': 'SOCKET_08', 'state': 0}
}

for PIN in range(65, 81):
    wiringpi.pinMode(PIN, 1)


@relay.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = wiringpi.digitalRead(pin)
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'pins': pins
    }
    # Pass the template data into the template main.html and return it to the user
    return render_template('dashboard.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@relay.route("/dashboard/<changePin>/<action>")
def action(changePin, action):
   changePin = int(changePin)
   deviceName = pins[changePin]['name']
   if action == "on":
      wiringpi.digitalWrite(changePin, 0)
      message = "Turned " + deviceName + " on."
   if action == "off":
      wiringpi.digitalWrite(changePin, 1)
      message = "Turned " + deviceName + " off."

   for pin in pins:
      pins[pin]['state'] = wiringpi.digitalRead(pin)

   templateData = {
      'pins': pins
   }
   return render_template('dashboard.html', **templateData)
