import kivy
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
    )
from kivy.vector import Vector
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

#_________________________________________

def get_high():
        try: 
            f = open("HS.txt", "r") 
            high = f.read()
            f.close()
        except: high = 0
        return high
    
def add_high(new_score):
        current = int(get_high())
        if new_score>current:
            f = open("HS.txt", "w")
            f.write(str(new_score))
            f.close()


class PingGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    pop_up = ObjectProperty(None)
    pause = ObjectProperty(None)
    highscore = NumericProperty(get_high())
    
    
    def serve_ball(self, vel=(0, 4)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def stop_ball(self):
        self.ball.velocity = (0,0)

    def update(self, dt):
        self.ball.move()
        # bounce of paddles
        self.player1.score += self.player1.bounce_ball(self.ball)
        
        # bounce off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width): self.ball.velocity_x *= -1  #When you want it whacky, change here
        
        
        # went off to a bottom to lose?
        if self.ball.y < self.y:
            add_high(self.player1.score)
            self.highscore = get_high()
            self.player1.score = 0
            self.serve_ball(vel=(0, 4))

        
    def on_touch_move(self, touch):
        if touch.y < self.width / 3: self.player1.center_x = touch.x


    def click(self, order):
        if order == "s": self.player1.score = 0
        self.pause.exist = 0
        self.pop_up.exist = 0
        self.serve_ball()



#_________________________________________

class PingApp(App):

    def build(self):
        game = PingGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


#_________________________________________

class PingBall(Widget):
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
        self.velocity_y -= 0.2


#_________________________________________

class PingPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_x - self.center_x) / (self.width / 2) 
            ball.velocity =  Vector(vx+ offset*2, vy* -0.95 + abs(offset) )*1.05
            return 1
        return 0

#_________________________________________
class Message(Widget):
    exist = NumericProperty(0)
    text = StringProperty("")

#_________________________________________

if __name__ == '__main__': PingApp().run()