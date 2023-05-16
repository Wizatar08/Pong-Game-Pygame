import pygame, sys, random, math, time
import pygame.locals as gameGlobals

#first initialize pygame with pygame.init()
pygame.init();

#Now set all of your global variables, including colour values, dimensions of your game window, etc.
WINDOW_SIZE = (800, 600)

#next create a display surface using the pygame.display.set_mode method
WINDOW = pygame.display.set_mode(WINDOW_SIZE); # Create window variable
pygame.display.set_caption("I love large beefly men dominating me")

RED_PLAYER_COLOR = (198, 9, 13); # Create player colors
BLUE_PLAYER_COLOR = (21, 8, 203);
TEXT_FONT = pygame.font.Font("assets/fonts/Koulen-Regular.ttf", 32); # Create fonts
TEXT_FONT_SMALL = pygame.font.Font("assets/fonts/Koulen-Regular.ttf", 16);

wPressed, sPressed, upPressed, downPressed = False, False, False, False; # Create variables that detect if a key is PRESSED DOWN


"""
This is where you should be creating your classes. Similar to the Target Shooter, what classes will you need? What properties will each class need to get them to behave the way you want? With every decision you make, you are trying to reduce the amount of code you need, making use of inheritance and association where it makes sense.
"""

class MainMenu:

  def __init__(self):
    super().__init__();
    self.arrowMenuOrder = [
      ["manual", "bot (difficulty: easy)", "bot (difficulty: normal)", "bot (difficulty: hard)", "bot (difficulty: extreme)"],
      ["manual", "bot (difficulty: easy)", "bot (difficulty: normal)", "bot (difficulty: hard)", "bot (difficulty: extreme)"],
      ["off", "on"],
      ["start"]
    ]; # Create a 2D list that will determine which option at which menu item is displayed
    self.menuOptionHeaders = ["Player 1 Type: ", "Player 2 Type: ", "Powerups: ", "START"]; # Create a list that shows the title of each memu option
    self.menuIndex = [0, 0, 0, 0]; # Create a list that stores the index of each menu option chosen
    
    self.optionI = 0; # Variable that stores what current menu option the user is choosing
    self.firstPlayerText = Text(TEXT_FONT, ""); # Menu text creation
    self.secondPlayerText = Text(TEXT_FONT, "");
    self.powerupsText = Text(TEXT_FONT, "");
    self.startText = Text(TEXT_FONT, f"{self.menuOptionHeaders[3]}");
    self.leftArrowText = Text(TEXT_FONT, "<");
    self.rightArrowText = Text(TEXT_FONT, ">");

    self.arrowKeyText = Text(TEXT_FONT_SMALL, "Use the arrow keys to navigate menu, press the space bar on START to begin game", (0, WINDOW_SIZE[1] - 40)); # Create text and position it's x coordinate
    self.arrowKeyText.x = (WINDOW_SIZE[0] // 2) - (TEXT_FONT_SMALL.size(self.arrowKeyText.text)[0] // 2);
    self.updateBlitCoords(); # Update text and text position

  def update(self, timeDiff):
    if keyTapped: # Detect when a key is tapped
      if upTapped and self.optionI > 0: # Move the current selected menu option up if up is tapped
        self.optionI -= 1;
      elif downTapped and self.optionI < len(self.arrowMenuOrder) - 1: # Move the current selected menu down if down is tapped
        self.optionI += 1;
      elif leftTapped: # In the current selected menu, change the option to be 1 to the left if left is tapped
        self.menuIndex[self.optionI] -= 1;
        if self.menuIndex[self.optionI] < 0: # Loop to the end if the option is already at the beginning
          self.menuIndex[self.optionI] = len(self.arrowMenuOrder[self.optionI]) - 1;
      elif rightTapped: # In the current selected menu, change the option to be 1 to the right if right is tapped
        self.menuIndex[self.optionI] += 1;
        if self.menuIndex[self.optionI] > len(self.arrowMenuOrder[self.optionI]) - 1: # Loop to the beginning if the option is already at the end
          self.menuIndex[self.optionI] = 0;
      elif spaceTapped and self.optionI == len(self.arrowMenuOrder) - 1: # If the current menu option is on START and space is tapped, begin the game
        self.startGame();
      self.updateBlitCoords(); # Update the text and coords if text, since text will be changing

    pygame.draw.rect(WINDOW, (31, 31, 31), self.outlineRect); # Draw the selected menu option rectangle
    self.firstPlayerText.update(); # Update all the text
    self.secondPlayerText.update();
    self.powerupsText.update();
    self.startText.update();
    self.arrowKeyText.update();
    if self.optionI != len(self.arrowMenuOrder) - 1: # Update the side arrows if the current menu option is not on the START button
      self.leftArrowText.update();
      self.rightArrowText.update();

  def updateBlitCoords(self):
    self.firstPlayerText.text = f"{self.menuOptionHeaders[0]}{self.arrowMenuOrder[0][self.menuIndex[0]]}"; # Update the actual text
    self.secondPlayerText.text = f"{self.menuOptionHeaders[1]}{self.arrowMenuOrder[1][self.menuIndex[1]]}";
    self.powerupsText.text = f"{self.menuOptionHeaders[2]}{self.arrowMenuOrder[2][self.menuIndex[2]]}";
    
    self.outlineRect = pygame.Rect(100, 100 + (100 * (self.optionI)), WINDOW_SIZE[0] - 200, 50); # Set the rectangle position
    self.firstPlayerText.x = (WINDOW_SIZE[0] // 2) - (TEXT_FONT.size(self.firstPlayerText.text)[0] // 2); # Position the text to be centered
    self.firstPlayerText.y = 100;
    self.secondPlayerText.x = (WINDOW_SIZE[0] // 2) - (TEXT_FONT.size(self.secondPlayerText.text)[0] // 2);
    self.secondPlayerText.y = 200;
    self.powerupsText.x = (WINDOW_SIZE[0] // 2) - (TEXT_FONT.size(self.powerupsText.text)[0] // 2);
    self.powerupsText.y = 300;
    self.startText.x = (WINDOW_SIZE[0] // 2) - (TEXT_FONT.size(self.startText.text)[0] // 2);
    self.startText.y = 400;
    self.leftArrowText.x = 125 # Move the arrows
    self.leftArrowText.y = 100 + (100 * self.optionI);
    self.rightArrowText.x = WINDOW_SIZE[0] - 125;
    self.rightArrowText.y = 100 + (100 * self.optionI);

  def startGame(self):
    global currMenu;
    currMenu = Game(self.menuIndex[0], self.menuIndex[1], self.arrowMenuOrder[2][self.menuIndex[2]]); # Change the current menu to be the Game

class Game: # polymorphism of Menu

  def __init__(self, player1setting, player2setting, powerups):
    if player1setting == 0: # Set players to be manual or AI's
      self.player1 = Player("left");
    else:
      self.player1 = AIPlayer("left", player1setting);
    if player2setting == 0:
      self.player2 = Player("right");
    else:
      self.player2 = AIPlayer("right", player2setting);
    self.shouldHavePowerups = True if powerups == "on" else False; # Set powerups to be on or off
    self.powerups = []; # Create powerups list, which will be updated every frame
    self.stones = []; # Create stones list, which will be updated every frame
    self.balls = [Ball(self)]; # Create a list of balls, and add one to it
    self.powerupTimer = time.time(); # Create a time, 

  def update(self, timeDiff):
    for powerup in self.powerups: # Update all powerups
      powerup.update();
    for stone in self.stones: # Update all stones
      stone.update();
    for ball in self.balls: # update all balls
      ball.update([self.player1, self.player2], self.powerups, self.stones, timeDiff);
    self.player1.update(self, timeDiff); # Update both players
    self.player2.update(self, timeDiff);
    if self.shouldHavePowerups and time.time() - self.powerupTimer > 10: # If there should be powerups in the game and 10 seconds have passed since the last powerup spawned, add another one
      self.addPowerup();

  def newRound(self):
    self.balls = [Ball(self)]; # Create new ball
    if self.shouldHavePowerups: # Add a powerup randomly
      self.addPowerup();
    self.player1.paddle.setPaddleHeight(100); # Reset paddle heights
    self.player2.paddle.setPaddleHeight(100);
    removableStones = []; # Create a list of stones that should be removed
    for stone in self.stones: # Loop through all stones
      stone.seeCapturedBalls(self.balls); # Make sure all new balls are in this list so that it can smoothly leave the inside of the stone
      stone.rounds += 1; # Add one to number of rounds this stone has been in the game
      if stone.rounds >= 3: # if this stone has been in more than 3 rounds, remove it
        removableStones.append(stone);
    for stone in removableStones: # Remove any stones that need to be removed
      self.stones.remove(stone);

  def addPowerup(self):
    if self.shouldHavePowerups == True: # If ther e should be powerups
      self.powerupTimer = time.time(); # Set the powerup timer to the current time
      powerupNum = random.randint(1, 4); # Make a random number and add a powerup accordingly
      if powerupNum == 1:
        self.powerups.append(StonePower(self));
      elif powerupNum == 2:
        self.powerups.append(Extension(self));
      elif powerupNum == 3:
        self.powerups.append(Duplicate(self));
      elif powerupNum == 4:
        self.powerups.append(Speed(self));

class EndScreen:

  def __init__(self, winner):
    self.winnerText = Text(TEXT_FONT, f"{winner} has won the game!"); # Create text and position it on the screen
    self.continueText = Text(TEXT_FONT_SMALL, "Press SPACE to reset");
    self.winnerText.x = (WINDOW_SIZE[0] // 2) - (TEXT_FONT.size(self.winnerText.text)[0] // 2);
    self.winnerText.y = 200;
    self.continueText.x = (WINDOW_SIZE[0] // 2) - (TEXT_FONT_SMALL.size(self.winnerText.text)[0] // 2);
    self.continueText.y = 400;

  def update(self, timeDiff):
    global currMenu;
    self.winnerText.update(); # Update the text on screen
    self.continueText.update();
    if spaceTapped: # If the space key is tapped, switch to main menu
      currMenu = MainMenu();
    

class Player:

  def __init__(self, side):
    self.side = side; # Figure out which side the player is supposed to be on, and set their settings accordingly
    if self.side == "left": # LEFT: player is red, and on the left side
      self.color = RED_PLAYER_COLOR;
      self.paddle = Paddle(50, "ws", self.color, self);
    else: # RIGHT: player is blue, and on the right side
      self.color = BLUE_PLAYER_COLOR;
      self.paddle = Paddle(WINDOW_SIZE[0] - 80, "arrows", self.color, self);
    self.score = Score(self.side); # Create score class for the player

  def update(self, game, timeDiff):
    self.paddle.update(True, timeDiff); # Update the player's paddle
    self.score.update(); # update the player's score


class AIPlayer(Player):

  def __init__(self, side, difficulty):
    super().__init__(side); # Call the superclass constructor
    self.distanceRelativeToBall = (0, 0); # Create a tuple showing the x and y difference of the paddle and closest ball
    if difficulty == 1: # Set the paddle speed according to its difficulty
      self.speed = 4;
    elif difficulty == 2:
      self.speed = 6;
    elif difficulty == 3:
      self.speed = 11;
    elif difficulty == 4:
      self.speed = 35;

  def update(self, game, timeDiff):
    self.paddle.update(False, timeDiff); # Update the player paddle but make sure the input controls are not being checked
    self.score.update(); # update player score
    balls = game.balls; # get all balls in game

    ball = self.getClosestBall(balls); # Get the closest ball and find the x and y difference between it and the paddle
    self.distanceRelativeToBall = (ball.getCenterCoords()[0] - self.paddle.x, ball.getCenterCoords()[1] - self.paddle.y - (self.paddle.height // 2))

    if self.distanceRelativeToBall[1] > 10: # Move the paddle up or down if the y difference is greater than 10
      self.paddle.y += min(self.speed * timeDiff / 30, self.distanceRelativeToBall[1]);
    elif self.distanceRelativeToBall[1] < -10:
      self.paddle.y -= min(self.speed * timeDiff / 30, abs(self.distanceRelativeToBall[1]));

  def getClosestBall(self, balls):
    closestBall = None; # make a closest ball variable
    closestXBallCoord = WINDOW_SIZE[0]; # Get the closest ball difference
    for ball in balls: # Loop through balls
      if abs(ball.rect.x - self.paddle.x) < closestXBallCoord: # If the difference is less than the current looped ball
        closestBall = ball; # Set the ball to be the difference
        closestXBallCoord = abs(ball.rect.x - self.paddle.x); # Set the difference variable to be the difference with this new ball
    return closestBall;
  
  
class Paddle: # Inheritance to Player
  
  def __init__(self, x, usedKeys, color, player):
    self.player = player; # Set the player instance this paddle corresponds to
    self.width = 20; # Set width/height
    self.height = 100;
    self.x = x; # Set coords
    self.y = (WINDOW_SIZE[1] // 2) - (self.height // 2);
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height); # Create paddle rectangle
    self.usedKeys = usedKeys; # Set the keys to correspond to the side the player is on
    self.color = color; # Set paddle colour
    self.speed = 10; # For manual players: set paddle speed

  def setPaddleHeight(self, newHeight):
    yPosMovement = (newHeight - self.height) / 2; # Set a change in the paddle y coord
    self.y -= yPosMovement; 
    self.height = newHeight; # Set the height of paddle to be the new height, same with the rectangle object
    self.rect.height = newHeight;

  def update(self, isManual, timeDiff):
    self.move(isManual, timeDiff); # Move the paddle (manual movement)
    self.rect.y = self.y; # Set the rectangle y to be the paddle y
    pygame.draw.rect(WINDOW, self.color, self.rect); # Draw the paddle

  def move(self, isManual, timeDiff):
    if isManual: # If the paddle is user controlled
      if self.usedKeys == "ws": # If the keys the user must use is the letters, detect if W or S is pressed and change the paddle's  y coordinate accordingly
        if wPressed:
          self.y -= self.speed * timeDiff / 30;
        elif sPressed:
          self.y += self.speed * timeDiff / 30;
      elif self.usedKeys == "arrows": # If the keys the user must use is the arrow keys, detect if UP or DOWN is pressed and change the paddle's  y coordinate accordingly 
        if upPressed:
          self.y -= self.speed * timeDiff / 30;
        elif downPressed:
          self.y += self.speed * timeDiff / 30;
    if self.y < 0: # If the paddle y coordinate makes any part of the paddle move off screen, move it back on screen
      self.y = 0;
    if self.y > WINDOW_SIZE[1] - self.height:
      self.y = WINDOW_SIZE[1] - self.height;

class Score: # Inheritance to player

  def __init__(self, side):
    self.side = side; # Set the side the player is on (left or right)
    self.menuWidth, self.menuHeight = 40, 40; # Set dimensions of rectangle
    self.alphaSurface = pygame.Surface((self.menuWidth, self.menuHeight)); # Create a new surface, that can draw a rectangle with an alpha value
    self.alphaSurface.set_alpha(191); # Set alpha value
    if self.side == "left": # Fill the alpha layer based on which side the paddle is on
      self.alphaSurface.fill(RED_PLAYER_COLOR);
    elif self.side == "right":
      self.alphaSurface.fill(BLUE_PLAYER_COLOR);
    self.score = 0;

  def update(self):
    scoreRenderer = TEXT_FONT.render(str(self.score), True, (255, 255, 255)); # Render the text of the score
    if self.side == "left": # Put the text in the appropriate position and blit 
      WINDOW.blit(self.alphaSurface, (40, 30)); # Add the alpha surface to the window
      WINDOW.blit(scoreRenderer, (50, 21)); # Blit the score onto the window
    elif self.side == "right":
      WINDOW.blit(self.alphaSurface, (WINDOW_SIZE[0] - self.menuWidth - 40, 30));
      WINDOW.blit(scoreRenderer, (WINDOW_SIZE[0] - self.menuWidth - 30, 21));
    if self.score >= 10: # If the score is greater than 10, end the game, displaying who won based on the side that got 10
      global currMenu;
      currMenu = EndScreen("RED" if self.side == "left" else "BLUE");
    

class Ball:

  def __init__(self, game, x = None, y = None, angle = None, speed = 5, delay = False):
    self.radius = 15; # Set radius
    self.rect = pygame.Rect((WINDOW_SIZE[0] // 2) - self.radius, (WINDOW_SIZE[1] // 2) - self.radius, 2 * self.radius, 2 * self.radius); # Create rectangle
    self.gameInstance = game; # Pass in game instance
    self.speed = speed; # Set speed
    self.moveable = delay; # Set whether the ball should initially move or not
    self.ballEventTime = time.time(); # Set the time 
    self.rect.x = (WINDOW_SIZE[0] // 2) - self.radius if x == None else x; # Set x and y to be either the middle of the screen or at passed on values
    self.rect.y = (WINDOW_SIZE[1] // 2) - self.radius if y == None else y;
    if angle == None: # Set angle to be either a random angle or a specified angle
      self.angle = (random.random() * (math.pi / 6)) + (math.pi / 6); # Radians between pi/6 and pi/3
      self.angle += 0 if random.randint(1, 2) == 1 else (math.pi / 2); # Determine random direction ball should move
      self.angle *= 1 if random.randint(1, 2) == 1 else -1; # Determine if the ball angles up or down
    else:
      self.angle = angle; # Set angle to be angle
    self.xDir = math.cos(self.angle); # Set x and y directions
    self.yDir = math.sin(self.angle);
    self.lastPlayerHit = None; # Set a last player hit variable so sertain powerups can work

  def update(self, players, powerups, stones, timeDiff):
    if self.moveable: # If the ball should move
      self.move(timeDiff); # Move the ball
      self.increaseSpeed(); # Slowly incremement speed
    else: # If the ball should not move
      if time.time() - self.ballEventTime >= 3: # If it is stopped for 3 seconds, move the ball
        self.moveable = True;
        self.ballEventTime = 0;
    for player in players: # Loop through all pl.ayers
      self.detectPaddleCollision(player.paddle); # Detect player paddle collision
    for powerup in powerups: # Loop through all pwoerups
      self.detectPowerupCollision(powerup); # Detect powerup collision
    for stone in stones: # Loop through all stones
      self.detectStoneCollision(stone); # Detect stone collision
    self.detectHittingEdge(players); # Detect the ball hitting the edge of the playing area
    self.draw(); # Draw the ball

  def increaseSpeed(self):
    if time.time() - self.ballEventTime > 2: # If the last time the ball sped up was two seconds ago
      self.ballEventTime = time.time(); # Reset time
      self.speed += 1; # Increase speed by 1
  
  def move(self, timeDiff):
    self.rect.x += self.xDir * self.speed * timeDiff / 30; # Move the ball by x and y compositions
    self.rect.y += self.yDir * self.speed * timeDiff / 30;

  def getCenterCoords(self):
    return self.rect.x + self.radius, self.rect.y + self.radius; # Get the conter coords of ball
  
  def draw(self):
    pygame.draw.circle(WINDOW, (255, 255, 255), self.getCenterCoords(), self.radius); # Draw the circle

  def detectPaddleCollision(self, paddle):
    if self.rect.colliderect(paddle.rect): # If the ball rect collides with the paddle rect
      self.lastPlayerHit = paddle.player; # Set the last player hit to correspond to the paddle
      if self.rect.right > paddle.rect.left or self.rect.left < paddle.rect.right: # If the ball coords are in the paddle
        ballYRelativetoPaddle = self.getCenterCoords()[1] - paddle.y; # Get the center ball coords relative to paddle coords
        if ballYRelativetoPaddle < 0: # If it is less than 0 (ball landed on top of paddle)
          self.yDir = -abs(self.yDir); # Bounce off top
        elif ballYRelativetoPaddle >= paddle.height: # If it is greater than 0 (ball landed on bottom of paddle)
          self.yDir = abs(self.yDir); # Boucne off bottom
        else:
          self.xDir *= -1; # Bounce off side

  def detectPowerupCollision(self, powerup):
    if self.rect.colliderect(powerup.rect): # If ball hits powerup, call powerup effects
      powerup.onHit(self);

  def detectStoneCollision(self, stone):
    xDiff = self.getCenterCoords()[0] - stone.x; # get ccneter coords of ball
    yDiff = self.getCenterCoords()[1] - stone.y;
    centerDistance = math.sqrt((xDiff ** 2) + (yDiff ** 2)); # Get distance between ball and stone
    if self.radius + stone.radius > centerDistance: # If they are insdie one another
      if self in stone.caughtBalls: # If the ball apawned in the stone
        angle = math.atan2(yDiff, xDiff); # Push it out
        self.xDir = math.cos(angle); 
        self.yDir = math.sin(angle);
      else: # If it instead hit the stone
        centerAngle = math.atan2(yDiff, xDiff); # Get angle of center of stone and center of ball
        hittingAngle = math.atan2(self.yDir, self.xDir); # Get angle at which the ball hits the stone
        angleDifference = centerAngle - hittingAngle; # Get the difference of the two angles
        newAngle = hittingAngle + (2 * angleDifference); # Add twice the difference angle to the balls initial angle
        self.xDir = -math.cos(newAngle); # Set the new xDir to be the opposite of the new angle
        self.yDir = -math.sin(newAngle);
        while self.radius + stone.radius < centerDistance: # Make sure the ball is actually outside the stone so this does not run again
          self.rect.x += self.xDir * self.speed;
          self.rect.y += self.yDir * self.speed;
      

  def detectHittingEdge(self, players):
    if (self.rect.y < 0 and self.yDir < 0) or (self.rect.y > WINDOW_SIZE[1] - (2 * self.radius) and self.yDir > 0): # If it hits a top/bottom edge and y dir is going the appropriate direction
      self.yDir *= -1; # Reverse the y movement
    if self.rect.x < 0: # If ball hits left edge, left player scores and round resets
      for player in players:
        if player.side == "right":
          player.score.score += 1;
      self.gameInstance.newRound();
    elif self.rect.x > WINDOW_SIZE[0] - (2 * self.radius): # If ball hits right edge, right player scores and round resets
      for player in players:
        if player.side == "left":
          player.score.score += 1;
      self.gameInstance.newRound();
          

class Stone:

  def __init__(self, balls, centerX, centerY):
    self.balls = balls; # Get list of balls
    self.x = centerX; # Set center X and Y
    self.y = centerY;
    self.radius = random.randint(50, 75); # Set radius to be a random number
    self.rounds = 0;
    self.caughtBalls = []; # Create list of balls spawned inside the stone
    self.seeCapturedBalls(balls); # Add captured balls

  def update(self):
    if self.rounds == 0: # Set color of stone based on round
      pygame.draw.circle(WINDOW, (21, 235, 13), (self.x, self.y), self.radius);
    elif self.rounds == 1:
      pygame.draw.circle(WINDOW, (177, 198, 14), (self.x, self.y), self.radius);
    elif self.rounds == 2:
      pygame.draw.circle(WINDOW, (243, 223, 68), (self.x, self.y), self.radius);
    removableBalls = []; # Create list of balls that should be removed from caughtBalls
    for ball in self.caughtBalls: # Loop through caughtBalls
      if not self.inDistance(ball): # If the ball is no longer inside the stone, remove it
        removableBalls.append(ball);
    for ball in removableBalls: # Remove balls from caughtBalls list
      self.caughtBalls.remove(ball)

  def seeCapturedBalls(self, balls):
    for ball in balls: # Loop through all balls
      if self.inDistance(ball): # If the ball is inside the stone, add it to this list
        self.caughtBalls.append(ball);

  def inDistance(self, ball):
    xDiff = ball.getCenterCoords()[0] - self.x; # Get x and y distance of center of ball and center of stone
    yDiff = ball.getCenterCoords()[1] - self.y;
    centerDistance = math.sqrt((xDiff ** 2) + (yDiff ** 2)); # Get distance using pythagorean theorum
    return self.radius + ball.radius > centerDistance; # Return whether this distance is greater than the sum of the radius'

class Powerup: # Superclass for all powerups

  def __init__(self, game, imageFileName):
    self.game = game; # Get game instance
    self.image = pygame.image.load(f'assets/powerups/{imageFileName}.png'); # Get image file
    self.x = random.randint(70, WINDOW_SIZE[0] - 70); # Set x and y coords
    self.y = random.randint(30, WINDOW_SIZE[1] - 30);
    self.rect = pygame.Rect(self.x, self.y, 48, 48); # Create rect

  def onHit(self, ball):
    self.game.powerups.remove(self); # Remove powerup from the game

  def update(self):
    WINDOW.blit(self.image, (self.x, self.y)); # Blit the image onto the window

class Duplicate(Powerup):

  def __init__(self, game):
    super().__init__(game, 'duplicate'); # Call superclass, passing in the file name

  def onHit(self, ball):
    super().onHit(ball); # Call superclass onHit
    self.game.balls.append(Ball(self.game, ball.rect.x, ball.rect.y, ball.angle + math.pi, ball.speed // 2, True)); # ADd another ball to game
    ball.speed //= 2; # Half speed of ball

class Extension(Powerup):

  def __init__(self, game):
    super().__init__(game, "extension"); # CAll superclass, passing in the file name

  def onHit(self, ball):
    super().onHit(ball); # Call superclass onHit
    if ball.lastPlayerHit != None: # If there is a player that the ball last hit
      ball.lastPlayerHit.paddle.setPaddleHeight(ball.lastPlayerHit.paddle.height + 75); # Extend their paddle height by 75

class Speed(Powerup):

  def __init__(self, game):
    super().__init__(game, "speed"); # Call superclass constructor

  def onHit(self, ball):
    super().onHit(ball); # Call superclass onHit
    ball.speed += 7.5; # Increase ball speed

class StonePower(Powerup):

  def __init__(self, game):
    super().__init__(game, "barricade"); # Call superclass constructor

  def onHit(self, ball):
    super().onHit(ball); # Call superclass onHit
    self.game.stones.append(Stone(self.game.balls, self.x + 24, self.y + 24)); # Add a stone to window, using powerup coords
    
    

class Text(object):

  def __init__(self, font, text, coords = (0, 0), textColor = (255, 255, 255), bgColor = None):
    self.font = font; # Set font
    self.text = text; # Set text
    self.x, self.y = coords; # Set coords
    self.textColor = textColor; # Set color of text
    self.bgColor = bgColor; # Set background color of text
    self.show = True; # Set text to be shown

  def update(self):
    renderer = self.font.render(self.text, True, self.textColor); # Render text
    if self.bgColor != None: # If the background color is not None, add the background color
      renderer = self.font.render(self.text, True, self.textColor, self.bgColor); 
    if self.show: # If the text should be shown
      WINDOW.blit(renderer, (self.x, self.y)); # Draw text at coords


"""
This is where your main while loop should go.
"""

clock = pygame.time.Clock(); # Create clock variable

currMenu = MainMenu(); # Create screen variable, set it to MainMenu()

while True:
  pygame.display.update(); # Update display
  WINDOW.fill((63, 63, 63)); # Set background color and constantly update it
  deltaT = clock.tick(60); # Set FPS and get the time between current frame and last frame

  keys = pygame.key.get_pressed(); # Get all keys pressed
  wPressed = keys[gameGlobals.K_w]; # Get certain pressed keys
  sPressed = keys[gameGlobals.K_s];
  upPressed = keys[gameGlobals.K_UP];
  downPressed = keys[gameGlobals.K_DOWN];
  upTapped, downTapped, leftTapped, rightTapped, spaceTapped, keyTapped = False, False, False, False, False, False; # Set tapped keys to be false
  
  for event in pygame.event.get():
    if event.type == gameGlobals.QUIT: # If the user wants to quit game, shut down python and system operations
      pygame.quit();
      sys.exit();
    elif event.type == gameGlobals.KEYDOWN: # If the key is down
      keyTapped = True; # Show that a key is tapped
      if event.key == pygame.K_UP: # If a certain key is tapped, set that variable to show that the key is tapped
        upTapped = True;
      elif event.key == pygame.K_DOWN:
        downTapped = True;
      elif event.key == pygame.K_LEFT:
        leftTapped = True;
      elif event.key == pygame.K_RIGHT:
        rightTapped = True;
      elif event.key == pygame.K_SPACE:
        spaceTapped = True;
  currMenu.update(deltaT); # Update the menu

#Mark: PR1 First Submission. Missing response to assignment questions on inheritance etc (add them as a doc string below). Also would like to see better use of inheritance, a good way to do this would be to make a generic GameObject class that allyour game objects could inherit from (ball, paddle, power-up etc).


'''
What is polymorphism?

Polymorphism is a technique that relates properties of objects inherited from a superclass. What this allows you to do is change methods in the new class to be different from its superclass. For example, a class called Vehicle would have a move() method and two subclasses, Bike and Car. The Bike class would have a different way of using the move() method than the Car class. Within the Bike’s move() method, it would be about getting the user to move the bike’s pedals, and the Car’s move() method would be about how much the accelerator/brakes are being pressed. They both are subclasses of an abstract class, but their behaviors of the superclass’s methods are different.

Polymorphism in Pong Game:

Polymorphism is used for powerups. A Powerup() class is used for generally initializing a new object, which in this case is setting coordinates and getting an image file to display. This class also has a onHit() method, called when a ball hits the powerup. In the Powerup class, this simply removes the powerup from the game. However, their subclasses have different functionality in their onHit() method. The Duplicate powerup, which subclasses the Powerup class, calls the onHit() method, but what it does is that it adds another ball to the game, then calls its super method and removes the powerup from the game.

Inheritance:

Inheritance is used to create classes that are based on another class. These classes are known as ‘subclasses’, and they inherit the same methods and properties of the ‘superclass’, the class the subclass is being inherited from. The difference between inheritance and polymorphism is that inheritance is the act of creating a new class based on their methods and properties whereas polymorphism is changing the function of methods from a superclass to multiple subclasses.

Inheritance in Pong Game:

In Pong Game, inheritance is found through the Player and AIPlayer classes. This is due to AIPlayer being a subclass of Player, and where the properties of both classes are the same. 

'''