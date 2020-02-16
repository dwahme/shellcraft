import argparse
import shellcraft

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run shellcraft')
    parser.add_argument('-e', action='store', dest='editor', type=str, default="vim",
                        help='Which text editor to use (default: vim)')
    parser.add_argument('-s', action='store', dest='seed', type=int, default=None,
                        help='Which seed to use for world genearation')

    args = parser.parse_args()
    
    game = shellcraft.Game(args.editor, args.seed)
    game.run()
