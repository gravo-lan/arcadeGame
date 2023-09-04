import pygame as pg, math, random as rd, json

def game():
	pg.init()
	screen = pg.display.set_mode((852, 480))
	pg.display.set_caption('Space Game')

	### Save Loading
	with open ("save.json") as f:
		save = json.load(f)
	
	### Surfaces

	### --- Character
	char = pg.image.load("assets/spaceship.png")
	charScale = pg.transform.scale(char, (100, 100))
	charLoc = [100, 150]

	### --- Bullets
	bullet = pg.image.load("assets/bullet.png")
	bulletScale = pg.transform.scale(bullet, (50, 20))
	bulletLoc = [125, charLoc[1]]
	bigbullet = pg.image.load("assets/bigbullet.png")
	bigbulletScale = pg.transform.scale(bigbullet, (110, 60))
	bigbulletLoc = [125, charLoc[1]]
	eBullet = pg.image.load("assets/eBullet.png")
	ebScale = pg.transform.scale(eBullet, (100, 40))
	ebRoto = pg.transform.rotate(ebScale, 0)
	ebLoc = []

	### --- Enemies
	ufo = pg.image.load("assets/ufo.png")
	ufoScale = pg.transform.scale(ufo, (100, 75))
	ufoLoc = [800, rd.randint(50, 200)]
	secondLoc = [800, ufoLoc[1]]
	boss = pg.image.load("assets/boss.png")
	bossScale = pg.transform.scale(boss, (300, 225))
	bossLoc = [800, 150]

	### --- Health
	heart = pg.image.load("assets/heart.png")
	heartScale = pg.transform.scale(heart, (25, 25))

	### --- Environment
	star = pg.image.load("assets/star.png")
	starScale = pg.transform.scale(star, (5, 5))
	starLocX = [
	 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
	]
	starLocY = [
	 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
	]
	for index in range(0, len(starLocX)):
		starLocX[index] = rd.randint(0, 852)
		starLocY[index] = rd.randint(0, 480)

	score = 0
	streak = 0
	bossHealth = 20
	keys = pg.key.get_pressed()

	### Text
	gOverT = pg.font.Font('freesansbold.ttf', 25).render("GAME OVER", True, (255, 255, 255))
	restartT = pg.font.Font('freesansbold.ttf', 15).render("Press R to restart or X to quit", True,(255, 255, 255))
	gWon = pg.font.Font('freesansbold.ttf', 25).render("YOU WON!",True,(255,255,255))

	### Variables
	shoot = False
	eShoot = False
	bigshoot = False
	animation = 0
	explode = False
	eLoc = [0, 0]
	lives = 3
	play = True
	rpt = None
	boss = False
	a = 0
	b = 0
	z = 0 

	while play == True:
		clock = pg.time.Clock()
		clock.tick(60)
		speed = score / 10
		if score >= 10:
			speed -= 1

	### Background
		screen.fill((0, 0, 0))

		### --- Stars
		for index in range(0, len(starLocX)):
			screen.blit(starScale, (starLocX[index], starLocY[index]))

	### Explosion Animation
		if animation < 18 and explode == True:
			animation += 1
		elif animation >= 18:
			animation = 0
			explode = False

	### Bullet logic
	### --- Player Bullet
		if shoot == True:
			screen.blit(bulletScale, (bulletLoc))
			bulletLoc[0] += 20
		else:
			bulletLoc = [125, charLoc[1] + 35]
		if bigshoot == True:
			screen.blit(bigbulletScale, (bigbulletLoc))
			bigbulletLoc[0] += 3
		else:
			bigbulletLoc = [125, charLoc[1]]
	### --- Boss Bullet
		if eShoot == True:
			screen.blit(ebRoto, (ebLoc))
			ebLoc[0] -= 15
			ebLoc[1] -= 15 * b / a * z
		else:
			ebLoc = [bossLoc[0] + 100, bossLoc[1] + 100]

	### Blitting
	### --- Entities
		screen.blit(charScale, charLoc)
		#Only blit the UFOs if it isn't the boss level
		if boss == False:
			screen.blit(ufoScale, ufoLoc)
			#Introduce the second UFO after score 10
			if score >= 10:
				screen.blit(ufoScale, secondLoc)
		else:
			screen.blit(bossScale, bossLoc)
			bHealthT = pg.font.Font('freesansbold.ttf', 15).render('Health: ' + str(bossHealth), True, (255, 0, 0))
			screen.blit(bHealthT, (bossLoc[0] + 100, 25))

	### --- Explosion
		explosion = pg.image.load("assets/explosion/frame_" + str(animation) + ".gif")
		explosionScale = pg.transform.scale(explosion, (100, 100))
		if explode == True:
			screen.blit(explosionScale, eLoc)

	### --- Hearts
		#Soft code so any amount of hearts can be added
		for i in range(0, lives):
			screen.blit(heartScale, (25 + (i * 30), 25))

	### --- Score
		scoreT = pg.font.Font('freesansbold.ttf', 15).render("Score: " + str(score), True, (255, 255, 255))
		screen.blit(scoreT, (25, 76))
		streakT = pg.font.Font('freesansbold.ttf', 15).render("Streak: " + str(streak), True, (255, 255, 255))
		screen.blit(streakT, (25, 96))
		hScoreT = pg.font.Font('freesansbold.ttf',15).render("High Score: " + str(save['highscore']), True, (255,255,255))
		screen.blit(hScoreT, (25,116))
		hStreakT = pg.font.Font('freesansbold.ttf',15).render("High Streak: " + str(save['highstreak']), True, (255,255,255))
		screen.blit(hStreakT, (25,136))

		#Update the local variables of the high scores, but not the json file yet
		if score > save['highscore']:
			save['highscore'] = score
		if streak > save['highstreak']:
			save['highstreak'] = streak

		### Controls
		for event in pg.event.get():
			keys = pg.key.get_pressed()
			if keys[pg.K_SPACE]:
				shoot = True
			if keys[pg.K_w] and charLoc[1] > 0:
				charLoc[1] -= 5
			if keys[pg.K_s] and charLoc[1] < 440:
				charLoc[1] += 5
			if keys[pg.K_1] and score >= 10:
				bigshoot = True
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_x:
					lives=0

	### Bullet Collision
	### --- Normal Bullet
	### ------ Miss
		if bulletLoc[0]>852:
			shoot=False
			streak = 0
	### ------ Hit first UFO
		elif shoot == True and (abs(bulletLoc[0]-ufoLoc[0])<20 and abs(bulletLoc[1]-ufoLoc[1])<=51):
				shoot = False
				explode = True
				eLoc = [ufoLoc[0],ufoLoc[1]+10]
				ufoLoc = [800,rd.randint(50,200)]
				score+=1
				streak+=1
	### ------ Hit Second UFO
		elif (score>=10 and shoot == True and (abs(bulletLoc[0]-secondLoc[0])<20 and abs(bulletLoc[1]-secondLoc[1])<=51)):
			shoot = False
			explode = True
			eLoc = [secondLoc[0],secondLoc[1]+10]
			secondLoc = [805,rd.randint(50,200)]
			score+=1
			streak+=1
	### ------ Hit Boss
		elif (score==30 and shoot == True and (abs(bulletLoc[0]-(bossLoc[0]+150))<10 and abs(bulletLoc[1]-bossLoc[1])<=200)):
			shoot = False
			bossHealth-=1
	### --- Big Bullet
	### ------ Miss
		if bigbulletLoc[0]>852:
			bigshoot=False
			streak = 0
	### ------ Hit first UFO
		elif bigshoot == True and (abs(bigbulletLoc[0]-ufoLoc[0])<40 and abs(bigbulletLoc[1]-ufoLoc[1])<=102):
				bigshoot = False
				explode = True
				eLoc = [ufoLoc[0],ufoLoc[1]+10]
				ufoLoc = [800,rd.randint(50,200)]
				score+=1
				streak+=1
	### ------ Hit second UFO
		elif (score>=10 and bigshoot == True and (abs(bigbulletLoc[0]-secondLoc[0])<40 and abs(bigbulletLoc[1]-secondLoc[1])<=102)):
			bigshoot = False
			explode = True
			eLoc = [secondLoc[0],secondLoc[1]+10]
			secondLoc = [805,rd.randint(50,200)]
			score+=1
			streak+=1
	### ------ Hit Boss
		elif (score==30 and bigshoot == True and (abs(bigbulletLoc[0]-(bossLoc[0]+150))<40 and abs(bigbulletLoc[1]-bossLoc[1])<=400)):
			bigshoot = False
			bossHealth-=2

	### --- Boss Bullet
		if ebLoc[0] < -10:
			eShoot = False
			ebLoc = [bossLoc[0] + 100, bossLoc[1] + 100]
		elif eShoot == True and abs(ebLoc[0] - 125) < 10 and abs(ebLoc[1] - charLoc[1]) < 40:
			eShoot = False
			lives -= 1
			ebLoc = [bossLoc[0] + 100, bossLoc[1] + 100]

	### Player Death
		if ufoLoc[0] <= charLoc[0] or secondLoc[0] <= charLoc[0]:
			eLoc = charLoc
			if abs(ufoLoc[1] - charLoc[1]) < 70 or abs(secondLoc[1] - charLoc[1]) < 70:
				explode = True
			ufoLoc = [800, rd.randint(50, 200)]
			secondLoc = [800, ufoLoc[1]]
			lives -= 1

	### UFO Path
		ufoLoc[0] -= 1 + speed
		#UFO moves in a sine wave
		ufoLoc[1] += math.sin((1 / 15) * ufoLoc[0]) * (4 * ((1 + speed) / 1))
		#Introduce second UFO after score 10
		if score >= 10:
			secondLoc[0] -= 1 + speed
			secondLoc[1] += math.cos((1 / 15) * secondLoc[0]) * (4 * ((1 + speed) / 1))

	### Star Logic
		#Move all stars
		for index in range(0, len(starLocX)):
			if starLocX[index] > 0:
				starLocX[index] -= 2
			else:
				starLocX[index] = 800
				starLocY[index] = rd.randint(0, 480)

	### Boss Trigger
		if score == 30 and bossHealth > -1:
			#Get rid of the UFOs
			ufoLoc[0] = 900
			secondLoc[0] = 900
			boss = True
			#Slight sine movement
			bossLoc[0] -= 0.25
			bossLoc[1] = 15 * math.sin(bossLoc[0] / 15) + 100
			#Shoots immediately after bullet hits or misses
			if eShoot == False:
				eShoot = True
				a = abs(ebLoc[0] - charLoc[0])
				b = abs(ebLoc[1] - charLoc[1])
				if ebLoc[1] > charLoc[1]: z = 1
				elif ebLoc[1] < charLoc[1]: z = -1
				θ = math.tan(b / a)
				if charLoc[1] < ebLoc[1]: θ = -1 * θ
				ebRoto = pg.transform.rotate(ebScale, 0)
				ebRoto = pg.transform.rotate(ebScale, 100 * θ)

		else:
			#Gets rid of boss bullet if boss is dead
			eShoot = False
		if bossHealth <= 0 and boss == True:
			#Killing the boss
			eLoc = [bossLoc[0] + 200, bossLoc[1]]
			explode = True
			bossHealth -= 1
			score += 1
			lives += 1
			boss = False

	### Game Over (or won)
		if lives <= 0 or score >= 50:
			#Saving the highscore
			with open ('save.json','w') as f:
				json.dump(save,f)
			#End the main functions of the game
			play = False
		else: #Stop updating when game is over or won
			pg.display.update()
	#When game is finished this code runs 
	while rpt == None:
		screen.fill((0, 0, 0))
		#If game won then blit winning text
		if score >= 50: screen.blit(gWon, (300,100))
		#Otherwise blit game over text
		else: screen.blit(gOverT, (300, 100))
		screen.blit(restartT, (275, 250))
		for event in pg.event.get():
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_r:
					rpt = True
				if event.key == pg.K_x:
					exit()

		pg.display.update()

while True:
	game()