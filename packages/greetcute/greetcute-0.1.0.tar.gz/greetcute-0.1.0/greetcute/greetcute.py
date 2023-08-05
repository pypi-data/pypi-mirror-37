# -*- coding: utf-8 -*-

"""Main module."""

from random import choice


def greet():
    """
    Prints a loving statement for your entertainment and
    edification.
    """
    sweet_names = ['bunny', 'sweet pea', 'cherub', 'muffin',
                   'octopus', 'forrest animal', 'baby fawn', 'jelly bean',
                   'honeycomb', 'unicorn', 'merperson', 'musk ox',
                   'tropical fish', 'sunfish', 'baby hedgehog', 'koala',
                   'cinnamon stick', 'ginger beer', 'rain drop', 'sunbeam']
    adjectives = ['fantastic', 'luxurious', 'benevolent', 'sparkly',
                  'attractive', 'dashing', 'handsome', 'pretty', 'charming',
                  'friendly', 'spiff-o-rific', 'poetic', 'powerful', 'talented',
                  'opalescent', 'shimmery', 'sassy', ]
    compliment = ['the bees knees', 'super swell', 'an amazing human',
                  'elegant, like a sea bird', 'super good at stuff and things',
                  'lovely as a snowy owl perched in a snowy tree',
                  'mysterious, like a tv superhero', ]
    return (f"Hello you {choice(adjectives)} {choice(sweet_names)}! "
          f"I think you're {choice(compliment)}.")
