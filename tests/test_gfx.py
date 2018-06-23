from unittest import TestCase

from gtp.gfx import GFX, GFXSymbol, GFXPlayer


class TestGFX(TestCase):

    def test_set_label(self):
        gfx = GFX()
        gfx.set_label('A1', 'label')
        gfx.set_label('A2', 'label')

        self.assertEqual('LABEL A1 label A2 label', gfx.output())

    def test_set_color(self):
        gfx = GFX()
        gfx.set_color('A1', '#0000FF')
        gfx.set_color('A2', '#00FF00')

        self.assertEqual('COLOR #0000FF A1\nCOLOR #00FF00 A2', gfx.output())

    def test_square(self):
        gfx = GFX()
        gfx.set_symbol('A1', GFXSymbol.square)
        gfx.set_symbol('A2', GFXSymbol.square)

        self.assertEqual('SQUARE A1 A2', gfx.output())

    def test_mark(self):
        gfx = GFX()
        gfx.set_symbol('A1', GFXSymbol.mark)
        gfx.set_symbol('A2', GFXSymbol.mark)

        self.assertEqual('MARK A1 A2', gfx.output())

    def test_triangle(self):
        gfx = GFX()
        gfx.set_symbol('A1', GFXSymbol.triangle)
        gfx.set_symbol('A2', GFXSymbol.triangle)

        self.assertEqual('TRIANGLE A1 A2', gfx.output())

    def test_circle(self):
        gfx = GFX()
        gfx.set_symbol('A1', GFXSymbol.circle)
        gfx.set_symbol('A2', GFXSymbol.circle)

        self.assertEqual('CIRCLE A1 A2', gfx.output())

    def test_white(self):
        gfx = GFX()
        gfx.set_symbol('A1', GFXSymbol.white)
        gfx.set_symbol('A2', GFXSymbol.white)

        self.assertEqual('WHITE A1 A2', gfx.output())

    def test_black(self):
        gfx = GFX()
        gfx.set_symbol('A1', GFXSymbol.black)
        gfx.set_symbol('A2', GFXSymbol.black)

        self.assertEqual('BLACK A1 A2', gfx.output())

    def test_set_influence(self):
        gfx = GFX()
        gfx.set_influence('A1', 1)
        gfx.set_influence('A2', 1)

        self.assertEqual('INFLUENCE A1 1 A2 1', gfx.output())

    def test_variation(self):
        gfx = GFX()
        gfx.add_variation(GFXPlayer.black, 'A1')
        gfx.add_variation(GFXPlayer.white, 'PASS')
        gfx.add_variation(GFXPlayer.black, 'A2')

        self.assertEqual('VAR b A1 w PASS b A2', gfx.output())

    def test_set_status(self):
        gfx = GFX()
        gfx.set_status('status')

        self.assertEqual('TEXT status', gfx.output())
