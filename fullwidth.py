#! /usr/bin/python3

"""Translate ASCII letters into their full-width forms."""

import io
import argparse
import subprocess


class BaseTranslation:

    """Base class of all translation objects."""

    def __init__(self):
        """Create an instance."""
        self.table = dict()

    def translate(self, string):
        """Translate a string based on the translation class."""
        return string.translate(self.table)


class UpperTranslation(BaseTranslation):

    """Translation class for UPPERCASE LETTERS."""

    def translate(self, string):
        """Translate a string based on the translation class."""
        return string.upper().translate(self.table)


class FullWidthTranslation(UpperTranslation):

    """Translation class for ＦＵＬＬ－ＷＩＤＴＨ　ＬＥＴＴＥＲＳ."""

    def __init__(self):
        """Create an instance."""
        super().__init__()
        # Add uppercase-letters
        self.table = {ansi_letter: fullwidth_letter
                      for ansi_letter, fullwidth_letter
                      in zip(range(0x0021, 0x007E), range(0xff01, 0xff5e))}
        # Add space.
        self.table.update({0x0020: 0x3000})


class SuperscriptTranslation(BaseTranslation):

    """Translation class for ˢᵘᵖᵉʳ⁻ˢᶜʳⁱᵖᵗ ˡᵉᵗᵗᵉʳˢ."""

    def __init__(self):
        """Create an instance."""
        self.table = create_table(
            "ABDEGHIJKLMNOPRTUVWabcdefghijklmnoprstuvwxyz0123456789+-=()",
            "ᴬᴮᴰᴱᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᴿᵀᵁⱽᵂᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾",
            )


class SubscriptTranslation(UpperTranslation):

    """Translation class for ₛᵤB₋ₛCᵣᵢₚₜ ₗₑₜₜₑᵣₛ."""

    def __init__(self):
        """Create an instance."""
        self.table = create_table(
            "AEHIJKLMNOPRSTUVX0123456789+-=()",
            "ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎",
            )


class BlackletterTranslation(BaseTranslation):

    """Translation class for 𝔟𝔩𝔞𝔠𝔨𝔩𝔢𝔱𝔱𝔢𝔯."""

    def __init__(self):
        """Create an instance."""
        self.table = create_table(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷",
            )


class BoldBlackletterTranslation(BaseTranslation):

    """Translation class for 𝖇𝖔𝖑𝖉 𝖇𝖑𝖆𝖈𝖐𝖑𝖊𝖙𝖙𝖊𝖗."""

    def __init__(self):
        """Create an instance."""
        self.table = create_table(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟",
            )


class MathScriptTranslation(BaseTranslation):

    """Translation class for 𝓈𝒸𝓇𝒾𝓅𝓉."""

    def __init__(self):
        """Create an instance."""
        self.table = create_table(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏",
            )


class BoldMathScriptTranslation(BaseTranslation):

    """Translation class for 𝓫𝓸𝓵𝓭 𝓼𝓬𝓻𝓲𝓹𝓽."""

    def __init__(self):
        """Create an instance."""
        self.table = create_table(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃",
            )


def create_table(src, dst):
    """Create a translation table from two strings.

    Given strings src="ABC" and dst="abc", this returns a table which
    maps 'A' to 'a', 'B' to 'b', and 'C' to 'c'.

    The strings must be of equal length.
    """
    assert len(src) == len(dst)
    return {ord(from_): ord(to) for (from_, to) in zip(src, dst)}


def send_to_xclip(s):
    """Send a string `s` to xclip's clipboard `XA_CLIPBOARD`.

    Return `True` if the action was successful, `False` otherwise.
    """
    process = subprocess.Popen(
        ['xclip', '-selection', 'clipboard'],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        )
    process.communicate(s.encode('UTF-8'))
    retcode = process.wait()
    return retcode == 0


def create_parser():
    """Create an argparse.ArgumentParser."""
    parser = argparse.ArgumentParser(
        description=__doc__)
    type_g = parser.add_mutually_exclusive_group()
    type_g.add_argument("--full", "-f", action="store_const",
                        const=FullWidthTranslation, dest='translator',
                        help="Translate to full-width letters. (the default)")
    type_g.add_argument("--super", "-s", action="store_const",
                        const=SuperscriptTranslation, dest='translator',
                        help="Translate to superscript letters.")
    type_g.add_argument("--sub", "-S", action="store_const",
                        const=SubscriptTranslation, dest='translator',
                        help="Translate to subscript letters.")
    type_g.add_argument("--black", "-b", action="store_const",
                        const=BlackletterTranslation, dest='translator',
                        help="Translate to blackletters.")
    type_g.add_argument("--bblack", "-B", action="store_const",
                        const=BoldBlackletterTranslation, dest='translator',
                        help="Translate to bold blackletters.")
    type_g.add_argument("--script", "-c", action="store_const",
                        const=MathScriptTranslation, dest='translator',
                        help="Translate to script.")
    type_g.add_argument("--sscript", "-C", action="store_const",
                        const=BoldMathScriptTranslation, dest='translator',
                        help="Translate to bold script.")
    parser.add_argument("words", type=str, nargs=argparse.REMAINDER)
    return parser


def main():
    args = create_parser().parse_args()
    translator = (args.translator or FullWidthTranslation)()
    translation = translator.translate(" ".join(args.words))
    send_to_xclip(translation)
    print(translation)

if __name__ == "__main__":
    main()
