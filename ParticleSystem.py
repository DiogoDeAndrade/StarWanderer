import math
import random
import pygame
import enum
from Color import *
from pygame import Vector2

class Emitter(enum.Enum): 
    Point = 0

class Particle:
    def __init__(self, position, velocity, life, color):
        self.position = self.old_position = position
        self.direction = velocity.normalize()
        self.speed = velocity.magnitude()
        self.life = life
        self.time = 0
        self.color = color        
        self.size = 1
    
class ParticleSystem:
    def __init__(self, position):
        self.position = position
        self.startSpeed = (10, 20)
        self.particleLife = (1, 2)
        self.colorOverTime = [(1,1,1,1),(0,0,0,0)]
        self.emitter = Emitter.Point
        self.rate = 10
        self.accumulated_time = 0
        self.duration = 0
        self.drag = 1.0
        self.time = 0

        self.particles = []

    def Update(self, delta_time):
        self.accumulated_time = self.accumulated_time + delta_time

        particles_to_spawn = (int)(math.floor(self.accumulated_time * self.rate))
        if (particles_to_spawn > 0):
            self.accumulated_time = self.accumulated_time - particles_to_spawn / self.rate
            self.Spawn(particles_to_spawn)

        for particle in self.particles:
            particle.time = particle.time + delta_time
            t = particle.time / particle.life

            particle.speed = particle.speed * self.drag
            particle.old_position = particle.position
            particle.position = particle.position + particle.direction * particle.speed * delta_time
            particle.color = Color.InterpolateWithArray(self.colorOverTime, t)

        for index in range(len(self.particles)-1, -1, -1):
            if (self.particles[index].time > self.particles[index].life):
                del(self.particles[index])

        self.time = self.time + delta_time

    def Render(self, screen):
        for particle in self.particles:
            pygame.draw.line(screen, particle.color.tuple(), particle.old_position, particle.position, (int)(particle.size))

    def Spawn(self, particle_to_spawn):
        if (self.emitter == Emitter.Point):
            for i in range(0, particle_to_spawn):
                ang = random.uniform(0, math.pi * 2)
                v = Vector2(math.cos(ang), math.sin(ang))
                v = v * random.uniform(self.startSpeed[0], self.startSpeed[1])
                particle = Particle(self.position, v, random.uniform(self.particleLife[0], self.particleLife[1]), self.colorOverTime[0].tuple())
                self.particles.append(particle)

    def IsAlive(self):
        if (self.duration == 0):
            return True
        if (self.time > self.duration):
            if (len(self.particles) > 0):
                return False

        return True