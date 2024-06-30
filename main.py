import pygame, random
import numpy as np

class Particula:
    def __init__(self,env, posicao, velocidade, raio, massa):
        self.env = env
        self.cor = (random.randint(100,255), random.randint(70,170), random.randint(100,255))
        self.pos = posicao
        self.vel = velocidade
        self.raio = raio
        self.m = massa

    def addVelocidade(self,velocidade):
        self.vel += velocidade

    def addPosicao(self, posicao):
        self.pos += posicao

    def move(self): 
        self.pos += self.vel*self.env.dt

    def colisao(self, p2):
        dx = self.pos - p2.pos
        distancia = np.sqrt(np.sum(dx**2))
        # Caso colida
        if distancia < self.raio + p2.raio:
            desvio = distancia - (self.raio + p2.raio)
            self.addPosicao((-dx/distancia) * desvio/2)
            p2.addPosicao((dx/distancia) * desvio/2)

            massa = self.m + p2.m
            v1 = -2*p2.m/massa*np.inner(self.vel-p2.vel,self.pos - p2.pos)/np.sum((self.pos - p2.pos)**2)*(self.pos-p2.pos)
            v2 = -2*self.m/massa*np.inner(p2.vel-self.vel,p2.pos - self.pos)/np.sum((p2.pos - self.pos)**2)*(p2.pos-self.pos)

            self.addVelocidade(v1)
            p2.addVelocidade(v2)

class Enviroment():

    def __init__(self, QUADRO, dt, tela):
        self.particulas = []
        self.dt = dt
        self.QUADRO = QUADRO
        self.display = tela

    
    def addParticulas(self, particula):
        self.particulas.append(particula)

    def update(self):
        for p1 in self.particulas:
            p1.move()
            self.bounce(p1)
            for p2 in self.particulas:
                if p1 != p2:
                    p1.colisao(p2)

    def bounce(self,p):
        for p in self.particulas:
            i = 0
            for x in p.pos[0]:
                if x > self.QUADRO[i]-p.raio:
                    distancia = p.raio-(self.QUADRO[i]-x)
                    p.addPosicao(-distancia)
                    tmp = np.zeros(np.size(p.vel))
                    tmp[i] = -2*p.vel[0][i]
                    p.addVelocidade(tmp)
                elif x < p.raio: 
                    distancia = p.raio-x
                    p.addPosicao(distancia)
                    tmp = np.zeros(np.size(p.pos))
                    tmp[i] = -2*p.vel[0][i]
                    p.addVelocidade(tmp)
                i += 1
        
    def run_simulator(self):

        run = True
        clock = pygame.time.Clock()
        i=0
        while run:
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            tela.fill(black)
            self.update()
            for p in self.particulas:
                pygame.draw.circle(self.display, p.cor , (int(p.pos[0][0]), int(p.pos[0][1])), p.raio)     

            pygame.display.update()
            i+=1
        pygame.quit()

# Parametros
black = (0,0,0)
white = (255,255,255)
QUADRO = np.asarray([800, 550])
numeroDeBolas = 20
dt = 0.04

# Ambiente
tela = pygame.display.set_mode((QUADRO[0], QUADRO[1]))
env = Enviroment(QUADRO, dt,tela)
pygame.display.set_caption('Simulador de colisões elásticas')

# Cria particulas
for i in range(numeroDeBolas):
    raio = np.random.randint(15, 30)
    massa = raio**3
    pos = np.random.rand(1, 2)*(QUADRO -raio)+raio
    vel = np.random.rand(1, 2)*75
    particula = Particula(env,pos,vel,raio,massa)
    env.addParticulas(particula)

env.run_simulator()
