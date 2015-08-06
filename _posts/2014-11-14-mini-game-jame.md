---
layout: post
title: Mini Game Jam
date: 2014-11-14 18:12:00 +0000
---


Theme: Hold The Line

Today we are having a mini "game jam". The idea is to give people a
chance to get used to some of the tools and techniques they might need
to take part in [Ludum Dare][] (the next Ludum Dare event is from the 5th-8th December 2014).

For this event, we strongly suggest that people use [Love2D][]. Love2D is a game-development framework written using [lua][], a small and easy-to-learn language.


## Running Love2D on departmental machines

Love2D is not installed on the departmental machines. Fortunately, HackSoc has a server set up to provide various useful pieces of software that are not on the departmental machines, including Love2D.

Go to [klaxon.hacksoc.org][] and follow the instructions there to get this
working on an ITS Linux machine.

## A one-minute guide to Love2D

1. Create a folder to contain your game:

    `mkdir mygame`
    
2. Create a file `main.lua` inside that directory. The body of
   `main.lua` should probably follow the following skeleton:
   
        function love.load()
            -- initialisation code goes here
        end

        function love.update(dt)
            -- simulate the passing of time---<dt> is the
            -- time (fraction of a second) that has passed
            -- since the last call to love.update
        end

        function love.draw()
            -- draw the current frame
        end

        function love.keypressed(key)
            -- handle <key> being pressed
        end

        function love.keyreleased(key)
            -- handle <key> being released
        end
        
        function love.mousepressed(x, y, button)
            -- handle mouse presses
        end
        
        function love.mousereleased(x, y, button)
            -- handle mouse button releases
        end

   (You may not need to handle all of those callbacks)

3. Run the game:

    `grprun love mygame`

## Love2D Resources:

- The [Love2D website][Love2D] obviously has links to many resources.

- Documentation for the [love namespace][], in which all Love2D
  modules live. The modules here most likely to be useful are:
    + [love.graphics][]
    + [love.keyboard][]
    + [love.mouse][]

- A table of all [Love2D Key Constants][]

## Lua Resources:

- A [brief introduction to Lua][]

- There are many tutorials in the Lua [tutorial directory][]. Most of
  these are either too basic or too sophisticated, however, the
  [tables tutorial][], the [modules tutorial][], and the
  [OO tutorial][] are worth reading.

## Other Resources & Examples:

One of the previous HackSoc Ludum Dare entries was written using Love2D: it can be found [on github][LudumDare28].

Some HackSoc committee members wrote examples to remind themselves how to use Love2D:

- A [minimal brawler by qlkzy][]
- An [asteroids clone by barrucadu][]

## Hints & Tips

- **Don't** use the Love2D physics module---it's massive overkill and lots
  of work.
  
- If you want physics, it's usually easiest to write something simple
  from scratch based on velocities and magic numbers. Code like

        x = x + vx * dt
  
        y = y + vy * dt
  is very common.
  
- Don't worry too much about good software design.

- Some use of Lua's "OO" features will make life easier (but see above
  about not getting hung up on good design).




[Ludum Dare]: http://ludumdare.com/compo
[Love2D]: http://love2d.org
[lua]: http://lua.org
[LudumDare28]: http://github.com/HackSoc/LudumDare28
[Love2D Key Constants]: http://love2d.org/KeyConstant
[minimal brawler by qlkzy]: http://github.com/qlkzy/indestructible-pastry
[asteroids clone by barrucadu]: http://github.com/barrucadu/luasteroids
[klaxon.hacksoc.org]: http://klaxon.hacksoc.org
[love namespace]: http://love2d.org/wiki/love
[love.graphics]: http://love2d.org/wiki/love.graphics
[love.keyboard]: http://love2d.org/wiki/love.keyboard
[love.mouse]: http://love2d.org/wiki/love.mouse
[brief introduction to Lua]: http://awesome.naquadah.org/wiki/The_briefest_introduction_to_Lua
[tutorial directory]: http://lua-users.org/wiki/TutorialDirectory
[tables tutorial]: http://lua-users.org/wiki/TablesTutorial
[modules tutorial]: http://lua-users.org/wiki/ModulesTutorial
[OO tutorial]: http://lua-users.org/wiki/ObjectOrientationTutorial
