# Tower of Rak

Tower of Rak is a turned-based roguelike game inspired by the Webtoon [Tower of God](https://www.webtoons.com/en/fantasy/tower-of-god/list?title_no=95&page=1).   
The game is set in a world of two opposing races, where the adventure begins as a young Gator hero sets out to conquer the ancient Tower of Rak, which is said to hold a legendary relic with immense powers. The hero seeks to free the Gators from the supression of the overwhelmingly dominant Teurtal race.

## Features
- pixel art graphics
- key elements of roguelikes
  - turned based gameplay
  - procedurally generated maps
  - permadeath
  
### Screenshots
<img src="screenshots/screenshot-1" width=450> <img src="screenshots/screenshot-2" width=450>
<img src="screenshots/screenshot-3" width=450> <img src="screenshots/screenshot-5" width=450>
  
## Download
To download an **early demo** of this game for macOS click <a href="dist/Tower-of-Rak.zip" download>here</a>.  
Unzip the file and simply open the application file to start playing.  
[py2app](https://pypi.org/project/py2app/) was used to bundle everything into this standalone Mac OS X application.

## Development Notes

**NOTE**  
Must use pygame version 2.0.0.dev2 to solve game window display issue on macOS Mojave.  
Also, as this game is still under development, please help by reporting any major bugs. 

### Built with
- [pygame](https://www.pygame.org/) (2.0.0.dev2)
- [tcod](https://pypi.org/project/tcod/) (6.0.6)
- [tdl](https://python-tcod.readthedocs.io/en/latest/tdl.html) (6.0.0)
- [numpy](https://numpy.org/)(1.15.2)

## License
This project is licensed under the GNU General Public License v3.0 License - see the [LICENSE.md](LICENSE) file for details. The license does not cover the game content (artwork, audio, etc.), which are not included and can only be used with the appropriate attributions to the original owners.
