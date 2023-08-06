# Liberate

Liberate is a Python 3 program written to convert audio/video files to .ogg audio files.

## Quick install

Assuming you have ffmpeg installed.

```
$ git clone --depth=1 https://notabug.org/necklace/liberate.git
$ cd liberate
$ sudo python setup.py install
```

## Examples

Convert a single existing file (any format, video or audio):
```
liberate file_to_convert.ext
```
Convert a whole directory of files (not recursive, will only take files in directory):
```
liberate path/to/directory/
```
Download from an external source (like youtube or soundcloud) using youtube-dl and convert:
```
liberate https://example.com/audio.mp3
```
Liberate doesn't delete the downloaded file by default, if you only want to keep the converted .ogg file:
```
liberate https://example.com/audio.mp3 --remove
```


## Dependencies

- ffmpeg
- youtube-dl (python)
- colorama (python)
- unix based system

This script is not tested on Windows, and most likely won't work at all on
any version of Windows. Feel free to add support and send me a pull request,
though.


## Development

Install python dependencies with `sudo pip3 install -r requirements.txt` 
(though these will be installed automatically if setup.py was ran)



