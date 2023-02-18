#-----------------------------------------------------------
# Autor/Author: Pedro Pampolini Mendicino      Criação/Created: 16/02/2023
# Ultima modificação/Last change: 17/02/2023
# Objetivo: Converter um video em ASCII e salvar em um .txt
# Objective: Convert a video to ASCII and save in a .txt file
# To play the video, use BadAppleGame.py
#-----------------------------------------------------------

import cv2
import time
import pygame
from moviepy.editor import VideoFileClip
from threading import Thread
import numpy as np

class VideoToASCII:
    

    #Método que retorna o pixel em escala de cinza || Method that returns the pixel in grayscale   
    def verificaTom(self,arr:np.array):
        #Soma o RGB do pixel e faz a média para pegar o tom de cinza    || Sum the RGB of the pixel and make the average to get the grayscale
        total = int((int(arr[0]) + int(arr[1]) + int(arr[2]))/3)
        return total

    #Método que retorna o caractere de acordo com a luminosidade em ASCII || Method that returns the character according to the luminosity in ASCII
    def getCharByShadow(self,char, multi:float=1.0, invert:bool=False):
        #Se quiser inverter a luminosidade da imagem    || If you want to invert the luminosity of the image
        if(invert):
            char = 255 - char
        if(char < (50 * multi)):
            return "█"
        elif(char < (100 * multi)):
            return "▓"
        elif(char < (150 * multi)):
            return "▒"
        elif(char < (200 * multi)):
            return "░"
        else:
            return " "

    def getAudioFromVideo(self,videoPath:str, audioPath:str):
        # Path to video file
        video = VideoFileClip(videoPath)
        # Path to audio file
        audio = video.audio
        # Write audio file
        audio.write_audiofile(audioPath)
        # Close video file
        video.close()
        audio.close()

    #Método construtor || Constructor method
    def __init__(self,videoFilePath:str,outputFilePath:str,songFilePath:str):
        self.__videoFilePath = videoFilePath
        self.__outputFilePath = outputFilePath
        self.__songFilePath = songFilePath
        #Inicia o video e seus atributos  || start the video and its attributes
        self.__video = cv2.VideoCapture(videoFilePath) #Carrega o video como um objeto   || Load the video as an object
        self.__ratio = 5       #ratio de reducao da imagem || image reduction ratio
        self.__framesCounter = 0   #contador de frames para a porcentagem  || frame counter for percentage
        self.__width = int(self.__video.get(cv2.CAP_PROP_FRAME_WIDTH))    #pega a largura do frame    || get the frame width
        self.__height = int(self.__video.get(cv2.CAP_PROP_FRAME_HEIGHT))    #pega a altura do frame   || get the frame height

        #Inicializa o arquivo com os atributos do video || initialize the file with the video attributes        
        self.__file = open(self.__outputFilePath,"w",encoding="UTF-8")    #cria o arquivo que conterá os frames   || create the file that will contain the frames
        self.__file.write(f"{self.__width}\n")  #Salva a largura  || save the width
        self.__file.write(f"{self.__height}\n")    #Salva a altura    || save the height
        self.__file.write(f"{self.__ratio}\n")    #Salva o ratio  || save the ratio
        self.__file.write(f"{int(self.__video.get(cv2.CAP_PROP_FRAME_COUNT))}\n")    #Salva a quantidade de frames    || save the number of frames

    def close(self):
        self.__file.close()
        self.__video.release()
        

    #Método que converte o video em ASCII e salva no arquivo || Method that converts the video to ASCII and saves in the file
    def convert(self):

        print("Convertendo o audio do video... || Converting the video audio...")
        self.getAudioFromVideo(self.__videoFilePath,self.__songFilePath)
        print("Audio convertido com sucesso! || Audio converted successfully!")
        print("Convertendo o video... || Converting the video...")
        progresso = 0   #variavel para mostrar o progresso  || variable to show the progress
        while True:
            
            ret, frame = self.__video.read()   #pega o frame do video  || get the video frame
            if not ret:     #se nao tiver mais frames, sai do loop  || if there are no more frames, exit the loop
                break
            width = int(len(frame))    #pega a largura do frame || get the frame width
            height = int(len(frame[0]))    #pega a altura do frame  || get the frame height
            resized_frame = cv2.resize(frame, (int(width/self.__ratio), int(height/self.__ratio)))    #Redimensiona o frame   || Resize the frame
                
            for i in resized_frame:
                for j in i:
                    char = self.getCharByShadow(self.verificaTom(j),multi=1,invert=True)  #pega o caractere de acordo com o pixel     || get the character according to the pixel
                    self.__file.write(char + char + char + char)   #escreve o caractere 4 vezes para aumentar a largura da imagem  || write the character 4 times to increase the image width
                self.__file.write("\n")
                
            #Calcula a porcentagem de progresso || Calculate the percentage of progress
            progressoAnti = progresso
            #Recupera o progresso atual || Retrieve the current progress
            progresso = int((self.__framesCounter/int(self.__video.get(cv2.CAP_PROP_FRAME_COUNT)))*100)
            #Caso tenha progredido 1%, imprime na tela  || If have progressed 1%, show it on the screen
            if(progresso != progressoAnti):
                print(f"\r{progresso}% concluido",end="")
            
            self.__framesCounter += 1  #incrementa o contador de frames    || increment the frame counter
        print()

        print("Terminou||Finished")
        self.close()
        
class playVideo:
    
    def pegaFrame(self):
        
        frame = str()   #Cria uma string para armazenar o frame  || Create a string to store the frame
        #Recupera todas as linhas do frame  || Get all the lines of the frame
        for w in range(self.__width):
            linha = self.__file.readline() #Recupera a linha   || Get the line
            frame += linha  #Adiciona a linha ao frame  || Add the line to the frame
        frame.replace("\n\n","\n")  #Remove os \n que ficam no final do frame   || Remove the \n that are at the end of the frame
        return frame

    
    def __init__(self,songFilePath:str, inputFilePath:str):
        self.__songFilePath = songFilePath
        self.__inputFilePath = inputFilePath
        
        #Abre o arquivo dos frames || Open the file of the frames
        self.__file = open(inputFilePath,"r",encoding="UTF-8")  #Abre o arquivo que contém os frames   || Open the file that contains the frames
        self.__width = int(self.__file.readline())    #Recupera a largura   || Get the width
        self.__heigth = int(self.__file.readline())   #Recupera a altura  || Get the heigth
        self.__ratio = int(self.__file.readline())    #Recupera o ratio de reducao    || Get the ratio
        self.__framesCount = int(self.__file.readline())  #Recupera a quantidade de frames    || Get the frames count

        self.__width = int(self.__width/self.__ratio)
        self.__heigth = int(self.__heigth/self.__ratio)
    
    def close(self):
        self.__file.close()
    
    def playVideo(self,fps=32):
        if(fps < 1):
            raise ValueError("O fps deve ser maior que 0 || The fps must be greater than 0")
        
        
        pygame.init()       #Inicializa o pygame    || Initialize pygame
        #recupera a largura da tela para encaixar o video   || Get the screen width to fit the video
        windowWidth, windowHeight = pygame.display.Info().current_w, pygame.display.Info().current_h

        #Cria a janela do pygame ja em fullscreen   || Create the pygame window in fullscreen
        window = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)
        pygame.display.set_caption("Bad Apple") #Coloca o titulo da janela  || Set the window title

        font = pygame.font.SysFont("Courier", 3)    #Seta a fonte da ASCII art e o tamanho padrão   || Set the font of the ASCII art and the default size
        text = font.render("Init", True, (255, 255, 255))  #Cria o texto inicial    || Create the initial text

        pygame.mixer.init() #Inicializa o mixer de musica do pygame  || Initialize the pygame music mixer
        pygame.mixer.music.load(self.__songFilePath)  #Carrega a musica na memória    || Load the music in the memory
        pygame.mixer.music.play()   #Toca a musica  || Play the music

        # Loop principal    || Main loop
        while True:
            # Limita a taxa de quadros em 30fps  || Limit the frame rate to 30fps
            thread = Thread(target=lambda: time.sleep(1/fps))    
            thread.start()
            
            # Processa eventos do pygame    || Process pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Atualiza o texto  || Update the text
            frame = self.pegaFrame()
            frame = frame.splitlines()  #Quebra o frame em linhas   || Split the frame in lines
            
            line_height = font.get_linesize()   
            # Cria uma superfície para o texto  || Create a surface for the text
            text_surface = pygame.Surface((windowWidth, len(frame) * line_height))
            # Desenha o texto na superfície  || Draw the text in the surface
            for i, line in enumerate(frame):
                line_surface = font.render(line, True, (255, 255, 255))
                text_surface.blit(line_surface, (0, i * line_height))

            # define a posição do texto na tela || define the text position in the screen
            text_rect = text_surface.get_rect(center=(windowWidth/2 + 250, windowHeight/2))
            # desenha o texto na tela  || draw the text in the screen
            window.blit(text_surface, text_rect)
            pygame.display.flip()
            
            thread.join()   #Espera o tempo do frame acabar   || Wait for the frame time to end
            
            # Atualiza a janela do pygame   || Update the pygame window
            pygame.display.update()
        
        self.close()
            
