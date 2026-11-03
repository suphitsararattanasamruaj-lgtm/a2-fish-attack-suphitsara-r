@namespace
class SpriteKind:
    SmallFish = SpriteKind.create()
    BigFish = SpriteKind.create()
    KillerWhale = SpriteKind.create()
# Reference: https://arcade.makecode.com/reference/sprites/sprite/set-kin
# The "Sprite kinds" example uses SpriteKind.create() to define new categories.
# My code names these SmallFish, BigFish and KillerWhale because each creature can have its own collision rules.
# :each fish type has differnt rules for what happens when it touchs the shark
# ============================================================================================================================================================================
# Reference used when creating game sound: https://arcade.makecode.com/reference/music/play-tone
# 2. DAMAGE SOUND
def play_damage_sound():
    music.play_tone(147, 180)
# My code uses 147 Hz for a low tone and 180 milliseconds for a short sound.
# This function is called when a big fish or killer whale damages the shark.
# ============================================================================================================================================================================
# 3. BIG FISH SOUND
def play_big_fish_sound():
    music.play_tone(659, 70)
    music.play_tone(880, 100)
# My code calls it twice: 659 Hz for 70 ms, then 880 Hz for 100 ms
# The rising sound plays when the shark eats a big fish
# ============================================================================================================================================================================
# 4. BIG FISH COLLISION
# This function runs when the shark touches a big fish.
# Touched_fish is the particular big fish that the shark has touched.
# The game checks the shark level before deciding whether to eat the fish or lose a heart.

def on_on_overlap(player_sprite, touched_fish):
    global big_fish, can_take_damage
    if shark_level >= 2:
        sprites.destroy(touched_fish)
        big_fish = None
        play_big_fish_sound()
        info.change_score_by(3)
        info.change_life_by(1)
        if info.life() > 3:
            info.set_life(3)
    elif can_take_damage:
        can_take_damage = False
        info.change_life_by(-1)
        scene.camera_shake(4, 200)
        play_damage_sound()
        pause(1500)
        can_take_damage = True
sprites.on_overlap(SpriteKind.player, SpriteKind.BigFish, on_on_overlap)

# Reference: https://arcade.makecode.com/reference/sprites/on-overlap
# Reference: https://arcade.makecode.com/reference/loops/pause
# ============================================================================================================================================================================
# 5. SMALL FISH COLLISION + growing to level 2
# Small fish can be eaten at level 1 and at every later level.
# The game removes only the small fish that was touched.
# The growth check happens after the point is added, so eating the 20th small fish

def on_on_overlap2(player_sprite3, touched_fish2):
    global shark_level
    sprites.destroy(touched_fish2)
    play_small_fish_sound()
    info.change_score_by(1)
    info.change_life_by(1)
    if info.life() > 3:
        info.set_life(3)
    if info.score() >= 20 and shark_level == 1:
        shark_level = 2
        change_shark_image(assets.image("""
            Medium Shark new
            """))
        play_growth_sound()
sprites.on_overlap(SpriteKind.player, SpriteKind.SmallFish, on_on_overlap2)
# Reference: https://arcade.makecode.com/reference/sprites/on-overlap
# Reference: https://arcade.makecode.com/reference/info/change-score-by
# I added rules restore one heart, cap health at 3, and grow a level 1 shark to level 2 when the score reaches 20.
# Its picture changes to the medium shark and the growth sound plays.
# ============================================================================================================================================================================
# 6. TWO-MINUTE TIMER
# This runs when the countdown finishes, not when a fish is eaten.
# str(final_score) turns the score into text so it can appear in the message.
# A score equal to a nonzero previous best does not count as a new high score here.

def on_countdown_end():
    global final_score
    music.stop_all_sounds()
    play_time_up_sound()
    final_score = info.score()
    game.splash("TIME'S UP!", "Your score: " + ("" + str(final_score)))
    if best_score_before_run == 0 or final_score > best_score_before_run:
        game.set_game_over_message(True, "NEW HIGH SCORE!")
    else:
        game.set_game_over_message(True, "BEAT " + ("" + str(best_score_before_run)) + " NEXT!")
    game.game_over(True)
info.on_countdown_end(on_countdown_end)

# Reference: https://arcade.makecode.com/reference/info/on-countdown-end
# Reference: https://arcade.makecode.com/reference/info/high-score
# A higher score, or a previous best of 0, selects "NEW HIGH SCORE!" otherwise the message challenges the player to beat the previous best score.
# ============================================================================================================================================================================
# Reference: https://arcade.makecode.com/reference/music/play-tone
# 7. GROWTH SOUND
def play_growth_sound():
    music.play_tone(523, 70)
    music.play_tone(659, 70)
    music.play_tone(784, 130)
# My code joins 523, 659 and 784 Hz tones lasting 70, 70 and 130 ms.
# This rising sequence is called when the shark grows to level 2 or 3.
# ============================================================================================================================================================================
# 8. TIME-UP SOUND
def play_time_up_sound():
    music.play_tone(523, 120)
    music.play_tone(392, 120)
    music.play_tone(262, 250)
# My code uses falling pitches of 523, 392 and 262 Hz for 120, 120 and 250 ms.
# The longer final tone marks the end of the two minute countdown.
# ============================================================================================================================================================================
# 9. KILLER WHALE SOUND
def play_whale_sound():
    music.play_tone(523, 70)
    music.play_tone(784, 70)
    music.play_tone(1047, 130)
# My code combines 523, 784 and 1047 Hz for 70, 70 and 130 ms.
# This separate sound plays when the level 3 shark eats a killer whale.
# =======================================================================-=====================================================================================================
# 10. KILLER WHALE COLLISION
# The whale is food at level 3, but it is dangerous at levels 1 and 2.
# It uses the same can_take_damage setting as the big fish.
# While that setting is False, neither creature can take another heart through these touch rules.

def on_on_overlap3(player_sprite2, touched_whale):
    global killer_whale, can_take_damage
    if shark_level >= 3:
        sprites.destroy(touched_whale)
        killer_whale = None
        play_whale_sound()
        info.change_score_by(10)
        info.change_life_by(1)
        if info.life() > 3:
            info.set_life(3)
    elif can_take_damage:
        can_take_damage = False
        info.change_life_by(-1)
        scene.camera_shake(4, 200)
        play_damage_sound()
        pause(1500)
        can_take_damage = True
sprites.on_overlap(SpriteKind.player, SpriteKind.KillerWhale, on_on_overlap3)

# Reference: https://arcade.makecode.com/reference/sprites/on-overlap# level 3 eats the whale for 10 points: lower levels take damage without removing the whale.
# Reference: https://arcade.makecode.com/reference/info/change-life-by
# ============================================================================================================================================================================
# 11. CHANGE SHARK IMAGE
# new_image is the picture passed into this function when the shark grows.
# The direction check keeps the new shark picture facing the same way as before.
def change_shark_image(new_image: Image):
    shark.set_image(new_image.clone())
    if not (shark_facing_right):
        shark.image.flip_x()
# Reference: https://arcade.makecode.com/reference/sprites/sprite/set-image
# Reference: https://arcade.makecode.com/reference/images/image/clone
# Reference: https://arcade.makecode.com/reference/images/image/flip-x
# ============================================================================================================================================================================
# 12. SMALL FISH SOUND
def play_small_fish_sound():
    music.play_tone(784, 80)
vertical_speed = 0
small_fish: Sprite = None
final_score = 0
shark: Sprite = None
best_score_before_run = 0
shark_facing_right = False
can_take_damage = False
shark_level = 0
big_fish: Sprite = None
killer_whale: Sprite = None
# Reference: https://arcade.makecode.com/reference/music/play-tone
# My code uses 784 Hz for 80 ms to make a quick eating sound.
# The small-fish collision function calls it when food is collected.
# ============================================================================================================================================================================
# 13. UNDERWATER BACKGROUND
scene.set_background_image(img("""
    6666666666666666888888888666666666666666666666666666666666666666666666666666666666666666666666666666888888888888888868666666666666666666666666666666666666666666
    6666666666666666888888888666666666666666666666666666666666666666666666666666666666666666666666666666888888888866688866666666666666666666666666666666666666666666
    6666666666666666888888888666666666666666666666666666666666666666666666666668888888866668666666666666888888866666666866666666666666666666666666666666666666666666
    6666666666666668888888888866666666666666666666666666666666666666666666666688888888888888888866666666888888866666666666666666666666666666666666666666666666666666
    6666666666666668888888888888886666666666668888888666666666666666666666666888888888888888888886666668888888886666666666666666666666666666666666666666666666666666
    8866666666666688888888888888888888888888888888888886666666666666666666668888888888888888888888666888888888888866666666666666666666666666666666666666666666666666
    8866666666666888888888888888888888888888888888888888866666666666666666668888888888888888888888888888888888888888888886666666666666666666666666666666666666666666
    8866666666666888888888888888888888888888888888888888886666666666666666688888888888888888888888888888888888888888888888888666666666666666666666666666666666666666
    8866666666688888888888888888888888888888888888888888888866666666666666688888888888888888888888888888888888888888888888888866666666666666666666666666666666666666
    8886666666888888888888888888888888888888888888888888888888666666666668888888888888888888888888888888888888888888888888888888866666666666666666666666666666666666
    8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888886666666666666666666666666666666
    8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888886666666666666666666666666
    8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888866666666666666666
    8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888866666666666666888
    8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888886666666666668888
    8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888886666666888888
    8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888881888888888888888888888888888888888888888
    8888888888888888888888888888888888888818888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    8888888888888888888888888888888888866666888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    8888888888888888888888888888888886666666668888888888888888888888888888888888888888888888888888888888888888888888888888888888888888866666888888888888888888888888
    8888888888888888888888888888888866666666666888888888888888888888888888888888888888888888888888888888888888888888888888888888888886666666668888888888888888888888
    8888888888888888888888888888888666666666666666666668888886666666888888888888888888888888888866668888888888888888888866668888888866666666666888888888888888888888
    8866666888888888888888888888866666666666666666666666688866666666668888888888888881888888866666666888888888866666886666666888888866666666666666666688888888888888
    6666666668886666666688888888666666666666666666666666666666666666666666666688888888888866666666666666888888666666666666666666888666668666666666666688888888888888
    6666666666616666666666888866666668666666666688866666666666666666666666666666888888866666666666666666666666666666666666666666686666666666666666666688886666666666
    6666666666666666666666686666666888888666666888866666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666888866666666666
    8888886666666688866666666666668888888866666888886888888888866666666666666666666666666666666666666666666666666666666666666666666666666666666666668886666666666666
    8888888888888888888666666666888888888866666888888888888888888886666666666666666666666666666666666666666666666666666666666666666666666666666666668866666668888888
    8888888888888888888866666688888888888888888888888888888888888888866666666666666666666666666666666666666666666666666666666666666686666666666666666666666888888888
    8888888888888888888888888888888888888888888888888888888888888888888888666666666666666666666666666666666666666666666668888888888886666666666666666666688888888888
    8888888888888888888888888888888888888888888888888888888888888888888888888666666666666666666666666666666666666666668888888888888888888866666686666666888888888888
    8888888888888888888888888888888888888888888888888888888888888888888888888888886666666666666666666666666666666666668888888888888888888666666888666668888886888888
    8888888888888888888888888888888888888888888888888888888888888888888888888888888888866666666666666666666666666666666888888888888888886666688888888888888887888866
    8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888866686666666666688881888888888886666688888888888888867666666
    888888888888888886666666666666666666666666888888888888888888888888888888888888888888888888888888888886666666666666666888888888888888666688888888888888887e666666
    888888888888666666666666666666666666666666666666688888888888888888888888888888888888888888888888888886666666666666666888888888888888666888888888888888867c666666
    8888888888666666666666666888888868866666666666666686688888888888888888888888888888888888888888888888866666666666666666888888888888888888888888888888866776666666
    8888888666666666668888888888888888888888666666666886666668888888888888888888888888888888888888888888866666666666666666888888888888888888888888888888666776666666
    88886666666666668888888888888888888888888886666668866666666666888888888888888888888888888888888888888866666666666666668888888888888888888888888886666677c6666666
    8866666666668888888888888888888888888888888888866886666666666666688888888888888888668888888888888888888866666666666666888888888888888888888888886666677766666666
    8666666668888888888888888888888888888888888888888886666666666666666888888888888888888888888888888888888888888866666666888888888888888888888888666666677766666666
    6666666688888888888888888888888888888888888888888888666666666666666666688888888888888888888888888888888888888886666666888888888888888888888866666666777666666666
    6666666666666666666666666668888888888888888888888888888666666666666666666668888888888888888888888888888888888886666666888888888888888888866666666667777666866666
    6666666666666666666666666666668888888888888888888888888886666666666666666666888866888888888888888888888888888888866666888888888888888886666666666667777666866666
    666666666666666666666666666666666688888888888888888888888886666666666666666666666688888888888888888888888888888888888888888886888888666666666666686777c668866666
    6666666666666666666666666666666666666688888888888888888888888866666666666666666666688888888888888888888888888888888888888888866668886666666666666677776888888888
    6666666666666666666666666666666666666688888888888888888888888888666666666666666666666688888888888888888888888888888888888886666668888666666666888777778888888888
    6666666666666666666666666666666666666888866688888888888888888888888666666666666666666666666888888888888888888888888886666666666668888866888888888777778888888888
    6666666666666666688888888866666666666888666666688888888888888888888866666666666666666666666666666666666666666666666666666666666666888866888888888777778888888888
    6666666688888888888888888888888888888888b6666666688888888888888888888866666666666666666666666666666666666666666666666666666b6666668888888888888867777c8888888888
    68888888888888888888888888888888888888886688888668888668888888888888888888666666666666666666666666666666666666666666666666666666668888888888888867777c8888888888
    88888888888888888888888888888888888888888888888888888666666668888888888888886666666666666666666666666666666666666666666666666668888888888888888867777c8888888888
    8888888888888888888888888888888888888888888888888888888888888888888888888888886666666b666666666666666666666666666666666666666688888888888888888867777c8888888888
    88888888888888888888888888888888888888888888888888888888888888888888888866888886666666666666666666666666666666666666666666688888888888888888888867777c8888888888
    88888888888888888888888888888888888888888888888888888888888888888888888866666666666666666666666666666666666666666666666688888888888888888888888867777c8888888888
    88888888888888888888888888888888888888888888888888888888888888888888888866666666666666666666666666666666666666666666668888888888888888888888888887777c8888888888
    8888888888888888888888888888888888888888888888888888888888888888888888888888666666666666666666666666666666666666666888888888888888888888888888888777778888888888
    8888888888888888888888888888888888888888888888888888888888888888888888888888888886666666666666666666666666666666888888888888888888888888888888888c77778888888888
    8888888888888888888888888888888888888888888888888888888888888888888888888888888888866866666666666666666666666688888888888888888888888888888688888877776888888888
    88888888888888888881888888888888888888888888888888888888888888888888888888888888888668888886666666666666888888888888888888888888888888888886688888c777c888888888
    88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888886c88888c7777688888888
    8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888cc8888887777688888888
    88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888886c8888886777768888888
    88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888886c6888888777768888888
    88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888887c6888c88c77778888888
    88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888887c888878887777ccc8888
    88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888867c88887888c77777c8888
    88888888888888888888888888881888888888818888888888888888888888888888888888888888888888888888888881888888888888888888888888888888888888888877c8888e888877777c8888
    88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888c77c888cc888877777c8888
    88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888c7e888c7c8888c7777c8888
    888ddddd88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888c77c888c78888867777c8888
    88dddd8d88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888777c88c778888867777c8888
    8ddddddddd88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888c77cc8877c8888867777c8888
    ddddddddddddddddd8888888888888888888888888888888888888888818888888888888888888888888888888888888888888888888888888888888888888888888888777c88777c888886777778888
    ddddddddddddddddddd8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888c77cc8c77ec88888c7777cc888
    ddddddddddddddddddddd888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888dddddd88888c77c88c777c8888cc7777cc888
    dddddddddddddddddddddd88888888888888888888888888888888888888888888888888888888888888888888888888888888888dd88888888888888ddddddddd888cc77c8cc77c8888cc777777cc88
    dddddddddddddddddddddddd88888888888dddddddd88888888888888888888888888888888888888888888888888888888888ddddddd888888888888ddddddddddd8c77cc8c777c8888cc7777777c88
    3333decddddddddddddddddddd88888dddddddddddddd8888888888888888888888888888888888888888888888888888888ddddddddd88888888888dddddddddddddc7cc88c777c88888cc77777c888
    3333decdddddddddddddd3dddddddddddddddddddddddd8888888888888888888888888888888888888888888888888888dddddddddddd888888888ddddddddddddddc77cc8cc77cc88888c77777c888
    33b6beecdddddddddddddbbbdddddddddddddddddddddddd888888888888888888888888888888888888888888888888ddddddddddddddddddd888dddddddddddddddc777c88c777c88888c77777c888
    b33bbbeedddcbcdbddddd3bbddddddddddddddddddddddddd8888888888888888888888888888888888888888888888ddddddddddddddddddddddddddddddddddddddc777c88c777e888887777777888
    33b68beecdd4eed3ddddd33bdddddddddddddddddddddddddd88888888888888888888888888888888888888888888dddddddddddddddddddddddddddddddddddddddc777c88c7777ec8887777777888
    33b88bbeed6beedbbddd63bbdddddddddddddddddddddddddddd8888888888888888888888ddddddd88888888888ddddddddddddddddddddddddddddddddddddddddc7777c888c7777ec867777777888
    3bbc633becbbeca336dd633bdddddddddddddddddddddddddddddd8888888888888888888dddddddddd88888888dddddddddddddddddddddddddddddddddddddddddc77777888877777c8c77e7777c88
    3bbea333ecbbecb33bdd6b3bddddddddddddddddddddddddddddddd88888888888888888dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddc7777c8888c7777c777e7777c88
    3bbecb33bebec8333b6db33bdddddddddddddddddddddddddddddddd888888888888888ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddc77777c888c77777777e7777c88
    bcbeeb333bbec8333b6dbb3bdddddddddddddddddddddddddddddddd888888888888888ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddc77777c8888c7777777e7777c88
    b8beecb33bbec6333b6d3336dd6ddddddddddddd6dddddddddddddddd8888888888888ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddc77777c8888777777e77777888
    b6b3ea333bbecb333ecb33bddbbecddddddddddddddddddddddddddddd88888888888ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddc7777cddddd77777e77777888
    b6334bb33bbecb333eeb33bdcbeecddddddddb6dddddddddddddddddddd88888888dddddddddddddddddddddddddddddddddddddddddddddddddddaaadddddddddddddddc777ecddd77777ee7777c888
    b6333bb33bbeb33bbbe33366beecdd6dddddd66dddddddddddddddddddddd88888dddddddddddddddddddddddddddddddddddddddddddddddddaddaaaaaaddddddddddddcc777cddc77777e7777cdddd
    bb333bb333bee33bbb333b8bbee8bbbbddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddaaaaaaaaaadddddddddddddc777eddc7777ee7777cdddd
    bbb33bb333be333bbb333364eec8b33bddbbbcddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddaaaaabbaaaaacddddddddddd777edc77777e7777cddddb
    bbb33bb333be333bbb333364eec8b33bddbbbcdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddbaabbbbbbbbaaabaabbaaaacdddddddddddc77cdc7777e7777ecddddd
    34b333b33be333b88b33333bec88a333cbbbeedd6ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddbaababdbdbaabaabbaaabaaacddddddddddc77cd77777e7777cdddcdd
    3be333b33bb333c66333333bec888b33bbbbecddbdddddddddddddddddddccddddddddddddddddddddddddddddddddddddddddbbabaaaaadbaabab444baaaaaaabccccccddc7e8c7777777777ddddcdd
    3beb33333bb33b8bb33be33bec888b33bbeeccbdddddddd7ddddddddddcccccddddddddddddddddddddddddddddddddddddddbbbabbbaaaddaaab44444aabbaabddddddbcce7cc77777e7777cdddd7cd
    3beb33333333bec3333be33bec888633bbeeccddddddddd7ddddddddddccccccddddddddddddddddddddddddddddddddddddbbbaabbaaaaaaabbb44444b444baddddddddbc777d77777e7777bbbbb7bd
    33eb33333333beb333bbe33bec888633beccccddddddbdd77d7ddddddcccdddcdddddddddddddddddddddddddddddddddddbabababbaaaaaaaaaa4444444444badddddddbc77dd777d7e7777ddddd7bd
    33bb33333333be3333beeb33ec888c33becccbdddddd77d77d7dddddddccddcdddddddddddddddddddddddddddddddddddddbbbbbbbbbbbbbbbb44444444444bbbdbbbbbbbe7dd777d7e7777ddddd7bd
    33b333333333eb333bbeeb33ec888b33becccbdddddd77b77b7bdddddddccdcddddddddddddddddddddddddddddddddddddddddddddddddddd44444444444444bbbcccccccccbb777b7e7777dddd77bd
    33333333333be33bbbbeeb33ec888b33becbbbddddd7b777777bddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd4444444444444bccccccccccccccccccb77777bdddd777d
    b3333333333bb33bbbbebb3bee88b333eeccbddcbbc7b777777dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd444444444444bcccccccccccccccccccbb7777bdddb77bd
    b3333333333bb33bbbeec33bee88b33beeccbddc33bb777777ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd4444444444bbbbbccccccccccccccccbbbb777dddd777bd
    bbb33333333bb33bb4eeb33beec6333beecbbcdc33b.b77b7b7dddddddddddddddddb7ddbddddddddddddddddddddddddddddddddddddddddd4444444bbbbbbbbccccccccccccccb4444c77dddd777bd
    bbbbbbbbb33b333ccbee333ceeeb33bbeecccecc33b..bbbbbbdddddddddddddddd33b7ddddddddddddddddddddddddddddddddddddddddddd444444bbbbbbbbbbbbbccccccccccb5444cc7dddd777dd
    bbbbbbbbbbbb333cceec33b8eee3338ceeccbbec33b..bbbbbddd66666ddddddddb4447db7ddddddddddddddddddddddddddddddddddddddd474444bbbbbbbbbbbbbbbccccccb4444444be7bddd777dd
    bbbbbbbbbbb6b33cceeb33b8eee33b8ceeccc4eb33b....b..66d669966ddddddb44447477ddddddddddddddddddddddddddddddddbddddb7777744bbbbbbbbbbbbbbccbbbcb44454444444ddd777bdd
    bbbbbbbbbbb6b33cceeb33b8eee33b8ceeccc4eb33bbbb....66d669966ddddddbee447777dbdddddddddddddddddddddddddddddddddb7777777eccbbbbbbbbbbccccb445b4545444445444dd777ddd
    bbbbbbb44bbbbbbeeeeb33b8eee33b8ceecccbb333cbbbbb.6666669996d666ddd7eeb7777d7ddddddddddddddddddddddddddddddddd77777777ccccccccccccccccb444444444444444545db77bddd
    bbbbbbb44bbbbbbbbeeb33c8eee33c8cbecc8b333bbbbcbcb69999999966996ddd7..7777db7dddddddddddddddddddddddddddddddd777ee7777ccccccccccccccccb4444444474444447777777dddd
    bbbbbbbbbbbbbbbbbbee33b8eee33c8cbecc8b333...c396669999999999996ddd7b.7777b77ddddddddddddddddddddddddddddddddb77eeeeeeccccccccccccccccc444744477744777777e7bbdddd
    66bbbbbbbbbbbbbbbbbe33b8eeeb3c8ceecc8333bc..b399999999999999996ddd777777d77dddddddddddddddddddddddddddddddddddddb777edbbbbcccccccccc7e74777777777777777eee7ddddd
    ccccc6bbbbbbbbbbbbbbbbb6bbbbbb8ceeccb33bbec.b3b699999999999999666dd777777ddddddddddddddddddddddddddddddddddddddddddddddddddddddddd77777777777777777777eeee7ddddd
    ccccccccbbbbbbbbbbbbbbbbbbbbbb6eeeccb33bbee66699999999999999999966ddbcccbbdddddddddddddddddddddddddddddddddddddddddddddddddddddddd77e77e777777777eeeeeeeeedddddd
    ccccccccc6bbbbbbbbb6666bbbbbbbbceebb33bcbbe6669999999999999999996bbbccccccbddddddddddddddddddddddddddddddddddddddddddddddddddddddd77eeeeeeeee7eeeeeeeebbbbdddddd
    ccccccccccbbbb6666666c66bbbbbb6cecbb33b8bbeb666999999999999996966bbbcccccbdddddddddddddddddddddddddddddddddddddddddddddddddddddddddd77eeee7eeeeeeeecbbbbbbbbdddd
    """))
shark_level = 1
can_take_damage = True
shark_facing_right = True
big_fish_facing_left = True
whale_facing_left = True
best_score_before_run = info.high_score()
# Reference: https://youtu.be/vTLKndl2sBs?si=mrAGHJjk2GPBNKAJ
# ============================================================================================================================================================================
# 15. GAME SETUP
# The introduction appears before the shark controls and countdown are set up below.
music.set_volume(100)
game.splash("FISH ATTACK", "Score as much as possible in 2 minutes!")
if best_score_before_run > 0:
    game.splash("BEST SCORE: " + ("" + str(best_score_before_run)),
        "Can you beat it?")
else:
    game.splash("FIRST RUN", "Set your first high score!")
# Reference: https://arcade.makecode.com/reference/game/splash
# My code supplies "FISH ATTACK" and the two-minute objective, then uses another splash to show either the previous best score or the first run message.
# ============================================================================================================================================================================
# 16. CREATE PLAYER SHARK
# This is the player shark at level 1.
shark = sprites.create(img("""
        . . . . . . . . . . . . . . . .
        . . . . . 1 . . . . . . . . . .
        . . 4 . . 1 1 1 . . . . . . . .
        . . 4 . . . 1 1 1 . . . . . . .
        . 4 4 4 . 4 4 4 4 4 4 . . . . .
        . . . 4 4 1 1 1 4 f 4 4 . . . .
        . . . . 4 1 1 4 4 4 4 . . . . .
        . . . . . 1 . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        """),
    SpriteKind.player)
# The first 80 sets left/right movement speed: the second 80 sets up/down speed.
# The following lines keep the shark on screen and start the score, hearts and timer.
controller.move_sprite(shark, 80, 80)
shark.set_stay_in_screen(True)
info.set_score(0)
info.set_life(3)
info.start_countdown(120)
# Reference: https://arcade.makecode.com/reference/controller/move-sprite
# Reference: https://arcade.makecode.com/reference/info/start-countdown
# The setup also starts the player at 0 points and 3 hearts.
# ============================================================================================================================================================================
# 17. SPAWN BIG FISH
# Big fish can appear while the shark is still level 1.
# There is no level check in this creation function: the eating rule is checked when they touch.
# The 4 second check does not always create a fish: it skips creation if one already exists.

def on_update_interval():
    global big_fish, big_fish_facing_left
    if len(sprites.all_of_kind(SpriteKind.BigFish)) == 0:
        big_fish = sprites.create(assets.image("""
                Left facing big fish
                """).clone(),
            SpriteKind.BigFish)
        big_fish_facing_left = True
        vertical_speed2 = randint(10, 20)
        if randint(0, 1) == 0:
            vertical_speed2 = 0 - vertical_speed2
        big_fish.set_position(140, randint(20, 100))
        big_fish.set_velocity(-30, vertical_speed2)
        # Never destroy the big fish at the screen edge
        big_fish.set_flag(SpriteFlag.AUTO_DESTROY, False)
game.on_update_interval(4000, on_update_interval)

# Reference: https://arcade.makecode.com/reference/game/on-update-interval
# Reference: https://arcade.makecode.com/reference/sprites/all-of-kind
# Reference: https://arcade.makecode.com/reference/sprites/sprite/set-flag
# ============================================================================================================================================================================
# 18. SPAWN SMALL FISH
# Unlike big fish, small fish are created without checking whether others already exist.
# This allows several small fish to be in the game at the same time.
# A negative left/right speed moves a fish left, a positive speed moves it right.

def on_update_interval2():
    global small_fish, vertical_speed
    small_fish = sprites.create(assets.image("""
            SmallFish0
            """),
        SpriteKind.SmallFish)
    vertical_speed = randint(8, 20)
    if randint(0, 1) == 0:
        vertical_speed = 0 - vertical_speed
    if randint(0, 1) == 0:
        small_fish.set_image(assets.image("""
            SmallFish0
            """))
        small_fish.set_position(155, randint(15, 105))
        small_fish.set_velocity(-40, vertical_speed)
    else:
        small_fish.set_image(assets.image("""
            Right facing small fish
            """))
        small_fish.set_position(5, randint(15, 105))
        small_fish.set_velocity(40, vertical_speed)
    small_fish.set_flag(SpriteFlag.AUTO_DESTROY, True)
game.on_update_interval(1500, on_update_interval2)

# Reference: https://arcade.makecode.com/reference/game/on-update-interval
# Reference: https://arcade.makecode.com/reference/math/randint
# Reference: https://arcade.makecode.com/reference/sprites/sprite/set-flag
# ============================================================================================================================================================================
# 19. KILLER WHALE MOVEMENT
# This movement check runs repeatedly.
# The whale must exist before the code can check its position or change its movement.
# abs() removes a minus sign: abs(-45) becomes 45.
# Using 0 - abs() makes the speed negative, so the whale can turn left or up.

def on_forever():
    global whale_facing_left
    if killer_whale != None:
        # Left edge
        if killer_whale.left <= 0 and killer_whale.vx < 0:
            killer_whale.left = 0
            killer_whale.vx = abs(killer_whale.vx)
        elif killer_whale.right >= 160 and killer_whale.vx > 0:
            # Right edge
            killer_whale.right = 160
            killer_whale.vx = 0 - abs(killer_whale.vx)
        # Top edge
        if killer_whale.top <= 0 and killer_whale.vy < 0:
            killer_whale.top = 0
            killer_whale.vy = abs(killer_whale.vy)
        elif killer_whale.bottom >= 120 and killer_whale.vy > 0:
            # Bottom edge
            killer_whale.bottom = 120
            killer_whale.vy = 0 - abs(killer_whale.vy)
        # Face right
        if killer_whale.vx > 0 and whale_facing_left:
            killer_whale.image.flip_x()
            whale_facing_left = False
        elif killer_whale.vx < 0 and not (whale_facing_left):
            # Face left
            killer_whale.image.flip_x()
            whale_facing_left = True
forever(on_forever)

# Reference: https://arcade.makecode.com/reference/sprites/sprite/vx
# Reference: https://arcade.makecode.com/reference/sprites/sprite/vy
# Reference: https://arcade.makecode.com/reference/images/image/flip-x
# ============================================================================================================================================================================
# 20. LARGE SHARK GROWTH
# Both checks must be true: the score must be at least 50 AND the shark must be level 2.
# After the level changes to 3, this condition is no longer true, so the growth sound does not keep playing each time the function checks again.

def on_forever2():
    global shark_level
    if info.score() >= 50 and shark_level == 2:
        shark_level = 3
        change_shark_image(assets.image("""
            BiG Shark
            """))
        play_growth_sound()
forever(on_forever2)

# Reference: https://arcade.makecode.com/reference/info/score
# Reference: https://docs.python.org/3/tutorial/controlflow.html#if-statements
# ============================================================================================================================================================================
# 21. SMALL FISH VERTICAL MOVEMENT
# current_fish means the fish being checked during this turn through the list.
# After checking one fish, the loop moves to the next.
# These checks only turn fish at the top and bottom, so they can still leave at the sides.

def on_forever3():
    for current_fish in sprites.all_of_kind(SpriteKind.SmallFish):
        if current_fish.top <= 0 and current_fish.vy < 0:
            current_fish.top = 0
            current_fish.vy = abs(current_fish.vy)
        elif current_fish.bottom >= 120 and current_fish.vy > 0:
            current_fish.bottom = 120
            current_fish.vy = 0 - abs(current_fish.vy)
forever(on_forever3)

# Reference: https://arcade.makecode.com/reference/sprites/all-of-kind
# Reference: https://arcade.makecode.com/reference/sprites/sprite/vy
# ============================================================================================================================================================================
# 22. SHARK FACING DIRECTION
# Moving only up or down does not change which way the shark faces.
# If its left/right speed is zero, neither turning condition is true.

def on_forever4():
    global shark_facing_right
    if shark != None:
        if shark.vx > 0 and not (shark_facing_right):
            shark.image.flip_x()
            shark_facing_right = True
        elif shark.vx < 0 and shark_facing_right:
            shark.image.flip_x()
            shark_facing_right = False
forever(on_forever4)

# Reference: https://arcade.makecode.com/reference/sprites/sprite/vx
# Reference: https://arcade.makecode.com/reference/images/image/flip-x
# ============================================================================================================================================================================
# 23. BIG FISH MOVEMENT
# The code checks both the fish position and its movement direction.
# For example, it turns a fish at the left edge only if the fish is still moving left.
# A fish already moving back to the right is allowed to continue without turning again.

def on_forever5():
    global big_fish_facing_left
    if big_fish != None:
        # Left edge
        if big_fish.left <= 0 and big_fish.vx < 0:
            big_fish.left = 0
            big_fish.vx = abs(big_fish.vx)
        elif big_fish.right >= 160 and big_fish.vx > 0:
            # Right edge
            big_fish.right = 160
            big_fish.vx = 0 - abs(big_fish.vx)
        # Top edge
        if big_fish.top <= 0 and big_fish.vy < 0:
            big_fish.top = 0
            big_fish.vy = abs(big_fish.vy)
        elif big_fish.bottom >= 120 and big_fish.vy > 0:
            # Bottom edge
            big_fish.bottom = 120
            big_fish.vy = 0 - abs(big_fish.vy)
        # Face right
        if big_fish.vx > 0 and big_fish_facing_left:
            big_fish.image.flip_x()
            big_fish_facing_left = False
        elif big_fish.vx < 0 and not (big_fish_facing_left):
            # Face left
            big_fish.image.flip_x()
            big_fish_facing_left = True
forever(on_forever5)

# Reference: https://arcade.makecode.com/reference/sprites/sprite/vx# My code checks left <= 0 or right >= 160 only while the fish moves outwards,puts its edge back on the boundary, then changes vx to point into the screen.
# Reference: https://arcade.makecode.com/reference/sprites/sprite/vy
# Reference: https://arcade.makecode.com/reference/images/image/flip-x
# ============================================================================================================================================================================
# 24. SPAWN KILLER WHALE
# Whales can appear before the shark reaches level 3.
# The level controls whether the shark can eat a whale, not whether a whale can appear.
# If a whale is still present at the next 8 second check, no extra whale is created.

def on_update_interval3():
    global killer_whale, whale_facing_left
    if len(sprites.all_of_kind(SpriteKind.KillerWhale)) == 0:
        killer_whale = sprites.create(img("""
                ............dd................
                ............dd................
                ............df................
                ...........ddff...............
                ...........dfff...............
                ..........dffff...............
                .........dffffffd.............
                .....dddddfffffffdd...........
                ....dfffffffffffffffddd...dddf
                ..ddffff1fffffffffffffff.dfff.
                .dffffff1fffffffffffffffdffff.
                .fffffffff11ffffff11fffffd....
                .fff111111ffffff1111fffffd....
                .f1111111fffffff1111....ffdd..
                .1111111ffffff111111....fffd..
                ........ffffff............fff.
                .........fffff................
                ..........fff.................
                ...........ff.................
                ..............................
                """),
            SpriteKind.KillerWhale)
        whale_facing_left = True
        vertical_speed3 = randint(15, 30)
        if randint(0, 1) == 0:
            vertical_speed3 = 0 - vertical_speed3
        killer_whale.set_position(140, randint(25, 95))
        killer_whale.set_velocity(-45, vertical_speed3)
        killer_whale.set_flag(SpriteFlag.AUTO_DESTROY, False)
game.on_update_interval(8000, on_update_interval3)

# Reference: https://arcade.makecode.com/reference/game/on-update-interval
# Reference: https://arcade.makecode.com/reference/sprites/all-of-kind
# Reference: https://arcade.makecode.com/reference/sprites/sprite/set-flag# Its starting velocity is -45 horizontally, with a random vertical speed of 15-30.
# ============================================================================================================================================================================
# 25. HUNGER SYSTEM
# This is a separate repeating timer from the twominute game countdown.
# It does not check can_take_damage, so protection from fish or whale hits
# does not stop hunger from removing a heart.

def on_update_interval4():
    info.change_life_by(-1)
game.on_update_interval(10000, on_update_interval4)
