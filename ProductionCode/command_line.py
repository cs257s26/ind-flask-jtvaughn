#in this file we'll call our 3 teammate's files
import argparse
import sys

from top_species_command_line import (
    forward_geocode,
    filter_by_radius,
    top_species_by_taxon,
)
from game_command_line import game

from top_species_command_line import load_data as load_species_data
from game_command_line import load_data as load_game_data

from leaderboard_command_line import load_data as load_leaderboard_data
from leaderboard_command_line import create_leaderboard
from leaderboard_command_line import check_for_improper_request

def cmd_leaderboard(args):
    """Displays the top 100 species-specific contributors to INaturalist in Minnesota for a given animal. 
    
    Args:
        args: Parsed command-line arguments. Expects args.animal (str)."""
    creature_of_interest = args.animal

    data = load_leaderboard_data()
    if check_for_improper_request(creature_of_interest, data):
        create_leaderboard(creature_of_interest, data)
    

def cmd_species(args):
    """Finds most observed species near a location in Minnesota.
    
    Args:
        args: Parsed command-line arguments. Expects args.city (str), optional args.radius (float), and optional args.top (int).
    """
    data = load_species_data()
    coords = forward_geocode(args.city)
    if coords is None:
        print(f"Could not geocode '{args.city}'")
        sys.exit(1)
    lat, lon = coords
    observations = filter_by_radius(data, lat, lon, args.radius)
    if len(observations) == 0:
        print(f"No observations found near '{args.city}'. Make sure your location is in Minnesota.")
        sys.exit(1)
    print(f"Found {len(observations)} observations within {args.radius} miles of {args.city}:")
    top_by_taxon = top_species_by_taxon(observations, args.top)
    for taxon_group, species_list in top_by_taxon.items():
        print(f"\n{taxon_group.capitalize()}:")
        for taxon_name, common_name, count in species_list:
            print(f"{common_name} ({taxon_name}): {count} observations")


def cmd_game(args):
    """Starts the mammal guessing game.
    
    Args:
        args: Parsed command-line arguments. No additional arguments expected.
    """
    game(load_game_data())


def main():
    parser = argparse.ArgumentParser(prog="command_line.py")
    sub = parser.add_subparsers(dest="command", required=True)

    p_species = sub.add_parser("species", help="Find commonly observed species near a MN location")
    p_species.add_argument("city", type=str, help="e.g. 'Northfield, Minnesota'")
    p_species.add_argument("--radius", type=float, default=10)
    p_species.add_argument("--top", type=int, default=3)
    p_species.set_defaults(func=cmd_species)

    p_game = sub.add_parser("game", help="Run the mammal guessing game")
    p_game.set_defaults(func=cmd_game)

    p_leaderboard = sub.add_parser("leaderboard", help="Find the top 100 species-specific contributors to INaturalist in Minnesota")
    p_leaderboard.add_argument("animal", type=str, help="e.g. 'Muskrat'")
    p_leaderboard.set_defaults(func=cmd_leaderboard)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

