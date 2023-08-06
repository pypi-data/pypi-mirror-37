import requests
import turtle

### Adapted from github.com/jrheard/madison_wcb

# TODOs
# figure out how to generate docs
# re-figure out how to upload to pypi

### Implementation details

# Global mutable state. Forgive me.
state = {
    'connected_to_bot': False,
    'window': None,
    'turtle': None,
}

# These measurements are in "steps", which are basically pixels.
AXI_WIDTH = 1040
AXI_HEIGHT = 784

def _make_cnc_request(endpoint):
    """CNC Server is the way that madison_axi talks to the AxiDraw.

    See https://github.com/techninja/cncserver/ for more information.

    When running cncserver at the command line, specify --botType=axidraw,
    and change machine_types/axidraw.ini's width and height to your satisfaction.
    I use 10400 and 7840 for drawing on a piece of printer paper with a 1cm margin.
    """
    if state['connected_to_bot']:
        return requests.get('http://localhost:4242/' + endpoint)


### Public API

def initialize():
    """IMPORTANT: Call this function at the beginning of your program."""
    try:
        requests.get('http://localhost:4242/poll')
        state['connected_to_bot'] = True
    except requests.exceptions.ConnectionError:
        state['connected_to_bot'] = False

    # set up turtle
    state['window'] = turtle.Screen()
    state['window'].setup(width=AXI_WIDTH, height=AXI_HEIGHT)
    state['turtle'] = turtle.Turtle()
    state['turtle'].width(5)
    state['turtle'].speed(0)
    point_in_direction(0)

    pen_up()

def cleanup():
    """IMPORTANT: Call this function at the end of your program."""
    pen_up()
    move_to(-AXI_WIDTH/2, AXI_HEIGHT/2)


def pen_down():
    """Puts the pen in its "down" position, so that it touches the paper."""
    _make_cnc_request("pen.down")
    state['turtle'].pendown()

    # Wiggle the turtle one step so that it marks a dot on the turtle canvas.
    state['turtle'].forward(1)
    state['turtle'].backward(1)

def pen_up():
    """Puts the pen in its "up" position, so that it doesn't touch the paper."""
    _make_cnc_request("pen.up")
    state['turtle'].penup()

def move_to(x, y):
    """Moves the pen to a particular position.

    Arguments:
        x - a number between -250 and 250.
        y - a number between -180 and 180.
    """
    _make_cnc_request("coord/{0}/{1}".format(x, y))
    state['turtle'].goto(x, y)

def point_in_direction(angle):
    """Points the pen's "turtle" in the direction of the angle specified.

    Arguments:
        angle - a number between 0 and 360.
    """
    # convert angle from regular coordinates to scratch coordinates
    _make_cnc_request("move.absturn./" + str(90 - angle))

    state['turtle'].setheading(angle)

def move_forward(num_steps):
    """Moves the pen forward a few steps in the direction that its "turtle" is facing.

    Arguments:
        num_steps - a number like 20. A bigger number makes the pen move farther.
    """
    assert int(num_steps) == num_steps, "move_forward() only accepts integers, but you gave it " + str(num_steps)

    _make_cnc_request("move.forward./" + str(num_steps))

    state['turtle'].forward(num_steps)

def turn_left(relative_angle):
    """Turns the pen's "turtle" to the left.

    Arguments:
        relative_angle - a number like 10.
            A bigger number makes the turtle turn farther to the left.
    """
    assert int(relative_angle) == relative_angle, "turn_left() only accepts integers, but you gave it " + str(relative_angle)

    _make_cnc_request("move.left./" + str(relative_angle))
    state['turtle'].left(relative_angle)

def turn_right(relative_angle):
    """Turns the pen's "turtle" to the right.

    Arguments:
        relative_angle - a number like 10.
            A bigger number makes the turtle turn farther to the right.
    """
    assert int(relative_angle) == relative_angle, "turn_right() only accepts integers, but you gave it " + str(relative_angle)

    _make_cnc_request("move.right./" + str(relative_angle))
    state['turtle'].right(relative_angle)

def get_position():
    """Returns the pen's current position.

    Return value:
        A list like [-102, 50] representing the pen's current [x, y] position.
    """
    return state['turtle'].position()

def get_x():
    """Returns the pen's current x-coordinate.

    Return value:
        A number between -250 and 250, represnting the pen's current horizontal position.
    """
    return state['turtle'].xcor()

def get_y():
    """Returns the pen's current y-coordinate.

    Return value:
        A number between -180 and 180, representing the pen's current vertical position.
    """
    return state['turtle'].ycor()
