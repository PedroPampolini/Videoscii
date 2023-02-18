# Videoscii - Português

Converte um vídeo em ASCII e salva em um arquivo.txt.

## Como usar

Para converter o vídeo em ASCII, crie uma instância da classe `VideoToASCII` passando como parâmetros o caminho do arquivo de vídeo e o caminho do arquivo de saída .txt:

```python
from VideoToASCII import VideoToASCII

videoFilePath = "exemplo_video.mp4"
outputFilePath = "exemplo_video_ascii.txt"
songFilePath = "exemplo_video_audio.mp3"
v2a = VideoToASCII(videoFilePath, outputFilePath, songFilePath)
v2a.convert()
```

Após convertido, pode usar a clase `playVideo` para executar o video criado da seguinte forma:

```python
from VideoToASCII import playVideo

inputFilePath = "exemplo_video_ascii.txt"
songFilePath = "exemplo_video_audio.mp3"
vid = VideoToASCII(intputFilePath, songFilePath)
vid.playVideo()
```

##Dependências
Algumas bibliotecas são necessárias para esse projeto, sendo elas:
- opencv: `pip install opencv-python`
- pygame: `pip install pygame`
- moviepy: `pip install moviepy`
- numpy: `pip install numpy`


# Videoscii - English

Converts a video to ASCII and saves it in a .txt file.

## How to Use

To convert the video to ASCII, create an instance of the `VideoToASCII` class by passing the video file path and the output .txt file path as parameters:

```python
from VideoToASCII import VideoToASCII

videoFilePath = "exemplo_video.mp4"
outputFilePath = "exemplo_video_ascii.txt"
songFilePath = "exemplo_video_audio.mp3"
v2a = VideoToASCII(videoFilePath, outputFilePath, songFilePath)
v2a.convert()
```

Once it's converted, you can use the `playVideo` class to play the created video as follows:

```python
from VideoToASCII import playVideo

inputFilePath = "exemplo_video_ascii.txt"
songFilePath = "exemplo_video_audio.mp3"
vid = VideoToASCII(intputFilePath, songFilePath)
vid.playVideo()
```

##Dependencies
Some libraries are required for this project, which are:
- opencv: `pip install opencv-python`
- pygame: `pip install pygame`
- moviepy: `pip install moviepy`
- numpy: `pip install numpy`
