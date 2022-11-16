import numpy
import random
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm
from math import *

pygame.init()

screen = pygame.display.set_mode(
    (900, 600),
    pygame.OPENGL | pygame.DOUBLEBUF
)
# dT = pygame.time.Clock()



vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;

uniform mat4 amatrix;

out vec3 ourColor;
out vec2 fragCoord;


void main()
{
    gl_Position = amatrix * vec4(position, 1.0f);
    fragCoord =  gl_Position.xy;
    ourColor = vertexColor;

}
"""

fragment_shader = """
#version 460

layout (location = 0) out vec4 fragColor;

uniform vec3 color;


in vec3 ourColor;

void main()
{
    fragColor = vec4(ourColor, 1.0f);
    fragColor = vec4(color, 1.0f);
}
"""


fragment_shader2 = """
#version 460

layout (location = 0) out vec4 fragColor;

uniform float iTime;
vec2 vp = vec2(320.0, 200.0);

in vec2 fragCoord;

vec3 iResolution = vec3(500,500,500);
float pi = 3.1415926435;

void main()
{
    float i = fragCoord.x;
    vec3 t = (iTime) / vec3(63.0, 78.0, 45.0);
    vec3 cs = cos(i * pi * 2.0 + vec3(0.0, 1.0, -0.5) * pi + t);
    fragColor = vec4(0.5 + 0.5 * cs, 1.0);    
}
"""

fragment_shader3 = """
#version 460

layout (location = 0) out vec4 fragColor;

uniform float iTime;
uniform vec3 color;
vec2 vp = vec2(320.0, 200.0);

in vec2 fragCoord;

vec3 iResolution = vec3(500,500,500);
float pi = 3.1415926435;

void main()
{
    float i = fragCoord.x;
    vec3 t = (iTime) / color;
    vec3 cs = cos(i * pi * 2.0 + vec3(0.0, 1.0, -0.5) * pi + t);
    vec3 ct = sin(i * pi * 2.0 + vec3(0.0, 1.0, -0.5) * pi + t);
    
    fragColor = vec4(0.5 + 0.5 * ct, 1.0);    
}
"""
compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
compiled_fragment_shader2 = compileShader(fragment_shader2, GL_FRAGMENT_SHADER)
compiled_fragment_shader3 = compileShader(fragment_shader3, GL_FRAGMENT_SHADER)

shader1 = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader
)

shader2 = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader2
)

shader3 = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader3
)

shader = shader1
glUseProgram(shader)      
glEnable(GL_DEPTH_TEST)



vertex_data = numpy.array([
    #Caras frontales
    1, 0, 0,
    0, 1, 0,
    0, 0, 0,
    
    1, 0, 0,
    0, 1, 0,
    1, 1, 0,
    
    1, 0, 1,
    0, 1, 1,
    0, 0, 1,
    
    1, 0, 1,
    0, 1, 1,
    1, 1, 1,
#---------------------------------------    
    
    0, 1, 0,
    0, 0, 1, 
    0, 0, 0,
    
    0, 1, 0,
    0, 0, 1,
    0, 1, 1,
    
    1, 1, 0, 
    1, 0, 1, 
    1, 0, 0, 
    
#---------------------------------------    
    
    0, 1, 1,  
    1, 1, 0,  
    0, 1, 0,  
    
    0, 1, 1, 
    1, 1, 0, 
    1, 1, 1,     
    
    
    0, 0, 1,  
    1, 0, 0,  
    0, 0, 0,  
    
    0, 0, 1, 
    1, 0, 0, 
    1, 0, 1, 

], dtype=numpy.float32)

vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(
    GL_ARRAY_BUFFER,  # tipo de datos
    vertex_data.nbytes,  # tamaño de da data en bytes    
    vertex_data, # puntero a la data
    GL_STATIC_DRAW
)
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

glVertexAttribPointer(
    0,
    3,
    GL_FLOAT,
    GL_FALSE,
    3*4,
    ctypes.c_void_p(0)
)
glEnableVertexAttribArray(0)


glVertexAttribPointer(
    1,
    3,
    GL_FLOAT,
    GL_FALSE,
    3*4,
    ctypes.c_void_p(3 * 4)
)
glEnableVertexAttribArray(1)


def calculateMatrix(angle,vector_rotatio,vector_translate =(0,-0.5,0)):
    i = glm.mat4(1)
    translate = glm.translate(i, glm.vec3(vector_translate))
    rotate = glm.rotate(i, glm.radians(angle), glm.vec3(vector_rotatio))
    scale = glm.scale(i, glm.vec3(1, 1, 1))

    model = translate * rotate * scale

    view = glm.lookAt(
        glm.vec3(0, 0, 5),
        glm.vec3(0, 0, 0),
        glm.vec3(0, 1, 0)
    )

    projection = glm.perspective(
        glm.radians(45),
        900/600,
        0.1,
        1000.0
    )

    amatrix = projection * view * model

    glUniformMatrix4fv(
        glGetUniformLocation(shader, 'amatrix'),
        1,
        GL_FALSE,
        glm.value_ptr(amatrix)
    )

glViewport(0, 0, 900, 600)



running = True

glClearColor(0.5, 1.0, 0.5, 1.0)

r = 0
opcion1 = True
opcion2 = False
opcion3 = False
suma = 1
color1 = random.random()
color2 = random.random()
color3 = random.random()

while running:
    
    r += suma
    
    glUniform1f(
                glGetUniformLocation(shader,'iTime'),
                r/100
            )
    
    if opcion1:
        shader = shader1
        glUseProgram(shader)              
        if r >= 255:
            suma =-1
        if r <= 0:
            suma =1
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        color = glm.vec3((r%255)/255,0,0)
        glUniform3fv(
                glGetUniformLocation(shader,'color'),
                1,
                glm.value_ptr(color)
            )
        
        
        calculateMatrix(2*r,(0, 1, 0))
        
    if opcion2:
        shader = shader3
        glUseProgram(shader)              
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        if r % 15 ==0:
            color1 = random.random()
            color2 = random.random()
            color3 = random.random()

            color = glm.vec3(color1, color2, color3)

        glUniform3fv(
            glGetUniformLocation(shader,'color'),
            1,
            glm.value_ptr(color)
        )
    
        calculateMatrix(r,(0.5, 1, 0.1))
        
    
    if opcion3:
        shader = shader2
        glUseProgram(shader)              
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        mov = (0,sin(r/10),cos(-r/10))

        if r % 4 == 0:
            color = glm.vec3(0, 0, 255)
        elif r % 3 == 0:
            color = glm.vec3(0, 255, 0)
        elif r % 2 == 0:
            color = glm.vec3(255, 0, 0)
        
        glUniform3fv(
                glGetUniformLocation(shader,'color'),
                1,
                glm.value_ptr(color)
            )
        calculateMatrix(5*r,(0, 0.1, 0.1),mov)
    
    
    

    pygame.time.wait(50)


    glDrawArrays(GL_TRIANGLES, 0, len(vertex_data))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
            
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_1):
                opcion1 = True
                opcion2 = False
                opcion3 = False
            if (event.key == pygame.K_2):
                opcion1 = False
                opcion2 = True
                opcion3 = False
                suma =1
                
            if (event.key == pygame.K_3):
                opcion1 = False
                opcion2 = False
                opcion3 = True
                suma =1