# In consumers.py
from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from . import game
from . import views
from .models import User,Table
import time

global PLAYERS
global TURN
global GAME
global ROUNDOVER
ROUNDOVER = False
GAME = game.PokerGame()
PLAYERS = []
TURN = 0
# Connected to websocket.connect
def ws_add(message):
	print message.content
	print message.channel
	print message.reply_channel.name
	print message.content['path'][1:-1]
	print "ws_add"
	Group("table").add(message.reply_channel)
	global PLAYERS
	PLAYERS.append({ "reply_channel": message.reply_channel, "channel_name": message.reply_channel.name})
	print PLAYERS



# Connected to websocket.receive
def ws_message(message):
	print "*"*60
	print message.content
	print message.content['text']
	print message.reply_channel
	print message.content["path"][1:-1]
	print "ws_message"
	global ROUNDOVER
	if message.content['text'] == "fold" and ROUNDOVER == False:
		global PLAYERS
		for player in PLAYERS:
			if player['channel_name'] == message.reply_channel.name:
				global GAME
				if GAME.players[GAME.turn].name == player['username']:
					move = "move" + str(GAME.turn + 1) + "Fold."
					GAME.fold(player)
					Group("table").send({"text": move})
					playersRemaining = 0
					temp = game.Player(100, "Temp")
					for x in GAME.inGame:
						if GAME.inGame[x]:
							playersRemaining += 1
							temp = x
					if playersRemaining < 2:
						s = GAME.awardWinner(temp)
						Group("table").send({"text": s})
						for client in PLAYERS:
							for user in GAME.players:
								if user.name == client['username']:
									client['chips'] = user.money
						ROUNDOVER = True
						time.sleep(10)
						GAME.newGame()
						GAME = game.play(PLAYERS)
						ROUNDOVER = False
						Group("table").send({"text": "reset"})
						index = 0
						for player in PLAYERS:
							index += 1
							user = User.objects.get(username=player['username'])
					 		s = "prof" + str(index) + "../../static/" + user.picture 
							Group("table").send({"text": s})
						for player in GAME.players:
							cards = "hand" + GAME.deal(player)
							cash = "cash" + str(player.money)
							for client in PLAYERS:
								if player.name == client['username']:
									client['reply_channel'].send({"text": cards})
									client['reply_channel'].send({"text": cash})
						GAME.preflop()
						for player in PLAYERS:
								global ROUNDOVER
								if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
									player['reply_channel'].send({"text": "active"})
								else:
									player['reply_channel'].send({"text": "inactive"})
						s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
						Group("table").send({"text": s})
					phase = 0
					if GAME.checkRoundEnd():
						Group("table").send({"text": "bet$0"})
						phase = GAME.nextRound()
						if phase == 1:
							s = GAME.flop()
							Group("table").send({"text": s})
						elif phase == 2:
							s = GAME.turnphase()
							Group("table").send({"text": s})
						elif phase == 3:
							s = GAME.river()
							Group("table").send({"text": s})
						elif phase == 4:
							global ROUNDOVER
							s = GAME.showdown()
							for client in PLAYERS:
								for user in GAME.players:
									if user.name == client['username']:
										client['chips'] = user.money
							ROUNDOVER = True
							Group("table").send({"text": s})
							time.sleep(10)
							GAME.newGame()
							GAME = game.play(PLAYERS)
							ROUNDOVER = False
							Group("table").send({"text": "reset"})
							index = 0
							for player in PLAYERS:
								index += 1
								user = User.objects.get(username=player['username'])
						 		s = "prof" + str(index) + "../../static/" + user.picture 
								Group("table").send({"text": s})
							for player in GAME.players:
								cards = "hand" + GAME.deal(player)
								cash = "cash" + str(player.money)
								for client in PLAYERS:
									if player.name == client['username']:
										client['reply_channel'].send({"text": cards})
										client['reply_channel'].send({"text": cash})
							GAME.preflop()
							for player in PLAYERS:
									global ROUNDOVER
									if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
										player['reply_channel'].send({"text": "active"})
									else:
										player['reply_channel'].send({"text": "inactive"})
							s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
							Group("table").send({"text": s})
					if not phase == 4:
						s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
						Group("table").send({"text": s})
					break
		for player in PLAYERS:
			global ROUNDOVER
			if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
				player['reply_channel'].send({"text": "active"})
			else:
				player['reply_channel'].send({"text": "inactive"})
	elif message.content['text'] == "check" and ROUNDOVER == False:
		global PLAYERS
		for player in PLAYERS:
			if player['channel_name'] == message.reply_channel.name:
				global GAME
				if GAME.players[GAME.turn].name == player['username']:
					move = "move" + str(GAME.turn + 1) + "Check."
					GAME.check(player)
					Group("table").send({"text": move})
					phase = 0
					if GAME.checkRoundEnd():
						Group("table").send({"text": "bet$0"})
						phase = GAME.nextRound()
						if phase == 1:
							s = GAME.flop()
							Group("table").send({"text": s})
						elif phase == 2:
							s = GAME.turnphase()
							Group("table").send({"text": s})
						elif phase == 3:
							s = GAME.river()
							Group("table").send({"text": s})
						elif phase == 4:
							s = GAME.showdown()
							for client in PLAYERS:
								for user in GAME.players:
									if user.name == client['username']:
										client['chips'] = user.money
							global ROUNDOVER
							ROUNDOVER = True
							Group("table").send({"text": s})
							time.sleep(10)
							GAME.newGame()
							GAME = game.play(PLAYERS)
							ROUNDOVER = False
							Group("table").send({"text": "reset"})
							index = 0
							for player in PLAYERS:
								index += 1
								user = User.objects.get(username=player['username'])
						 		s = "prof" + str(index) + "../../static/" + user.picture 
								Group("table").send({"text": s})
							for player in GAME.players:
								cards = "hand" + GAME.deal(player)
								cash = "cash" + str(player.money)
								for client in PLAYERS:
									if player.name == client['username']:
										client['reply_channel'].send({"text": cards})
										client['reply_channel'].send({"text": cash})
							GAME.preflop()
							for player in PLAYERS:
									global ROUNDOVER
									if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
										player['reply_channel'].send({"text": "active"})
									else:
										player['reply_channel'].send({"text": "inactive"})
							s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
							Group("table").send({"text": s})
					if not phase == 4:
						s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
						Group("table").send({"text": s})
					break
		for player in PLAYERS:
			global ROUNDOVER
			if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
				player['reply_channel'].send({"text": "active"})
			else:
				player['reply_channel'].send({"text": "inactive"})

	elif message.content['text'] == "call" and ROUNDOVER == False:
		global PLAYERS
		for player in PLAYERS:
			if player['channel_name'] == message.reply_channel.name:
				global GAME
				if GAME.players[GAME.turn].name == player['username']:
					move = "move" + str(GAME.turn + 1) + "Call."
					playerturn = GAME.turn
					GAME.call(player)
					cash = "cash" + str(GAME.players[playerturn].money)
					message.reply_channel.send({"text": cash})
					Group("table").send({"text": move})
					pot = "pot$" + str(GAME.pot)
					Group("table").send({"text": pot})
					phase = 0
					if GAME.checkRoundEnd():
						Group("table").send({"text": "bet$0"})
						phase = GAME.nextRound()
						if phase == 1:
							s = GAME.flop()
							Group("table").send({"text": s})
						elif phase == 2:
							s = GAME.turnphase()
							Group("table").send({"text": s})
						elif phase == 3:
							s = GAME.river()
							Group("table").send({"text": s})
						elif phase == 4:
							s = GAME.showdown()
							for client in PLAYERS:
								for user in GAME.players:
									if user.name == client['username']:
										client['chips'] = user.money
							global ROUNDOVER
							ROUNDOVER = True
							Group("table").send({"text": s})
							time.sleep(10)
							GAME.newGame()
							GAME = game.play(PLAYERS)
							ROUNDOVER = False
							Group("table").send({"text": "reset"})
							index = 0
							for player in PLAYERS:
								index += 1
								user = User.objects.get(username=player['username'])
						 		s = "prof" + str(index) + "../../static/" + user.picture 
								Group("table").send({"text": s})
							for player in GAME.players:
								cards = "hand" + GAME.deal(player)
								cash = "cash" + str(player.money)
								for client in PLAYERS:
									if player.name == client['username']:
										client['reply_channel'].send({"text": cards})
										client['reply_channel'].send({"text": cash})
							GAME.preflop()
							for player in PLAYERS:
									global ROUNDOVER
									if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
										player['reply_channel'].send({"text": "active"})
									else:
										player['reply_channel'].send({"text": "inactive"})
							s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
							Group("table").send({"text": s})
					if not phase == 4:
						s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
						Group("table").send({"text": s})
					break
		for player in PLAYERS:
			global ROUNDOVER
			if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
				player['reply_channel'].send({"text": "active"})
			else:
				player['reply_channel'].send({"text": "inactive"})
				
	elif message.content['text'].isnumeric() and ROUNDOVER == False:
		global PLAYERS
		for player in PLAYERS:
			if player['channel_name'] == message.reply_channel.name:
				global GAME
				if GAME.players[GAME.turn].name == player['username']:
					move = "move" + str(GAME.turn + 1) + "Raise $" + message.content['text']
					playerturn = GAME.turn
					GAME.raiseBet(player, message.content['text'])
					cash = "cash" + str(GAME.players[playerturn].money)
					message.reply_channel.send({"text": cash})
					Group("table").send({"text": move})
					pot = "pot$" + str(GAME.pot)
					Group("table").send({"text": pot})
					bet = "bet$" + str(GAME.highestBet)
					Group("table").send({"text": bet})
					phase = 0
					if GAME.checkRoundEnd():
						Group("table").send({"text": "bet$0"})
						phase = GAME.nextRound()
						if phase == 1:
							s = GAME.flop()
							Group("table").send({"text": s})
						elif phase == 2:
							s = GAME.turnphase()
							Group("table").send({"text": s})
						elif phase == 3:
							s = GAME.river()
							Group("table").send({"text": s})
						elif phase == 4:
							s = GAME.showdown()
							Group("table").send({"text": s})
							for client in PLAYERS:
								for user in GAME.players:
									if user.name == client['username']:
										client['chips'] = user.money
							global ROUNDOVER
							ROUNDOVER = True
							time.sleep(10)
							GAME.newGame()
							GAME = game.play(PLAYERS)
							ROUNDOVER = False
							Group("table").send({"text": "reset"})
							index = 0
							for player in PLAYERS:
								index += 1
								user = User.objects.get(username=player['username'])
						 		s = "prof" + str(index) + "../../static/" + user.picture 
								Group("table").send({"text": s})
							for player in GAME.players:
								cards = "hand" + GAME.deal(player)
								cash = "cash" + str(player.money)
								for client in PLAYERS:
									if player.name == client['username']:
										client['reply_channel'].send({"text": cards})
										client['reply_channel'].send({"text": cash})

							GAME.preflop()
							for player in PLAYERS:
									global ROUNDOVER
									if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
										player['reply_channel'].send({"text": "active"})
									else:
										player['reply_channel'].send({"text": "inactive"})
							s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
							Group("table").send({"text": s})
					if not phase == 4:
						s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
						Group("table").send({"text": s})
					break
		for player in PLAYERS:
			global ROUNDOVER
			if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
				player['reply_channel'].send({"text": "active"})
			else:
				player['reply_channel'].send({"text": "inactive"})

	elif ROUNDOVER == False:
		global PLAYERS
		index = 0
		for player in PLAYERS:
			if player['channel_name'] == message.reply_channel.name:
				player['username'] = message.content['text']
				user = User.objects.get(username=player['username'])
				player['chips'] = user.balance
			index += 1
			user = User.objects.get(username=player['username'])
	 		s = "prof" + str(index) + "../../static/" + user.picture 
			Group("table").send({"text": s})
		if len(PLAYERS) > 1:
			global GAME
			GAME = game.play(PLAYERS)
			for player in GAME.players:
				cash = "cash" + str(player.money)
				cards = "hand" + GAME.deal(player)
				for client in PLAYERS:
					if player.name == client['username']:
						client['reply_channel'].send({"text": cards})
						client['reply_channel'].send({"text": cash})
			GAME.preflop()
			for player in PLAYERS:
					if GAME.players[GAME.turn].name == player['username']:
						player['reply_channel'].send({"text": "active"})
					else:
						player['reply_channel'].send({"text": "inactive"})
			s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
			Group("table").send({"text": s})
			# Group("table").send({
   #      		"text": message.content['text'],
   #  		})

	print PLAYERS
# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("table").discard(message.reply_channel)
    print message.reply_channel
    global PLAYERS
    for player in PLAYERS:
    	print player
    	if player['channel_name'] == message.reply_channel.name:
    		PLAYERS.remove(player)
    		user = User.objects.get(username=player['username'])
    		user.balance = player['chips']
    		user.save()
    print PLAYERS



