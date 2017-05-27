#!/usr/bin/env python

from helpers import *
from scene import Scene

from eost.ordinal import *

class OrdinalPowerScene(Scene):

    def construct(self):

        #o = LimitOrdinal(
        #    lambda **kwargs: LimitOrdinal(
        #        lambda **kwargs: LimitOrdinal(
        #            OrdinalOmega,
        #            **kwargs
        #        ),
        #        **kwargs
        #    ),
        #    q = (0.6, 0.8, 0.8))

        o = make_ordinal_power(5, q = (0.7, 0.84, 0.84))

        o.set_color(GRAY)
        omega_group = []
        omega2_group = []
        omega3_group = []
        omega4_group = []

        for o1 in o:
            for o2 in o1:
                for o3 in o2:
                    for o4 in o3:
                        omega_group.append(o4[0])
                    omega2_group.append(o3[0][0])
                omega3_group.append(o2[0][0][0])
            omega4_group.append(o1[0][0][0][0])

        omega_group = VGroup(*omega_group)
        omega2_group = VGroup(*omega2_group)
        omega3_group = VGroup(*omega3_group)
        omega4_group = VGroup(*omega4_group)
        omega_group.set_color(GREEN)
        omega2_group.set_color(YELLOW)
        omega3_group.set_color(ORANGE)
        omega4_group.set_color(RED)

        self.add(o)
        self.add(omega_group)
        self.add(omega2_group)
        self.add(omega3_group)

        print(len(self.get_mobjects()))

        self.dither()

class OrdinalAsIndex(Scene):

    def construct(self):

        o1 = OrdinalOmega()
        o2 = OrdinalOmega(x0 = 4, x1 = 12)
        o = o1.copy()

        o.set_color(WHITE)
        VGroup(o1, o2).highlight(DARK_GREY)

        steps = o.to_steps()
        steps.shift(UP)
        self.add(o1, o2, o)
        self.dither()
        #self.play(o2.shift, UP)     
        self.play(Transform(o, steps,
                            submobject_mode = "one_at_a_time",
                            run_time = 2*DEFAULT_ANIMATION_RUN_TIME,
                            rate_func = rush_into,
        ))
        o2[0].highlight(YELLOW)
        self.dither(3)


class OmegaShowcase(Scene):

    def construct(self):

        o1 = OrdinalOmega()
        o2 = OrdinalOmega(seq = lambda n: o1.seq(2*n))
        o = o1.copy()
        o_odd = VGroup(*[
            tick
            for (i,tick)
            in enumerate(o.submobjects)
            if i % 2 == 1
        ])
        o_odd_target = o_odd.copy()
        o_odd_target.highlight(BLACK)
        o_odd_target.shift(UP)
        self.add(o)
        self.dither()
        self.play(Transform(o_odd, o_odd_target))
        self.dither()
        self.remove(o)
        o = o2.copy()
        self.play(Transform(o, o1))
        self.dither()
