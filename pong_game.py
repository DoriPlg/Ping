import kivy
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
    )
from kivy.vector import Vector
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock


#_________________________________________

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    pop_up = ObjectProperty(None)
    pause = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def stop_ball(self):
        self.ball.velocity = (0,0)

    def update(self, dt):
        self.ball.move()
        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # bounce off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1  #When you want it whacky, change here
        
        
        # went off to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

        if self.player1.score == 10:
            self.pop_up.exist = 1
            self.pop_up.text = "Player 1 wins!"
            self.stop_ball()
        if self.player2.score == 10:
            self.pop_up.exist = 1
            self.pop_up.text = "Player 2 wins!"
            self.stop_ball()
        
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


    def click(self, order):
        if order == "s":
            self.player1.score = 0
            self.player2.score = 0
        self.pause.exist = 0
        self.serve_ball()



#_________________________________________

class PongApp(App):

    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


#_________________________________________

class PongBall(Widget):
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


#_________________________________________

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

#_________________________________________
class Message(Widget):
    exist = NumericProperty(0)
    text = StringProperty("")

#_________________________________________

if __name__ == '__main__':
    PongApp().run()