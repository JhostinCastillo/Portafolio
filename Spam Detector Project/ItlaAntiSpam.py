import pygame
import time
import clipboard
from transformers import pipeline
pygame.init()

def procesar_texto(input: str, PIPE = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")):
    x = PIPE(input)[0]
    if x["label"] == "LABEL_0":
        return "no spam"
    else:
        return "spam"
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

def mostrar_imagen(imagen):
    screen.blit(imagen, ((SCREEN_WIDTH - imagen.get_width()) // 2, (SCREEN_HEIGHT - imagen.get_height()) // 2))
    pygame.display.flip()
    time.sleep(5)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ITLA IA ANTISPAM")
icono = pygame.image.load(r'Recursos\icono.ico')
pygame.display.set_icon(icono)

def main():
    running = True
    font = pygame.font.Font(None, 36)
    texto = ""

    fondo = pygame.image.load(r'Recursos\1.png')  

    while running:
        screen.blit(fondo, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    resultado = procesar_texto(texto)
                    if resultado == 'spam':
                        imagen_spam = pygame.image.load(r'Recursos\2.png')  
                        mostrar_imagen(imagen_spam)
                    else:
                        imagen_no_spam = pygame.image.load(r'Recursos\3.png')  
                        mostrar_imagen(imagen_no_spam)
                    texto = ""
                elif event.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    texto += clipboard.paste()
                else:
                    texto += event.unicode

        texto_surface = font.render(texto, True, (255, 255, 255))
        screen.blit(texto_surface, ((SCREEN_WIDTH - texto_surface.get_width()) // 2, (SCREEN_HEIGHT - texto_surface.get_height()) // 2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
